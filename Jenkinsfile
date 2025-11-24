pipeline {
    agent any

    environment {
        ACR_URL = "acrdevopsabdessamad.azurecr.io"
        ACR_CREDENTIALS_ID = "acr-credentials"
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
                //  PYTHON BACKEND
                // ----------------------------------------------------
                stage('Python: Test & Build') {
                    steps {
                        script {
                            dir('product-api') {
                
                                // Au lieu de faire "pip install", on demande à Docker de lancer l'étape de test définie dans le Dockerfile
                                echo "Lancement des tests (dans Docker)..."
                                sh "docker build --target tester ."
                                echo "✅ Tests Python validés !"

                                // Ensuite on construit l'image finale
                                echo "Construction de l'image finale..."
                                sh "docker build --target production -t ${ACR_URL}/product-api:${DOCKER_TAG} ."
                            }
                        }
                    }
                }

                // ----------------------------------------------------
                // NODE BACKEND
                // ----------------------------------------------------
                stage('Node: Test & Build') {
                    steps {
                        script {
                            dir('order-api') {
                               
                                echo "Lancement des tests (dans Docker)..."
                                sh "docker build --target tester ."
                                echo "✅ Tests Node.js validés !"

                                echo "Construction de l'image finale..."
                                sh "docker build --target production -t ${ACR_URL}/order-api:${DOCKER_TAG} ."
                            }
                        }
                    }
                }

                // ----------------------------------------------------
                //  REACT FRONTEND
                // ----------------------------------------------------
                stage('⚛️ React: Test & Build') {
                    steps {
                        script {
                            dir('frontend') {
                                // Pour le front, on build simplement l'image
                                echo " Construction et Vérification React..."
                                sh "docker build -t ${ACR_URL}/frontend-app:${DOCKER_TAG} ."
                            }
                        }
                    }
                }
            }
        }

        //  SCAN DE SÉCURITÉ
        stage(' Security Scan (Trivy)') {
             parallel {
                stage('Scan Python') { steps { scanImage("product-api") } }
                stage('Scan Node') { steps { scanImage("order-api") } }
                stage('Scan Front') { steps { scanImage("frontend-app") } }
            }
        }

        //  PUSH (Uniquement sur MAIN)
        stage(' Push to Registry') {
            when { branch 'main' }
            steps {
                script {
                    echo "✅ Branche Main : Push vers Azure..."
                    pushImage("product-api")
                    pushImage("order-api")
                    pushImage("frontend-app")
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "🧹 Nettoyage..."
                sh "docker rmi ${ACR_URL}/product-api:${DOCKER_TAG} || true"
                sh "docker rmi ${ACR_URL}/order-api:${DOCKER_TAG} || true"
                sh "docker rmi ${ACR_URL}/frontend-app:${DOCKER_TAG} || true"
                sh "docker image prune -f || true" 
            }
        }
    }
}

// --- FONCTIONS UTILITAIRES ---

def scanImage(String imageName) {
    echo "🔍 Scanning ${imageName}..."
    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy image --severity CRITICAL --no-progress --exit-code 0 \
        ${ACR_URL}/${imageName}:${DOCKER_TAG}"
}

def pushImage(String imageName) {
    withCredentials([usernamePassword(credentialsId: env.ACR_CREDENTIALS_ID, passwordVariable: 'ACR_PASS', usernameVariable: 'ACR_USER')]) {
        // Attention aux guillemets ici, j'ai corrigé la syntaxe du login aussi
        sh """echo "$ACR_PASS" | docker login ${ACR_URL} -u "${ACR_USER}" --password-stdin"""
        sh "docker push ${ACR_URL}/${imageName}:${DOCKER_TAG}"
    }
}
