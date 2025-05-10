
from src.singleton import Singleton
from src.js_bridge.bridge import BaseJsBridge


class Player(Singleton, BaseJsBridge):
    def __new__(cls, *args, **kwargs):
        return Singleton.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        Singleton.__init__(self, *args, **kwargs)

    def _init_once(self, driver=None):
        BaseJsBridge.__init__(
            self, 
            js_file_name='player.js',
            predict_script="return window.player?.injected;",
            driver=driver
        )

    def start(self, scenario: list, scenario_name: str, play_id: str):
        for action in scenario:
            self.send_command(f"player?.start({action}, '{scenario_name}', '{play_id}')")
            yield
        self.send_command("player?.stop()")

    def start_unit(self, scenario_unit: dict):
        self.send_command(f"player?.start({scenario_unit})")

    def stop(self):
        self.send_command("player?.stop()")


if __name__ == "__main__":
    from src.driver_factory import SeleniumDriverFactory
    from src.json_handler import load_scenarios
    from src.config import CONFIG

    driver = SeleniumDriverFactory().get_driver()
    logs = load_scenarios('replay_test')

    player = Player(driver=driver)
    player.start('replay_test', logs, 0.3)
    