pipeline {
    agent any
    stages {
        stage('Check Chapter') {
            steps {
               // Restore previous chapter.txt
                copyArtifacts(projectName: currentBuild.projectName, filter: 'chapter.txt', optional: true)

                // USe credentials in Jenkins
                withCredentials([string(credentialsId: 'gmail-creds', variable: 'smtp_pass')]) {
                bat 'set smtp_pass=%smtp_pass% && call venv\\Scripts\\activate && python chapter_search.py'
                }

                // Archive updated chapter.txt
                archiveArtifacts artifacts: 'chapter.txt', fingerprint: true
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
