from selenium import webdriver
import time
from datetime import datetime
from src.json_handler import save_json
import json
from jinja2 import Environment, FileSystemLoader

class Recorder:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.env = Environment(loader=FileSystemLoader('recorder'))
        self.inject_recorder_js()

    def inject_recorder_js(self, context=None):
        context = context or {} 
        template = self.env.get_template('index.js')
        rendered_script = template.render(**context)
        self.driver.execute_script(rendered_script)

    def collect_logs(self):
        logs = self.driver.execute_script("return window.localStorage.getItem('testtool_logs');")
        if not logs: return []
        
        self.driver.execute_script("window.localStorage.removeItem('testtool_logs');")
        return json.loads(logs)

    def save_logs_periodically(self, interval_sec=60):
        all_logs = []
        try:
            while True:
                logs = self.collect_logs()
                all_logs.extend(logs)
                time.sleep(interval_sec)
        except KeyboardInterrupt:
            created_at = datetime.now().strftime("%Y%m%d%H%M%S")
            save_json(f'scenarios/recorded_{created_at}.json', {"scenario": all_logs})

if __name__ == "__main__":
    recorder = Recorder()
    recorder.save_logs_periodically()
