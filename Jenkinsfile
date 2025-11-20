pipeline {
    agent any
    triggers {
        cron('H/15 * * * 4-6') // Runs every 15 minutes on Thu-Fri-Sat
    }

    stages {

        stage('Setup Python Env') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Check Chapter') {
            steps {
                withCredentials([string(credentialsId: 'gmail-creds', variable: 'smtp_pass')]) {
                    bat '''
                    call venv\\Scripts\\activate
                    set smtp_pass=%smtp_pass%
                    python chapter_search.py
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline finished successfully."
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
