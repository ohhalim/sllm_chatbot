import uvicorn

if __name__ == "__main__":
    # "app.main:app"은 app 폴더 밑의 main.py 파일 안에 있는 app 변수를 의미합니다.
    # reload=True는 코드가 변경될 때마다 서버를 자동으로 재시작해주는 개발용 옵션입니다.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
