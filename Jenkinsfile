pipeline {
    
    agent any
    
    environment {
	workspace_path = '/var/lib/jenkins/workspace/course_attendance_app_pipeline'
        dockerHubRegistry = 'dmitreykazin/course_attendance_app'
        dockerHubRegistryCredential = '3e0b51f4-078c-45be-aae6-46b7b853a4d1'
        dockerImage = ''
        gitHubCredential = 'a0bb4e47-f112-4b84-9e36-1fb1d2239d7e'
        gitHubURL = 'https://github.com/DmitreyKazin/course_attendance_app.git'
    }
    
    stages {
        stage ('Git Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: 'master']], 
                    doGenerateSubmoduleConfigurations: false, 
                    extensions: [[$class: 'CleanCheckout']], 
                    submoduleCfg: [], 
                    userRemoteConfigs: [[credentialsId: gitHubCredential,
                                         url: gitHubURL]]
                ])
            }
        }
	stage ('Attach Env') {
	    steps {
		sh ''' sudo cp /home/dimak/course_attendance_app/.env workspace_path		
	    	       sudo cp -r /home/dimak/course_attendance_app/env workspace_path
		'''
		}
	}
        stage ('Build Image') {
            steps {
                script { 
                    dockerImage = docker.build(dockerHubRegistry + ":latest",
                    "-f ./Dockerfile-flask .")
                }
            }
        }
        stage ('Deploy to DockerHub') {
            steps {
               script {
                    docker.withRegistry( '', dockerHubRegistryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage ('Clean Memory') {
            steps {
                sh "docker rmi $dockerHubRegistry:latest"
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
