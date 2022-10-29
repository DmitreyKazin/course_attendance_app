pipeline {
    
    agent any
    
    environment {
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
	stage ('Attach Env Files') {
	    steps {
	        sh ''' sudo cp /home/dimak/course_attendance_app/.env /var/lib/jenkins/workspace/course_attendance_app_pipeline/		
	    	       sudo cp -r /home/dimak/course_attendance_app/env /var/lib/jenkins/workspace/course_attendance_app_pipeline/
		       sudo chmod 777 /var/lib/jenkins/workspace/course_attendance_app/env
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
	stage ('Health Check') {
	   steps {
	       sh ''' docker-compose up --build 
	              curl --fail http://localhost:5000/ || exit 1
	       '''
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
