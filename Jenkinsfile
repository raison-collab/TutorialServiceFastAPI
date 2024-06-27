pipeline {
   agent any

   environment {
       FAST_API_SERVICE_CONTAINER = "fast-api-container"
   }

   stages {
       stage('Build') {
           steps {
               script {
                   docker.build(FAST_API_SERVICE)
               }
           }
       }

//        stage('Test') {
//            steps {
//                script {
//                    docker.image(FAST_API_SERVICE).inside {
//                        sh 'pytest'
//                    }
//                }
//            }
//        }

       stage('Deploy') {
           steps {
               script {
                   docker.image(FAST_API_SERVICE).push()
               }
           }
       }
   }

   post {
       always {
           cleanWs()
       }
   }
}