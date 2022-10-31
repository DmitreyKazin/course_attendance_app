pipeline {
    
    agent any
    
    environment {
        dockerHubRegistry = 'dmitreykazin/course_attendance_app'
        dockerHubRegistryCredential = '99f93f2b-67ae-4bf9-9c2b-c5f02dab9cdd'
        dockerImage = ''
        gitHubCredential = '9c934149-1068-4763-8744-80e8ebafa24f'
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
	        sh ''' 		
	    	       cp -r /home/ec2-user/env_files/env /home/ec2-user/workspace/release-pipeline/
		       chmod 777 /home/ec2-user/workspace/release-pipeline/env
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
	       sh ''' docker-compose up -d --build 
	              HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:5000/)
		      if [ $HTTP_STATUS -eq 200 ]; then
				echo "TEST: SUCCESS"
		      else	
				echo "TEST: FAIL"
				exit 1
		      fi
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
