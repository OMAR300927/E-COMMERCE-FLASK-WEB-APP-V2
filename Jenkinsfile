pipeline {
    agent any
    
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        USERNAME = 'omarsa999'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/OMAR300927/E-COMMERCE-FLASK-WEB-APP-V2.git'
            }
        }
        
        stage('Gitleaks scan') {
            steps {
                sh 'gitleaks detect --source ./myapp --exit-code 1'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                    $SCANNER_HOME/bin/sonar-scanner \
                    -Dsonar.projectName=e-commerce-app \
                    -Dsonar.projectKey=e-commerce-app \
                    '''
                }
            }
        }
        
        stage('Quality gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false, credentialsId: 'sonar-cred'
                }
            }
        }
        
        stage('File system scan') {
            steps {
                sh 'trivy fs . --format table -o fs-report.html'
            }
        }
        
        stage('Build & tag the image') {
            steps {
                sh 'docker build -t $USERNAME/e-commerce-app:v2.0 -f myapp/Dockerfile .'
            }
        }
        
        stage('Scan the image') {
            steps {
                sh 'trivy image --timeout 10m --format table -o image-report.html $USERNAME/e-commerce-app:v2.0'
            }
        }
        
        stage('Push the image') {
            steps {
                withDockerRegistry(credentialsId: 'docker-cred', url: 'https://index.docker.io/v1/') {
                    sh 'docker push $USERNAME/e-commerce-app:v2.0'
                }
            }
        }

        stage('Apply Kubernetes manifests') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh 'kubectl apply -f ./K8s/'
                    sh 'kubectl rollout status deployment/flask-deployment'
                }
            }
        }

        stage('Verify the Deployment') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh 'kubectl get pods -o wide'
                }
            }
        }
    }
}