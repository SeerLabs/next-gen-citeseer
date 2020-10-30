node {
  stage 'Checkout'
  git url: 'https://github.com/SeerLabs/next-gen-citeseer.git'

  stage 'build'
  docker.build('server')
  docker.build('client')

  stage 'deploy'
  sh './deploy.sh'
}
