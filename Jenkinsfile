pipeline {
    agent any
    triggers {
        cron('H/15 * * * 4-6') // Runs every 15 minutes on Thu-Fri-Sat
    }

    stages {

        stage('Install GeckoDriver') {
            steps {
                powershell '''
                # Download GeckoDriver 0.36.0 if not already present
                if (!(Test-Path "gecko\\geckodriver.exe")) {
                    Write-Host "Downloading GeckoDriver 0.36.0..."
                    Invoke-WebRequest `
                        https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-win64.zip `
                        -OutFile gecko.zip

                    Expand-Archive gecko.zip -DestinationPath gecko -Force
                }

                Write-Host "GeckoDriver downloaded and unpacked."
                '''
                script {
                    // Prepend the new GeckoDriver to PATH
                    env.PATH = "${pwd()}\\gecko;${env.PATH}"
                }
            }
        }

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
