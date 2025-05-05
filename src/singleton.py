from threading import Lock

class Singleton:
    _instances = {}
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, *args, **kwargs):
        if self._initialized: return
        self._initialized = True

        # 자식 클래스에서 _init_once를 구현하면 여기서 한 번만 호출
        self._init_once(*args, **kwargs)
    
    def _init_once(self, *args, **kwargs):
        pass
