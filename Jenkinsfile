pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                sh '. venv/bin/activate && python3 script.py > result.txt'
            }
        }

        stage('Notify if New Chapter') {
            steps {
                script {
                    def current = readFile('result.txt')
                    def previous = fileExists('result_prev.txt') ? readFile('result_prev.txt') : ''

                    // Only send email if something new appeared
                    if (current != previous) {
                        emailext(
                            subject: 'New One Piece Chapter Available!',
                            body: current,
                            to: 'anfernagar@gmail.com'
                        )
                        // Save this as last result
                        writeFile file: 'result_prev.txt', text: current
                    } else {
                        echo 'New chapter is not available yet.'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'result.txt, result_prev.txt', onlyIfSuccessful: true
        }
    }
