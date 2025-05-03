from selenium import webdriver
import time
from src.json_handler import save_scenarios
import json
from jinja2 import Environment, FileSystemLoader
from src.driver_factory import SeleniumDriverFactory


class Recorder:
    STORE_KEY = 'testtool_logs'
    
    def __init__(self, url: str, driver=None):
        self.driver = driver or webdriver.Chrome()
        self.driver.get(url)
        self.env = Environment(loader=FileSystemLoader('template'))
    
    def inject_js(self) -> None:
        """로그 코드 주입. 무조건 멱등성을 띄어야 함.
        """
        # 이미 주입되었으면 종료.
        has_run = self.driver.execute_script(f"return typeof run === 'function';")
        if has_run: return
        
        template = self.env.get_template('recorder.js')
        rendered_script = template.render()
        self.driver.execute_script(rendered_script)
        self.driver.execute_script('run();')

    def collect_logs(self) -> str:
        """브라우저에서 로그 수집. 프로세스 종료 시, 무조건 호출되어야 함.
        """
        try:
            if self.driver is None: raise RuntimeError
            logs = self.driver.execute_script(f"return getLog();")
            if not logs: raise RuntimeError
            return json.loads(logs)
        except Exception as e:
            return []
    
    def health_check(self) -> bool:
        """브라우저 Health Check.
        """
        return (self.driver.current_url) is not None

    def save_logs_periodically(self, interval_sec=60):
        """로그 수집 후, 로그 저장.
        """
        total_logs = []
        try:
            while self.health_check(): 
                self.inject_js()
                if (logs := self.collect_logs()):
                    total_logs.extend(logs)
                else:
                    time.sleep(interval_sec)
            raise RuntimeError
        except Exception:
            total_logs.extend(self.collect_logs())
        return total_logs


if __name__ == "__main__":
    driver = SeleniumDriverFactory().get_driver()
    recorder = Recorder(
        url='https://www.naver.com/',
        driver=driver,
    )
    all_logs = recorder.save_logs_periodically(1)
    save_scenarios(all_logs)
