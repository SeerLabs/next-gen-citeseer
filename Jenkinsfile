node {
  stage 'Checkout'
  git branch: 'docker-containers', credentialsId: '5a706760-1e69-47c4-a7fd-34e96e61bb58', url: 'https://github.com/SeerLabs/next-gen-citeseer.git'

  stage 'build'
  docker.build('client')

  stage 'deploy'
  sh './deploy.sh'
}
