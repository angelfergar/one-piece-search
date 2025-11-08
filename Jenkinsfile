pipeline {
    agent any
    stages {
        stage('Check Chapter') {
            steps {
                script {
                    // Restore previous chapter.txt if it exists
                    if (fileExists('chapter.txt')) {
                        unstash 'chapter-txt'
                    }
                }

                // Use credentials stored in Jenkins
                withCredentials([string(credentialsId: 'gmail-creds', variable: 'smtp_pass')]) {
                    bat 'set smtp_pass=%smtp_pass% && call venv\\Scripts\\activate && python chapter_search.py'
                }

                // Save updated chapter.txt for next build
                stash includes: 'chapter.txt', name: 'chapter-txt', allowEmpty: true
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
