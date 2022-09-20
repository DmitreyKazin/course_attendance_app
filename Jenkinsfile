pipeline {
    environment {
        registry = 'dmitreykazin/course_attendance_app'
        registryCredential = '3e0b51f4-078c-45be-aae6-46b7b853a4d1'
        dockerImage = ''
    }
    agent any
    stages {
        stage ('Clone') {
            steps {
                git 'https://github.com/DmitreyKazin/course_attendance_app.git'
            }
        }
        stage ('Build') {
            steps {
                script { 
                    dockerImage = docker.build(registry + ":latest",
                    "-f ./Dockerfile-flask .")
                }
            }
        }
        stage ('Push') {
            steps {
               script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage ('Clean') {
            steps {
                sh "docker rmi $registry:latest"
            }
        }
    }
}
