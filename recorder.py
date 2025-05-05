import time
from src.json_handler import save_scenarios
import json
from jinja2 import Environment, FileSystemLoader
from src.driver_factory import SeleniumDriverFactory
from asyncio import sleep
from src.singleton import Singleton


class Recorder(Singleton):
    STORE_KEY = 'testtool_logs'
    
    def _init_once(self, driver=None):
        self.driver = driver or SeleniumDriverFactory().get_driver()
        self.env = Environment(loader=FileSystemLoader('template'))
    
    def inject_js(self) -> None:
        """로그 코드 주입.
        """
        template = self.env.get_template('recorder.js')
        rendered_script = template.render()
        self.driver.execute_script(rendered_script)
    
    def health_check(self) -> bool:
        """브라우저 Health Check.
        """
        return (self.driver.current_url) is not None
    
    def send_command(self, command=None):
        # 이미 주입되었으면 종료.
        has_func = self.driver.execute_script("return window.recorder?.injected;")
        if not has_func: self.inject_js()
        return self.driver.execute_script(command) if command else None
    
    async def launch(self, interval_sec=60) -> None:
        """driver에 필요한 JS 코드 주입.
        """
        while self.health_check():
            # JS 코드 주입여부 확인.
            self.send_command()

            # 무분별한 주입여부 확인 방지
            await sleep(interval_sec)

    def collect_logs(self) -> str:
        """브라우저에서 로그 수집. 프로세스 종료 시, 무조건 호출되어야 함.
        """
        try:
            logs = self.send_command("return recorder.getLog();")
            if not logs: raise RuntimeError
            return json.loads(logs)
        except Exception as e:
            return []

    def save_logs_periodically(self, interval_sec=60):
        """로그 수집 후, 로그 저장.
        """
        total_logs = []
        try:
            while self.health_check():
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
    driver.get('https://www.naver.com/')

    recorder = Recorder(driver=driver)
    all_logs = recorder.save_logs_periodically(1)
    save_scenarios(all_logs)
