pipeline {
  agent {
    label 'master'
  }
  environment {
    PYTHON_VERSION = '3.10.7'
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Set up Python') {
      steps {
        tool name: 'Python', type: 'hudson.plugins.python.PythonInstallation' // Configure Python tool in Jenkins
      }
    }
    stage('Install Dependencies') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Run Tests') {
      steps {
        sh 'python manage.py test'
      }
    }
  }
}
