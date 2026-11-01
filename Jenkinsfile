pipeline {
    agent any

    parameters {
        string(name: 'INPUT_ONE', defaultValue: 'demo application')
        string(name: 'INPUT_TWO', defaultValue: 'prompt injection')
        string(name: 'SERVICE_URL', defaultValue: 'http://host.docker.internal:8000/generate')
    }

    stages {
        stage('Install dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Generate prompts') {
            steps {
                bat 'py scripts\\call_service.py --url "%SERVICE_URL%" --input-one "%INPUT_ONE%" --input-two "%INPUT_TWO%" --output output\\prompts.json'
            }
        }
        stage('Create Excel report') {
            steps {
                bat 'py scripts\\to_excel.py output\\prompts.json output\\prompts.xlsx'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'output/*', fingerprint: true
        }
    }
}
