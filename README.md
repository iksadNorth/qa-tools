# 개요
Web Product를 End To End 테스트하기 위한 프로젝트.

아래 문제를 해결하기 위해 기획함
- 코드 작성 없이 테스트 수행
- 고객사들에게 혹은 인수인계 시, 인계자를 위한 Product 사용법 안내 시각화

# 사용방법
1. 해당 프로젝트를 Git Clone
2. config.yaml.template 파일을 기반으로 config.yaml 파일 생성
3. (Linux 기준) 
    ```
    source scripts/init_linux.sh
    ```

    (Mac 기준)
    ```
    source scripts/init_mac.sh
    ```

    (Windows 기준)
    scripts/init_window.bat 파일 클릭
4. 아래 명령어를 실행
    ```
    uv run python -m uvicorn main:app
    ```
5. http://localhost:8000/controller 를 실행해서 컨트롤러 화면띄우기
