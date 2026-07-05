pipeline {

    agent any

    stages {

        stage('Checkout') {

            steps {

                git branch: 'main',
                url: 'https://github.com/ksrikanth1243-rgb/flask_CI-CD.git'

            }

        }

        stage('Build') {

            steps {

                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'

            }

        }

        stage('Test') {

            steps {

                sh '. venv/bin/activate && pytest --junitxml=test-results.xml'

            }

        }

       stage('Code Quality & Security') {
            
        steps {
          sh '''
                 . venv/bin/activate
                   black --check .
                   bandit -r app.py
              '''
         }
       }


        stage('Deploy') {

            steps {

                echo 'Deploying to staging...'
            }

        }

    }

    post {

        success {

            emailext(
                subject: 'Build Successful',
                body: 'Pipeline completed successfully.',
                to: 'team@example.com'
            )

        }

        failure {

            emailext(
                subject: 'Build Failed',
                body: 'Pipeline execution failed.',
                to: 'team@example.com'
            )

        }

    }

}
