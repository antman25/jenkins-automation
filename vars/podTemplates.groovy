def pythonTemplate(Closure body) {
  podTemplate(
    containers: [
      containerTemplate(
        name: 'python',
        image: 'python:latest',
        command: 'cat',
        ttyEnabled: true
      )
    ]
  ) {
    body()
  }
}

def gradleTemplate(Closure body) {
  podTemplate(
      containers: [
        containerTemplate(
                name: 'gradle',
                image: 'gradle:7.4.2-jdk17-alpine',
                command: 'cat',
                ttyEnabled: true
        )
      ]
  ) {
    body()
  }
}



