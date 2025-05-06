from jinja2 import Environment, FileSystemLoader
from asyncio import sleep

from src.driver_factory import SeleniumDriverFactory
from src.config import CONFIG


class BaseJsBridge:
    """Selenium과 브라우저의 교량 역할의 클래스.
    해당 클래스를 통해서 JS 코드의 함수, 변수에 접근한다.
    두 컴포넌트 간 통신 중 일어나는 어려움을 라이브러리 형식으로 정리.

    [주요 쟁점]
    1. [Selenium -> 브라우저] 통신은 execute_script() 메서드를 통해 쉽게 실현되지만,
    [브라우저 -> Selenium] 통신은 실현이 어렵다. 
    필자는 이것을 Polling을 통해 주기적으로 JS 코드의 상태값을 확인하는 전략으로 풀어나갔다.
    2. 브라우저 특화 소스 코드와 Selenium 특화 소스 코드를 명확히 분리하려 했다.
    최대한 연산량을 많이 먹는 Polling 확인은 피하려 JS 쪽에도 로직 비중을 높였다.
    필수적인 로직이 아닌 이상 최대한 Python Selenium 로직을 최소화 하고자 한다.

    [Param]
    - js_file_name:         {APP.JS.ROOTDIR} 경로 아래의 JS 코드 중 해당 클래스가 주입하고자 하는 JS 소스코드 파일명.
    - predict_script:       Polling으로 JS 코드 주입여부를 확인하기 위한 테스트 JS 코드. 결과값이 True면 주입됨을 확인.
    """
    def __init__(self, js_file_name: str, predict_script: str, driver=None):
        self.driver = driver or SeleniumDriverFactory().get_driver()
        self.env = Environment(loader=FileSystemLoader(CONFIG.get('APP.JS.ROOTDIR')))
        self.js_file_name = js_file_name
        self.predict_script = predict_script
    
    def inject_js(self) -> None:
        """JS 코드 주입.
        """
        template = self.env.get_template(self.js_file_name)
        rendered_script = template.render()
        self.driver.execute_script(rendered_script)
    
    def health_check(self) -> bool:
        """브라우저 Health Check.
        """
        return (self.driver.current_url) is not None
    
    def send_command(self, command=None):
        """JS 함수 혹은 변수를 사용하는 메서드. 
        JS 코드가 주입이 안된 경우, Lazy하게 주입하고 JS 코드를 실행한다.
        """
        has_func = self.driver.execute_script(self.predict_script)
        if not has_func: self.inject_js()
        return self.driver.execute_script(command) if command else None
    
    async def launch(self, interval_sec=60) -> None:
        """driver에 필요한 JS 코드를 주입.
        [브라우저 -> Selenium]으로 통신이 어렵기 때문에 JS 결과를 Polling으로 확인.
        기존 웹페이지에서 벗어나는 경우, JS 코드 재주입이 필요하므로 주기적으로 주입여부 확인 요망.

        Ex) wwww.naver.com => search.naver.com 이동 시, JS 주입 코드가 사라짐.
        """
        while self.health_check():
            # JS 코드 주입여부 확인.
            self.send_command()

            # 무분별한 주입여부 확인 방지
            await sleep(interval_sec)
