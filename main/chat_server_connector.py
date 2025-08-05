import requests
from PySide6.QtCore import QObject, Signal

API_URL = "http://localhost:8000/ask"
TIMEOUT = 60

class AskWorker(QObject):
    finished = Signal(str)
    
    def __init__(self, question: str):
        super().__init__()
        self.question = question

    def run(self):
        try:
            r = requests.post(API_URL, json={"question": self.question}, timeout=TIMEOUT)
            r.raise_for_status()
            answer = r.json().get("answer", "No answer field")
        except Exception as e:
            answer = f" Error: {e}"
        self.finished.emit(answer)
        