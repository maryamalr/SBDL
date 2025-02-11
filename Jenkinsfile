pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
               bat 'python -m pipenv --python python sync'
            }
        }
        stage('Test') {
            steps {
               bat 'python -m pipenv run pytest'
            }
        }
        stage('Package') {
            when {
                anyOf { branch "master"; branch 'release' }
            }
            steps {
               bat 'zip -r sbdl.zip lib'
            }
        }
    }
}
