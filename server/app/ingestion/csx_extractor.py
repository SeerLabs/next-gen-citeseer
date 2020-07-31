import os

import re

from pathlib import Path
import xml.sax.saxutils as xmlutils
from ingestion.interfaces import CSXExtractor
from xml.etree.ElementTree import parse, tostring
from models.elastic_models import Paper, Author, Citation
import functools
import json


def extract_affiliations(affiliation_node):
    org_name_nodes = affiliation_node.findall('./orgName')

    # orders org_name nodes
    def compare(n1, n2):
        # types of orgNames in order from least to most important this means
        # institution nodes should come first, then department, then laboratory, then any others
        types = ['laboratory', 'department', 'institution']
        score1 = (0 if not n1.get('type') in types else types.index(n1.get('type')))
        score2 = (0 if not n2.get('type') in types else types.index(n2.get('type')))
        score = -cmp(score1, score2)

        if score != 0:
            return score
        # if same type or orgName nodes, then order by the key attribute
        else:
            return cmp(n1.get('key', ''), n2.get('key', ''))

    def cmp(a, b):
        return (a > b) - (a < b)

    sorted(org_name_nodes, key=functools.cmp_to_key(compare))
    return ', '.join([n.text for n in org_name_nodes])


def extract_authors_from_tei_root(tei_root):
    """Retreive author names from TEI doc"""
    namespaces = {'ns1': 'http://www.tei-c.org/ns/1.0'}
    authors = tei_root.findall('./teiHeader//biblStruct//author')
    paper_authors = []
    if authors is None:
        return paper_authors
    for author_node in authors:
        forename = ''
        if author_node.find("./ns1:persName/ns1:forename", namespaces) is not None:
            forename = author_node.find("./ns1:persName/ns1:forename", namespaces).text
        surname = ''
        if author_node.find("./ns1:persName/ns1:surname", namespaces) is not None:
            surname = author_node.find("./ns1:persName/ns1:surname", namespaces).text
        email = ''
        if author_node.find("./email") is not None:
            email = author_node.find("./email").text
        author = Author(forename=forename, surname=surname, email=email)
        # Find and output affiliation-related info
        affiliations = author_node.findall('./affiliation')
        if affiliations:
            # Use a pipe to delimit seperate affiliations
            affiliation_str = " | ".join(map(extract_affiliations, affiliations))
            author.affiliation = affiliation_str
        paper_authors.append(author)
    return paper_authors


def extract_title_from_tei_root(tei_root):
    title_node = tei_root.find('./teiHeader//titleStmt/title')
    if title_node is not None:
        return title_node.text
    return ''


def xml_to_plain_text(xml_string):
    remove_tags = re.compile(r'\s*<.*?>', re.DOTALL | re.UNICODE)
    plain_text = remove_tags.sub('\n', xml_string)
    # run this twice for weird situations where things are double escaped
    plain_text = xmlutils.unescape(plain_text, {'&apos;': "'", '&quot;': '"'})
    plain_text = xmlutils.unescape(plain_text, {'&apos;': "'", '&quot;': '"'})

    return plain_text.strip()


def extract_abstract(tei_root):
    abstract_node = tei_root.find('./teiHeader/profileDesc/abstract')
    abstract = ""
    if abstract_node is not None:
        xml_string = tostring(abstract_node).decode('utf-8')
        remove_heading = re.compile(r'\s*<head.*?>.*?<\s*/\s*head>', re.DOTALL | re.UNICODE)
        xml_string = remove_heading.sub('', xml_string)
        abstract = xml_to_plain_text(xml_string)
    return abstract


def extract_citations_from_tei_root(tei_root):
    citations = []
    """Retrieve author names from TEI doc"""
    namespaces = {'ns1': 'http://www.tei-c.org/ns/1.0'}
    citations_strucs = tei_root.findall('./text//listBibl//biblStruct')
    if citations_strucs is None:
        return citations
    for citations_struc in citations_strucs:
        citation = Citation()

        if citations_struc.find('./analytic/title') is not None:
            citation.title = citations_struc.find('./analytic/title').text
        elif citations_struc.find('./monogr/title') is not None:
            citation.title = citations_struc.find('./monogr/title').text
        else:
            citation.title = ''

        if citations_struc.findall('./analytic/author') is not None and len(
                citations_struc.findall('./analytic/author')):
            authors_strucs = citations_struc.findall('./analytic/author')
        elif citations_struc.findall('./monogr/author') is not None:
            authors_strucs = citations_struc.findall('./monogr/author')
        else:
            continue

        for authors_struc in authors_strucs:
            author = Author()
            if authors_struc.find("./ns1:persName/ns1:surname", namespaces) is not None:
                author.surname = authors_struc.find("./ns1:persName/ns1:surname", namespaces).text
            if authors_struc.find("./ns1:persName/ns1:forename", namespaces) is not None:
                author.forename = authors_struc.find("./ns1:persName/ns1:forename", namespaces).text
            citation.authors.append(author)
        citations.append(citation)
    return citations


def extract_text_from_tei_root(tei_root):
    body_node = tei_root.find('./text/body')
    xml_string = tostring(body_node).decode('utf-8')
    plain_text = xml_to_plain_text(xml_string)
    return plain_text


class CSXExtractorImpl(CSXExtractor):

    def batch_extract_textual_data(self, dirPath):
        all_files = list(Path(dirPath).rglob("*.[tT][eE][iI]"))
        papers = []
        for filepath in all_files:
            papers.append(self.extract_textual_data(filepath))
        return papers

    def extract_figures(self, filepath):
        pass

    def batch_extract_figures(self, dirPath):
        pass

    def extract_textual_data(self, filepath):
        tei_root = parse(filepath)
        paper = Paper()
        paper.title = extract_title_from_tei_root(tei_root)
        paper.abstract = extract_abstract(tei_root)
        paper.authors = extract_authors_from_tei_root(tei_root)
        paper.citations = extract_citations_from_tei_root(tei_root)
        paper.text = extract_text_from_tei_root(tei_root)
        return paper


if __name__ == "__main__":
    extractor = CSXExtractorImpl()
    paper = extractor.extract_textual_data("../../test/resources/sample_tei.tei")
    print(json.dumps(paper.to_dict()))
