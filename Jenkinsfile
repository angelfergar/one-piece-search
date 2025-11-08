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
                    def content = readFile('result.txt')
                    if (content.contains('NEW_CHAPTER_FOUND')) {
                        emailext(
                            subject: 'New One Piece Chapter Available!',
                            body: content,
                            to: 'anfernagar@gmail.com'
                        )
                    } else {
                        echo 'No new chapters found.'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'result.txt', onlyIfSuccessful: true
        }
    }
}
