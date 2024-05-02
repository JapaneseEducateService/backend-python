#!/bin/bash

curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

aws aws configure
# AWS Systems Manager Parameter Store에서 서비스 계정 키를 가져옴
aws ssm get-parameter --name "/app/credentials.json" --with-decryption --region ap-northeast-2 --query "Parameter.Value" --output text > /app/credentials.json

# GOOGLE_APPLICATION_CREDENTIALS 환경 변수 설정
export GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

# 원래 실행하려던 명령 실행
exec "$@"