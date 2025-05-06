import os
from yaml import safe_load
from dotenv import load_dotenv

class Config:
    SEP = '.'

    def __init__(self):
        # .env 파일 로드
        self.__table = {}

        ## 아래로 갈수록 우선순위가 높음.
        # config.yaml
        self.__deep_update(self.__table, self.__load_yaml_config())

        # .env && 환경변수
        self.__deep_update(self.__table, self.__load_env_config())
    
    def get(self, name: str, default=None):
        try:
            return self.index(self.__table, name)
        except KeyError as e:
            if default is not None:
                return default
            else:
                raise e
    
    def index(self, table: dict, key: str):
        if self.SEP in key:
            new_key, _, rest_key = key.partition(self.SEP)
            return self.index(table[new_key], rest_key)
        else:
            return table[key]

    def __load_yaml_config(self, path: str = "config.yaml") -> dict:
        with open(path, "r") as f:
            return safe_load(f)

    def __load_env_config(self) -> dict:
        """
        환경변수 중 키에 '.'이 포함된 것만 계층형 구조로 self.__table에 저장
        예: APP.DB_HOST=localhost -> {'APP' : {'DB_HOST': 'localhost'}}
        """
        load_dotenv()
        env_config = {}
        for key, value in os.environ.items():
            env_config.update(self.__destructuring(key, value))
        return env_config

    def __destructuring(self, key: str, value: str):
        table = {}
        if self.SEP in key:
            new_key, _, rest_key = key.partition(self.SEP)
            table[new_key] = self.__destructuring(rest_key, value)
        else:
            table[key] = value
        return table

    def __deep_update(self, original: dict, update: dict):
        for key, value in update.items():
            if (
                key in original and
                isinstance(original[key], dict) and
                isinstance(value, dict)
            ):
                self.__deep_update(original[key], value)
            else:
                original[key] = value


CONFIG = Config()


if __name__ == "__main__":
    print(CONFIG.get('APP'))
    print(CONFIG.get('APP.CORS'))
    print(CONFIG.get('APP.SELENIUM.HEADLESS'))
    print(CONFIG.get('APP.XXX', []))
    print(CONFIG.get('APP.XXX'))
