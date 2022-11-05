pipeline {
    
    agent {
	label 'Linux2'
    }
    
    environment {
        dockerHubRegistry = 'dmitreykazin/course_attendance_app'
        dockerHubRegistryCredential = '99f93f2b-67ae-4bf9-9c2b-c5f02dab9cdd'
        dockerLatestImage = ''
	dockerTagImage = ''
        gitHubCredential = '9c934149-1068-4763-8744-80e8ebafa24f'
        gitHubURL = 'https://github.com/DmitreyKazin/course_attendance_app.git'
    }
    
    stages {
        stage ('Git Checkout') {
            steps {
	        println """ 
                      ********************************************************
                                            JOB START

                      JOB: ${JOB_NAME}
                      RUNNING ON: ${NODE_NAME}
                      EXECUTER: ${EXECUTOR_NUMBER}
                      ********************************************************
                """.stripIndent()
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
	        sh ''' cp /home/ec2-user/workspace/env_files/.env /home/ec2-user/workspace/release-pipeline/		
	    	       cp -r /home/ec2-user/workspace/env_files/env /home/ec2-user/workspace/release-pipeline/
		'''
		}
	}
        stage ('Build Images') {
	    println """
                    ********************************************************
                                           BUILD START

                    BUILD TAG: ${BUILD_TAG}
                    ********************************************************
                """.stripIndent()

            steps {
		echo "BUILD START: ${BUILD_TAG}"
                script { 
                    dockerLatestImage = docker.build(dockerHubRegistry + ":latest",
                    "-f ./Dockerfile-flask .")
		    dockerTagImage = docker.build(dockerHubRegistry + ":${BUILD_NUMBER}",
		    "-f ./Dockerfile-flask .")
                }
            }
        }
	stage ('Health Check') {
	   steps {
	       sh ''' docker-compose up -d --build 
		      sleep 15
	              HTTP_STATUS=`curl -o /dev/null -s -w "%{http_code}\n" http://localhost:5000/`
		      docker-compose down 
		      if [ $HTTP_STATUS -eq 200 ];
		      then
		      		echo "TEST: SUCCES"
		      else
				echo "TEST: FAIL"
				exit 1
		      fi
		     
	       '''
	   }
	}
        stage ('Push to DockerHub') {
            steps {
               script {
                    docker.withRegistry( '', dockerHubRegistryCredential ) {
                        dockerLatestImage.push()
			dockerTagImage.push()
                    }
                }
		println  """ 
		         ******************************************************
                         BUILD SUCCES: ${env.BUILD_TAG}
			 ****************************************************
		""".stripIndent()
            }
        }
	stage ('Deploy to Production') {
	    steps {
	    	sh './deploy.sh'
            }
	}
    }
    
    post {
        always {
	    println """
                    ********************************************************
                    JOB ${currentBuild.currentResult}
		    MORE DETAILS: ${env.BUILD_URL}
                    ********************************************************
            """.stripIndent()
            emailext to: "kazindmitrey@gmail.com",
                     subject: "Jenkins build: ${currentBuild.currentResult}: ${env.JOB_NAME}",
                     body: "${currentBuild.currentResult}: Job ${env.JOB_NAME}\nMore Info can be found here: ${env.BUILD_URL}"
        }
    }
}
