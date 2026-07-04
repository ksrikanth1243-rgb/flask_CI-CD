pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        VENV = "${WORKSPACE}/venv"
        APP_NAME = "flask_practice"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    python --version
                    pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . ${VENV}/bin/activate

                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                '''
            }
        }

        stage('Verify Application') {
            steps {
                sh '''
                    . ${VENV}/bin/activate

                    echo "Checking Python syntax..."

                    python -m py_compile app.py

                    echo "Syntax verification completed."
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV}/bin/activate

                    pip install pytest

                    if [ -d tests ]; then
                        pytest -v
                    else
                        echo "No tests directory found. Skipping tests."
                    fi
                '''
            }
        }

        stage('Package Application') {
            steps {
                sh '''
                    tar --exclude=venv \
                        --exclude=.git \
                        --exclude=__pycache__ \
                        -czf ${APP_NAME}-${BUILD_NUMBER}.tar.gz .

                    ls -lh ${APP_NAME}-${BUILD_NUMBER}.tar.gz
                '''
            }
        }
    }

    post {

        success {
            echo "Build completed successfully."
            archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
        }

        failure {
            echo "Build failed. Please check the console output."
        }

        always {
            echo "Pipeline execution finished."
        }
    }
}
