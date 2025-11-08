pipeline {
    agent any
    stages {
        stage('Check Chapter') {
            steps {
                // Use credentials for email
                withCredentials([string(credentialsId: 'gmail-creds', variable: 'smtp_pass')]) {
                    bat 'set smtp_pass=%smtp_pass% && call venv\\Scripts\\activate && python chapter_search.py'
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
