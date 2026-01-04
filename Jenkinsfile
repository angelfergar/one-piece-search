pipeline {
    agent {
        label 'op-search'  
    }

    triggers {
        cron('H/15 * * * 4-6')
    }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        stage('Prepare Python Env') {
            steps {
                dir('op-chapter-search') { 
                    // Step 1: Create virtualenv if it doesn't exist
                    bat '''
                    if not exist venv (
                        echo Creating virtualenv...
                        python -m venv venv
                    )
                    '''

                    // Step 2: Upgrade pip and install requirements using venv's Python
                    bat '''
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Check Chapter') {
            steps {
                dir('op-chapter-search') {
                    withCredentials([
                        string(credentialsId: 'gmail-creds', variable: 'smtp_pass'),
                        string(credentialsId: 'op_receivers', variable: 'op_receivers')
                    ]) {
                        // Run Python script using venv's Python directly
                        bat '''
                        set smtp_pass=%smtp_pass%
                        set op_receivers=%op_receivers%
                        venv\\Scripts\\python.exe chapter_search.py
                        '''
                    }
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
