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
		echo ''' *********************** \
			   CHECKOUT START \
		      	 ***********************
		'''
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: 'master']], 
                    doGenerateSubmoduleConfigurations: false, 
                    extensions: [[$class: 'CleanCheckout']], 
                    submoduleCfg: [], 
                    userRemoteConfigs: [[credentialsId: gitHubCredential,
                                         url: gitHubURL]]
                ])
		echo ''' *********************** \
                           CHECKOUT SUCCESS \
                         ***********************
                '''
            }
        }
	stage ('Attach Env Files') {
	    steps {
	        sh ''' sudo cp /home/dimak/course_attendance_app/.env /var/lib/jenkins/workspace/course_attendance_app_pipeline/		
	    	       sudo cp -r /home/dimak/course_attendance_app/env /var/lib/jenkins/workspace/course_attendance_app_pipeline/
		       sudo chmod 777 /var/lib/jenkins/workspace/course_attendance_app_pipeline/env
		'''
		}
	}
        stage ('Build Image') {
            steps {
		echo ''' ******************* \
                             BUILD START \
                         *******************
                '''
                script { 
                    dockerImage = docker.build(dockerHubRegistry + ":latest",
                    "-f ./Dockerfile-flask .")
                }
            }
        }
	stage ('Health Check') {
	   steps {
	       echo ''' ****************** \
                            TEST START \
                        ******************
               '''
	       sh ''' docker-compose up -d --build 
	              HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:5000/)
		      if [ $HTTP_STATUS -eq 200 ]; then
				echo ''' ******************** \
                           		     TEST SUCCESS \
                                         ********************
                     		'''
		      else
				exit 1
		      fi
	       '''
	   }
	}
        stage ('Deploy to DockerHub') {
            steps {
	       echo ''' ******************** \
                            DEPLOY START \
                        ********************
               '''
               script {
                    docker.withRegistry( '', dockerHubRegistryCredential ) {
                        dockerImage.push()
                    }
                }
		echo ''' ********************** \
                             DEPLOY SUCCESS \
                         **********************
                '''
            }
        }
        stage ('Clean Memory') {
            steps {
                sh ''' docker ps -aq | xargs docker rm -f
		       docker images -q | xargs docker rmi -f
		''' 
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
