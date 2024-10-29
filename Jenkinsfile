pipeline {
    agent { label 'ec2-devita-ai' }

    environment {
        ECR_REGISTRY = '860195224276.dkr.ecr.ap-northeast-2.amazonaws.com'
        ECR_REPO_NAME = 'devita_ecr'
        IMAGE_TAG = 'latest_ai'
        AWS_REGION = 'ap-northeast-2'
        AWS_CREDENTIALS = credentials('AwsCredentials')
        INSTANCE_ID = 'i-0011ace91cb94a13f'
    }
    stages {
        stage('Check for Previous Builds') {
            steps {
                script {
                    // 현재 Job에서 실행 중인 이전 빌드를 가져옴
                    def job = Jenkins.instance.getItemByFullName(env.JOB_NAME)
                    def currentBuildNumber = currentBuild.number
                    
                    // 이전 빌드가 실행 중이면 중단시킴
                    job.builds.each { build ->
                        if (build.isBuilding() && build.number < currentBuildNumber) {
                            echo "Cancelling build #${build.number}"
                            build.doStop()  // 이전 빌드를 중단
                        }
                    }
                }
            }
        }
        stage('Checkout') {
            steps {
                script {
                    git branch: 'test', url: 'https://github.com/KTB-FinalProject-Team1/Devita-AI', credentialsId: "githubAccessToken"
                }
            }
        }
        stage('Login to ECR') {
            steps {
                script {
                    sh '''
                    export AWS_ACCESS_KEY_ID=$(echo $AWS_CREDENTIALS | cut -d':' -f1)
                    export AWS_SECRET_ACCESS_KEY=$(echo $AWS_CREDENTIALS | cut -d':' -f2)
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
                    '''
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    sh '''
                    docker build -t $ECR_REPO_NAME:$IMAGE_TAG .
                    docker tag $ECR_REPO_NAME:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPO_NAME:$IMAGE_TAG
                    '''
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    sh '''
                    docker push $ECR_REGISTRY/$ECR_REPO_NAME:$IMAGE_TAG
                    '''
                }
            }
        }
        stage('Start EC2 Instance and Deploy') {
            steps {
                script {
                    // EC2 인스턴스 시작
                    sh '''
                    export AWS_ACCESS_KEY_ID=$(echo $AWS_CREDENTIALS | cut -d':' -f1)
                    export AWS_SECRET_ACCESS_KEY=$(echo $AWS_CREDENTIALS | cut -d':' -f2)
                    aws ec2 start-instances --instance-ids $INSTANCE_ID --region $AWS_REGION
                    aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $AWS_REGION
                    '''
                    
                    // SSH로 AI 인스턴스에 접속하고 환경 변수를 전달
                    sshagent(['back_PEM']) {
                        sh '''
                        ssh -t -o StrictHostKeyChecking=no ubuntu@10.0.2.211 << EOF
                        export AWS_REGION='$AWS_REGION'
                        export ECR_REGISTRY='$ECR_REGISTRY'
                        export ECR_REPO_NAME='$ECR_REPO_NAME'
                        export IMAGE_TAG='$IMAGE_TAG'
                        export AWS_ACCESS_KEY_ID=\$(echo "$AWS_CREDENTIALS" | cut -d':' -f1)
                        export AWS_SECRET_ACCESS_KEY=\$(echo "$AWS_CREDENTIALS" | cut -d':' -f2)

                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

                        # 현재 실행 중이거나 종료된 컨테이너가 있는 경우만 삭제
                        docker ps -qa | xargs -r docker rm
                        # 현재 존재하는 이미지를 삭제할 때만 삭제
                        docker images -q | xargs -r docker rmi

                        docker pull $ECR_REGISTRY/$ECR_REPO_NAME:$IMAGE_TAG
                        docker images

                        # 기존에 실행 중이던 컨테이너가 있다면 삭제 후 새로운 컨테이너 실행
                        docker run -d --name devita_ai -p 8000:8000 $ECR_REGISTRY/$ECR_REPO_NAME:$IMAGE_TAG
                        docker ps -a
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
