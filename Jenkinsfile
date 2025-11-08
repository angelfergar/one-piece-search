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
                bat 'venv\\Scripts\\activate && python chapter_search.py > result.txt'
            }
        }

        stage('Notify if New Chapter') {
            steps {
                script {
                    def content = readFile('result.txt')
                    if (content.contains('IS ALREADY OUT')) {
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
