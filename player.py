from selenium import webdriver
import time
from jinja2 import Environment, FileSystemLoader


class Player:
    def __init__(self, driver=None):
        self.driver = driver or webdriver.Chrome()
        self.env = Environment(loader=FileSystemLoader('template'))

    def inject_js(self) -> None:
        """로그 코드 주입. 무조건 멱등성을 띄어야 함.
        """
        # 이미 주입되었으면 종료.
        has_run = self.driver.execute_script(f"return typeof run === 'function';")
        if has_run: return
        
        template = self.env.get_template('player.js')
        rendered_script = template.render()
        self.driver.execute_script(rendered_script)
    
    def health_check(self) -> bool:
        """브라우저 Health Check.
        """
        return (self.driver.current_url) is not None
    
    def keep_alive(self, interval_sec=60):
        try:
            while self.health_check(): 
                time.sleep(interval_sec)
            raise RuntimeError
        except Exception:
            pass

    def play(self, scenario: list, interval_sec=60):
        for action in scenario:
            self.inject_js()
            print((script := f"run({action})"))
            self.driver.execute_script(script)
            time.sleep(interval_sec)


if __name__ == "__main__":
    logs = [
        {
            'type': 'navigate',
            'to': 'https://www.google.com/search?q=%EA%B5%AC%EA%B8%80%EB%B2%88%EC%97%AD%EA%B8%B0&oq=%EA%B5%AC%EA%B8%80%EB%B2%88%EC%97%AD%EA%B8%B0',
        },
    ]
    player = Player()
    player.play(logs, 0.3)
    player.keep_alive(1)
    