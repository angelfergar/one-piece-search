pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                bat 'venv\\Scripts\\activate && python script.py > result.txt'
            }
        }

        stage('Notify if New Chapter') {
            steps {
                script {
                    def content = readFile('result.txt')
                    if (content.contains('NEW_CHAPTER_FOUND')) {
                        emailext(
                            subject: "New One Piece Chapter Available!",
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
