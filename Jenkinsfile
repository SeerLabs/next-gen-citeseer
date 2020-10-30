node {
  stage 'build'
  docker.build('server')
  docker.build('client')

  stage 'deploy'
  sh './deploy.sh'
}
