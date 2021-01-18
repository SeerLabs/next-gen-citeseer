<template>
    <v-row id="doc-view-header">
        <v-col cols="9">
            <h2>{{ title }}</h2>
            <h5>{{ authors.join(', ') }}</h5>
            <h5>{{ venue }} - {{ year }}</h5>
            <br />

            <div
                id="abstract"
                :style="
                    showAbstract
                        ? { height: 'min-content' }
                        : { maxHeight: '150px' }
                "
            >
                <p>{{ abstract }}</p>
            </div>
            <v-btn @click="() => (showAbstract = !showAbstract)">
                {{ !showAbstract ? 'Show more' : 'Show less' }}
            </v-btn>
        </v-col>
        <v-col cols="3">
            <v-card v-if="!loading" id="document-options">
                <v-card-text class="d-flex flex-column mb-6">
                    <!-- PDF Button -->
                    <v-btn
                        id="pdf-btn"
                        squared
                        :href="getPDFUrl"
                        target="_blank"
                        class="mv-md-2"
                    >
                        View PDF
                    </v-btn>

                    <v-btn @click="toggleMoniterPaper">
                      {{ monitered ? "Unmoniter Paper" : "Moniter Paper" }}
                    </v-btn>

                    <v-btn @click="toggleLikePaper">
                      {{ liked ? "Unlike Paper" : "Like Paper" }}
                    </v-btn>

                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
import { mapState } from 'vuex'
import authService from '~/api/AuthService'

export default {
    props: {
        docId: { type: String, default: '' },
        title: { type: String, default: '' },
        authors: { type: Array, default: null },
        venue: { type: String, default: '' },
        year: { type: String, default: '' },
        nCitation: { type: Number, default: 0 },
        abstract: { type: String, default: '' }
    },
    data() {
        return {
            showAbstract: false,
            liked: false,
            monitered: false,
            loading: true
        };
    },
    computed: {
        ...mapState(['auth']),

        getPDFUrl() {
            return '/pdf/' + this.$route.params.id;
        }
    },
    beforeMount() {
      if (this.auth.loggedIn) {
        authService.getUserProfile(this.auth.token)
        .then((response) => {
          const profile = response.data;
          this.liked = profile.liked_papers.includes(this.$route.params.id)
          this.monitered = profile.monitered_papers.includes(this.$route.params.id)
          this.loading = false;
        })
      }
      else {
        this.liked = false;
        this.monitered = false;

        this.loading = false;
      }
    },
    methods: {
        toggleReadMore() {
            this.showAbstract = !this.showAbstract;
        },

        toggleLikePaper() {
          if (!this.liked) {
            authService.addLikedPaper(this.auth.token, this.$route.params.id)
          }
          else {
            authService.deleteLikedPaper(this.auth.token, this.$route.params.id)
          }
          this.liked = !this.liked
        },

        toggleMoniterPaper() {
          if (!this.monitered) {
            authService.addMoniteredPaper(this.auth.token, this.$route.params.id)
          }
          else {
            authService.deleteMoniteredPaper(this.auth.token, this.$route.params.id)
          }
          this.monitered = !this.monitered
        }
    }
};
</script>

<style>
#doc-view-layout {
    background: rgb(255, 255, 255);
}

#doc-view-header {
    margin-bottom: 3em;
    background: #ffffff;
}

#abstract {
    overflow: hidden;
}

#summary-text {
    padding-top: 2%;
    padding-bottom: 2%;
}

.citation-card {
    margin-bottom: 1em;
}

#pdf-btn {
    background: rgb(235, 0, 0);
    color: white;
    margin-bottom: 1em;
    outline: transparent;
    border-color: transparent;
}
</style>
