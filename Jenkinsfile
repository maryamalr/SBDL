pipeline {
    agent any
    environment {
        HADOOP_HOME = 'C:\\Users\\marya\\Documents\\hadoop-3.3.6'
    }
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
