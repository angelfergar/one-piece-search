pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                // Create virtual environment and install dependencies
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                // Run your script and save output
                bat 'venv\\Scripts\\activate && python chapter_search.py > result.txt'
            }
        }

        stage('Notify if New Chapter') {
            steps {
                script {
                    def current = readFile('result.txt').trim()
                    def previous = fileExists('result_prev.txt') ? readFile('result_prev.txt').trim() : ''

                    // Only send email if there is something new
                    if (current && current != previous) {
                        try {
                            emailext(
                                subject: "New One Piece Chapter Available!",
                                body: current,
                                to: 'anfernagar@gmail.com',
                                mimeType: 'text/plain',
                                replyTo: 'anfernagar@gmail.com',
                                from: 'anfernagar@gmail.com'
                            )
                            echo "Email sent successfully."
                            // Save this as the previous result
                            writeFile file: 'result_prev.txt', text: current
                        } catch (Exception e) {
                            echo "Failed to send email: ${e}"
                        }
                    } else {
                        echo "No new chapters found since last check."
                    }
                }
            }
        }
    }

    post {
        always {
            // Archive the current and previous results for reference
            archiveArtifacts artifacts: 'result.txt, result_prev.txt', onlyIfSuccessful: true
        }
    }
}
