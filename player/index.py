from selenium import webdriver
from src.json_handler import load_json
import time

def wait_until_element(driver, selector: str, timeout: int = 5):
    # driver로부터 특정 셀렉터 요소가 나타날 때까지 대기
    pass

def click_element(driver, selector: str):
    # driver.find_element로 클릭
    pass

def input_text(driver, selector: str, value: str):
    # driver.find_element로 텍스트 입력
    pass

def upload_file(driver, selector: str, file_path: str):
    # input[type=file]에 파일 경로 보내기
    pass

class Player:
    def __init__(self, scenario_path: str):
        self.driver = webdriver.Chrome()
        self.actions = load_json(scenario_path)["시나리오"]

    def play(self):
        start_time = None
        for action in self.actions:
            if start_time is None:
                start_time = action["timestamp"]

            elapsed = action["timestamp"] - start_time
            time.sleep(elapsed)

            if action["type"] == "click":
                click_element(self.driver, action["selector"])
            elif action["type"] == "input":
                input_text(self.driver, action["selector"], action["value"])
            elif action["type"] == "file_upload":
                upload_file(self.driver, action["selector"], action["file_path"])
            elif action["type"] == "assert":
                wait_until_element(self.driver, action["selector"], timeout=action.get("timeout", 5))

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    player = Player('scenarios/recorded.json')
    player.play()
    player.close()