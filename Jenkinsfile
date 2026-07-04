pipeline {
    agent any
    
    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_DIR = "${WORKSPACE}/venv"
        APP_NAME = 'flask_practice'
        STAGING_SERVER = credentials('staging-server-credentials')
        STAGING_PATH = '/opt/flask_practice'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo '=== CHECKOUT STAGE ==='
                    checkout scm
                    echo "Repository cloned successfully"
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    echo '=== SETUP ENVIRONMENT STAGE ==='
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        echo "Virtual environment created and pip upgraded"
                    '''
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    echo '=== BUILD STAGE ==='
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pip install -r requirements.txt
                        echo "Dependencies installed successfully"
                        pip list
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo '=== TEST STAGE ==='
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pip install pytest pytest-cov
                        pytest tests/ -v --cov=. --cov-report=xml --cov-report=html
                        echo "Tests completed"
                    '''
                }
            }
            
	post {
              always {
                  script {
                    if (fileExists('test-results.xml')) {
                         junit 'test-results.xml'
            }

            if (fileExists('htmlcov/index.html')) {
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }
    }
}
        
        stage('Code Quality') {
            steps {
                script {
                    echo '=== CODE QUALITY STAGE ==='
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pip install pylint flake8
                        flake8 app/ tests/ --max-line-length=120 --exit-zero --format=json > flake8-report.json || true
                        pylint app/ --exit-zero > pylint-report.txt || true
                        echo "Code quality checks completed"
                    '''
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    echo '=== DEPLOY TO STAGING STAGE ==='
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        echo "Building application artifacts..."
                        tar -czf ${APP_NAME}-${BUILD_NUMBER}.tar.gz --exclude=venv --exclude=.git --exclude=__pycache__ .
                        echo "Application packaged: ${APP_NAME}-${BUILD_NUMBER}.tar.gz"
                        ls -lh ${APP_NAME}-${BUILD_NUMBER}.tar.gz
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo '=== VERIFY DEPLOYMENT STAGE ==='
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        python -m py_compile app/*.py
                        echo "Application syntax verified"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo '=== CLEANUP ==='
                cleanWs(deleteDirs: true, patterns: [[pattern: '**/.pytest_cache', type: 'INCLUDE']])
            }
        }
        
        success {
            script {
                echo '=== BUILD SUCCESSFUL ==='
                emailext (
                    subject: "Jenkins Build SUCCESS: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: '''
                        Build Status: SUCCESS
                        
                        Job Name: ${JOB_NAME}
                        Build Number: ${BUILD_NUMBER}
                        Build URL: ${BUILD_URL}
                        Branch: ${GIT_BRANCH}
                        Commit: ${GIT_COMMIT}
                        
                        The build and tests completed successfully.
                        The application is ready for deployment to staging.
                    ''',
                    to: '${DEFAULT_RECIPIENTS}',
                    recipientProviders: [developers(), requestor(), brokenBuildSuspects()]
                )
            }
        }
        
        failure {
            script {
                echo '=== BUILD FAILED ==='
                emailext (
                    subject: "Jenkins Build FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: '''
                        Build Status: FAILED
                        
                        Job Name: ${JOB_NAME}
                        Build Number: ${BUILD_NUMBER}
                        Build URL: ${BUILD_URL}
                        Branch: ${GIT_BRANCH}
                        Commit: ${GIT_COMMIT}
                        
                        Please review the build logs at: ${BUILD_URL}
                        
                        Common issues:
                        - Missing dependencies in requirements.txt
                        - Test failures in pytest suite
                        - Code quality violations
                        - Python syntax errors
                    ''',
                    to: '${DEFAULT_RECIPIENTS}',
                    recipientProviders: [developers(), requestor(), brokenBuildSuspects()]
                )
            }
        }
        
        unstable {
            script {
                echo '=== BUILD UNSTABLE ==='
                emailext (
                    subject: "Jenkins Build UNSTABLE: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: '''
                        Build Status: UNSTABLE
                        
                        Job Name: ${JOB_NAME}
                        Build Number: ${BUILD_NUMBER}
                        Build URL: ${BUILD_URL}
                        
                        Some tests or quality checks passed with warnings.
                        Please review the detailed logs.
                    ''',
                    to: '${DEFAULT_RECIPIENTS}',
                    recipientProviders: [developers(), requestor()]
                )
            }
        }
    }
}
