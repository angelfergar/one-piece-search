pipeline {
    agent {
        node {
	    label 'op-search'
            customWorkspace 'C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\op-chapter-search'
        }
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
                bat '''
                if not exist venv (
                    echo Creating virtualenv...
                    python -m venv venv
                )

                call venv\\Scripts\\activate

                rem Calculate hash of requirements.txt
                certutil -hashfile requirements.txt SHA256 > requirements.hash.tmp
                findstr /v "hash" requirements.hash.tmp > requirements.hash

                rem Compare hashes
                if not exist .requirements.hash (
                    echo Installing dependencies (first run)...
                    pip install -r requirements.txt
                    copy requirements.hash .requirements.hash
                ) else (
                    fc .requirements.hash requirements.hash >nul
                    if errorlevel 1 (
                        echo Requirements changed, reinstalling...
                        pip install -r requirements.txt
                        copy requirements.hash .requirements.hash
                    ) else (
                        echo Requirements unchanged, skipping install.
                    )
                )

                del requirements.hash.tmp
                '''
            }
        }

        stage('Check Chapter') {
            steps {
                withCredentials([
                    string(credentialsId: 'gmail-creds', variable: 'smtp_pass'),
                    string(credentialsId: 'op_receivers', variable: 'op_receivers')
                ]) {
                    bat '''
                    call venv\\Scripts\\activate
                    set smtp_pass=%smtp_pass%
                    set op_receivers=%op_receivers%
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
