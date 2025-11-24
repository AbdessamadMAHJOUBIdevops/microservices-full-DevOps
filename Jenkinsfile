pipeline {
    agent any

    environment {
        ACR_URL = "acrdevopsabdessamad.azurecr.io"
        ACR_CREDENTIALS_ID = "acr-credentials"
        // On remplace les slashs par des tirets pour éviter les erreurs Docker
        SAFE_BRANCH_NAME = "${env.BRANCH_NAME.replaceAll('/', '-')}"
        DOCKER_TAG = "${SAFE_BRANCH_NAME}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "🚀 Démarrage du pipeline pour la branche : ${env.BRANCH_NAME}"
            }
        }

        stage('Test & Build Microservices') {
            parallel {
                // ----------------------------------------------------
                //  PYTHON BACKEND (Product API)
                // ----------------------------------------------------
                stage('Python: Test & Build') {
                    steps {
                        script {
                            dir('product-api') {
                                
                                echo "🧪 Lancement des tests unitaires Python..."
                                sh "pip install pytest && pytest"
                                sh "echo 'Tests Python passés avec succès ✅'"

                                // 2. Build de l'image
                                buildDockerImage("product-api")
                            }
                        }
                    }
                }

                // ----------------------------------------------------
                //  NODE BACKEND (Order API)
                // ----------------------------------------------------
                stage(' Node: Test & Build') {
                    steps {
                        script {
                            dir('order-api') {
                                
                                echo "🧪 Lancement des tests unitaires Node.js..."
                                sh "npm install && npm test"
                                sh "echo 'Tests Node.js passés avec succès ✅'"

                                // 2. Build de l'image
                                buildDockerImage("order-api")
                            }
                        }
                    }
                }

                // ----------------------------------------------------
                //  REACT FRONTEND
                // ----------------------------------------------------
                stage('React: Test & Build') {
                    steps {
                        script {
                            dir('frontend') {
                                
                                echo "🧪 Lancement des tests unitaires React..."
                                // Note : Pour React, il faut souvent mettre CI=true
                                sh "npm install && CI=true npm test"
                                sh "echo 'Tests Frontend passés avec succès ✅'"

                                // 2. Build de l'image (Nginx)
                                buildDockerImage("frontend-app")
                            }
                        }
                    }
                }
            }
        }

        // SCAN DE SÉCURITÉ (DevSecOps)
        // On le fait après le build pour scanner l'image créée
        stage('Security Scan (Trivy)') {
        
                parallel {
                    stage('Scan Python') { steps { scanImage("product-api") } }
                    stage('Scan Node') { steps { scanImage("order-api") } }
                    stage('Scan Front') { steps { scanImage("frontend-app") } }
                }
            
        }

        // PUSH (Uniquement sur MAIN)
        stage('Push to Registry') {
            when {
                branch 'main'  
            }
            steps {
                script {
                    echo " Branche Main détectée : Push vers Azure ACR..."
                    pushImage("product-api")
                    pushImage("order-api")
                    pushImage("frontend-app")
                }
            }
        }
    }
    
    post {
        always {
            // Nettoyage des images locales pour ne pas saturer le disque Jenkins
            script {
                echo "Nettoyage du workspace..."
                sh "docker rmi ${ACR_URL}/product-api:${DOCKER_TAG} || true"
                sh "docker rmi ${ACR_URL}/order-api:${DOCKER_TAG} || true"
                sh "docker rmi ${ACR_URL}/frontend-app:${DOCKER_TAG} || true"
            }
        }
    }
}

// --- FONCTIONS UTILITAIRES (DRY - Don't Repeat Yourself) ---

def buildDockerImage(String imageName) {
    echo "Building ${imageName}..."
    sh "docker build -t ${ACR_URL}/${imageName}:${DOCKER_TAG} ."
}

def scanImage(String imageName) {
    echo "Scanning ${imageName}..."
    // --exit-code 0 permet de ne pas bloquer le build si faille trouvée (just pour tester)
    // En prod, on met --exit-code 1 pour bloquer.
    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy image --severity CRITICAL --no-progress --exit-code 1 \
        ${ACR_URL}/${imageName}:${DOCKER_TAG}"
}

def pushImage(String imageName) {
    withCredentials([usernamePassword(credentialsId: env.ACR_CREDENTIALS_ID, passwordVariable: 'ACR_PASS', usernameVariable: 'ACR_USER')]) {
        sh "echo "$ACR_PASS" | docker login  ${ACR_URL} -u ${ACR_USER} --password-stdin "
        sh "docker push ${ACR_URL}/${imageName}:${DOCKER_TAG}"
    }
}