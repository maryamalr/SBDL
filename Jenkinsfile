pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
               bat 'C:\\Users\\marya\\AppData\\Roaming\\Python\\Python310\\Scripts\\pipenv.exe --python python sync'
            }
        }
        stage('Test') {
            steps {
               bat 'C:\\Users\\marya\\AppData\\Roaming\\Python\\Python310\\Scripts\\pipenv.exe run pytest'
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
        stage('Release') {
            when {
                branch 'release'
            }
            steps {
              bat "scp -i /home/prashant/cred/edge-node_key.pem -o 'StrictHostKeyChecking no' -r sbdl.zip log4j.properties sbdl_main.py sbdl_submit.bat conf prashant@40.117.123.105:/home/prashant/sbdl-qa"
            }
        }
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
               bat "scp -i /home/prashant/cred/edge-node_key.pem -o 'StrictHostKeyChecking no' -r sbdl.zip log4j.properties sbdl_main.py sbdl_submit.bat conf prashant@40.117.123.105:/home/prashant/sbdl-prod"
            }
        }
    }
}