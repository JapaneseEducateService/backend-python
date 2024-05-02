# CREDENTIALS 환경변수에 설정 된 값을 파일로 출력
echo $CREDENTIALS > /app/credentials.json

# GOOGLE_APPLICATION_CREDENTIALS 환경 변수 설정
export GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

# 원래 실행하려던 명령 실행
exec "$@"