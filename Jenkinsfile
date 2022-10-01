pipeline {
    agent any
    environment {
        registry = 'dmitreykazin/course_attendance_app'
        registryCredential = '3e0b51f4-078c-45be-aae6-46b7b853a4d1'
        dockerImage = ''
    }
    stages {
        stage ('Clone Git') {
            steps {
                git 'https://github.com/DmitreyKazin/course_attendance_app.git'
            }
        }
        stage ('Build Image') {
            steps {
                script { 
                    dockerImage = docker.build(registry + ":latest",
                    "-f ./Dockerfile-flask .")
                }
            }
        }
        stage ('Deploy to DockerHub') {
            steps {
               script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage ('Clean Memory') {
            steps {
                sh "docker rmi $registry:latest"
            }
        }
    }
    post {
        always {
            emailext to: "kazindmitrey@gmail.com",
                     subject: "Jenkins build: ${currentBuild.currentResult}: ${env.JOB_NAME}",
                     body: "${currentBuild.currentResult}: Job ${env.JOB_NAME}\nMore Info can be found here: ${env.BUILD_URL}"
        }
    }
}
