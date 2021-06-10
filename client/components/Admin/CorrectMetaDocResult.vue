<template>
    <div class="document-results-list">
        <ul>
            <li v-for="(item, index) in papers" :key="index">
                 <v-container fluid class="document-results-item">
                    <metadata-diff-dialog
                    :paper="item"
                    :meta-request="metadataRequests[index]"
                    >
                    </metadata-diff-dialog>

                </v-container>
                
            </li>
        </ul>
    </div>
</template>

<script>
// import DocViewService from '~/api/DocViewService'
import MetadataDiffDialog from '~/components/Admin/MetadataDiffDialog'
export default {
    name: 'CorrectMetaDocResult',
    components: {
        MetadataDiffDialog
    },
    props: {
        metadataRequests: { type: Array, default: null },
        papers: { type: Array, default: null }
    },
    data () {
      return {
        dialog: false,
        notifications: false,
        sound: true,
        widgets: false,

      }
    },
    async beforeMount() {
        
    }
    // computed: {
    //     docUrl() {
    //         return `/doc_view/pid/${this.docId}`;
    //     },

    //     pdfUrl() {
    //         return '/pdf/' + this.docId;
    //     }
    // }
};
</script>

<style scoped>
.document-results-list {
    margin: 1.5em 0 1em 0;
    padding: 0;
}

.document-results-list ul {
    list-style: none;
    padding-left: 0;
}

.document-results-item {
    margin: 0.5em 0;
    background-color: white;
    padding: 1rem;
}

.result-type {
    text-align: right;
    font-weight: 600;
}

.result-info {
    margin-bottom: 0.5em;
}

.result-content {
    margin-bottom: 0.3em;
}

.links {
    text-align: right;
}

.links a {
    margin-left: 1em;
}
</style>