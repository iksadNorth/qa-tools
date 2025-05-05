import time
from jinja2 import Environment, FileSystemLoader
from src.driver_factory import SeleniumDriverFactory
from src.json_handler import load_scenarios
from asyncio import sleep
from src.singleton import Singleton


class Player(Singleton):
    def _init_once(self, driver=None):
        self.driver = driver or SeleniumDriverFactory().get_driver()
        self.env = Environment(loader=FileSystemLoader('template'))

    def inject_js(self) -> None:
        """로그 코드 주입.
        """
        template = self.env.get_template('player.js')
        rendered_script = template.render()
        self.driver.execute_script(rendered_script)
    
    def health_check(self) -> bool:
        """브라우저 Health Check.
        """
        return (self.driver.current_url) is not None
    
    def send_command(self, command=None):
        # 이미 주입되었으면 종료.
        has_func = self.driver.execute_script(f"return window.player?.injected;")
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

    def play(self, scenario: list, interval_sec=0.1):
        for action in scenario:
            print((script := f"player.start({action})"))
            self.send_command(script)
            time.sleep(interval_sec)


if __name__ == "__main__":
    driver = SeleniumDriverFactory().get_driver()
    logs = load_scenarios('scenarios/recorded_20250505124605.json')

    player = Player(driver=driver)
    player.play(logs, 0.3)
    