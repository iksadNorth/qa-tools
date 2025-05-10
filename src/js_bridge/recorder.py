import time
import json

from src.singleton import Singleton
from src.js_bridge.bridge import BaseJsBridge


class Recorder(Singleton, BaseJsBridge):
    def __new__(cls, *args, **kwargs):
        return Singleton.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        Singleton.__init__(self, *args, **kwargs)

    def _init_once(self, driver=None):
        BaseJsBridge.__init__(
            self, 
            js_file_name='recorder.js',
            predict_script="return window.recorder?.injected;",
            driver=driver
        )
    
    def start(self) -> None:
        return self.send_command("return recorder?.start();")
    
    def stop(self) -> None:
        return self.send_command("return recorder?.stop();")

    def getLog(self) -> str:
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
                if (logs := self.getLog()):
                    total_logs.extend(logs)
                else:
                    time.sleep(interval_sec)
            raise RuntimeError
        except Exception:
            total_logs.extend(self.getLog())
        return total_logs


if __name__ == "__main__":
    from src.driver_factory import SeleniumDriverFactory
    from src.json_handler import save_scenarios
    from src.config import CONFIG

    driver = SeleniumDriverFactory().get_driver()
    driver.get(CONFIG.get('APP.SELENIUM.INIT_URL'))

    recorder = Recorder(driver=driver)
    all_logs = recorder.save_logs_periodically(1)
    save_scenarios(all_logs)
