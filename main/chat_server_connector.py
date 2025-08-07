"""
chat_server_connector.py

Defines AskWorker to asynchronously query the chat server API and emit the result.
"""
# pylint: disable=import-error,no-name-in-module
# pylint: disable=too-few-public-methods
import requests
from PySide6.QtCore import QObject, Signal

API_URL = "http://localhost:8000/ask"
TIMEOUT = 60


class AskWorker(QObject):
    """
    Worker that sends a question to the chat server and emits the answer when done.
    """

    finished = Signal(str)

    def __init__(self, question: str):
        """
        Initialize AskWorker with the given question.

        Args:
            question: The text of the question to send.
        """
        super().__init__()
        self.question = question

    def run(self):
        """
        Send the question to the API and emit the response or error.
        """
        try:
            r = requests.post(
                API_URL, json={"question": self.question}, timeout=TIMEOUT
            )
            r.raise_for_status()
            data = r.json()
            answer = data.get("answer", "No answer field")
        except requests.RequestException as e:
            answer = f"Error: {e}"
        self.finished.emit(answer)
