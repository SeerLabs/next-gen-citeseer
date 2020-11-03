node {
  stage 'Checkout'
  git branch: 'docker-containers', credentialsId: '5a706760-1e69-47c4-a7fd-34e96e61bb58', url: 'git@github.com:SeerLabs/next-gen-citeseer.git'

  stage 'build'
  docker.build('server')

  stage 'deploy'
  sh './deploy.sh'
}
