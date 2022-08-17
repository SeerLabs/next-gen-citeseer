<template>
	<v-footer height="200" dark>
		<v-container>
			<v-row>
				<v-col md="3">
					<img src="@/assets/img/ist_logo.svg" alt="Penn State IST"/>
				</v-col>
				<v-col md="1" class="mr-15">
					<h5>Information</h5>
						<ul class="pa-0">
							<li v-for='i in information' :key='i.id' class="link-list">
								<a :alt="i.title" :href="i.link" target="_blank">
									{{ i.title }}
								</a>
							</li>
						</ul>
				</v-col>
				<v-col md="3">
					<h5>Services</h5>
						<ul class="pa-0">
							<li v-for='i in services' :key='i.id' class="link-list">
								<a  :alt="i.title" :href="i.link" target="_blank">
									{{ i.title }}
								</a>
							</li>
						</ul>
				</v-col>
				<v-col md="3">
					<h5>About</h5>
					<p>CiteSeer<sup>X</sup> is an evolving scientific literature digital library and search engine.</p>
					<p id="copyright">@2007-{{ new Date().getFullYear() }} The Pennsylvania State University</p>
				</v-col>
			</v-row>
		</v-container>
	</v-footer>
</template>

<script>

export default {
	data() {
		return {
			information: [
				{
					title: "About CiteSeerX",
					link: "https://csxstatic.ist.psu.edu/home",
				},
				{
					title: "Privacy Policy",
					link: "http://csxstatic.ist.psu.edu/privacy-policy",
				},
				{
					title: "Data",
					link: "http://csxstatic.ist.psu.edu/downloads/data",
				},
			],
			services: [
				{
					title: "Submit Documents",
					link: "http://csxcrawlweb01.ist.psu.edu/submit_pub/",
				},
				{
					title: "Help",
					link: "https://csxstatic.ist.psu.edu/help/",
				},
				{
					title: "Contact Us",
					link: "http://csxstatic.ist.psu.edu/contact",
				}
			]
		}
	}
}

</script>


<style scoped>
.link-list {
	list-style: none;
	list-style-type: none;
}

a {
	color: #fff;
}

#copyright {
	opacity: 0.5;
}
</style>
