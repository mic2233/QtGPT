import sys

# import chatgpt
from chat_server_connector import AskWorker
from mail_sender.emai_bridge import send_local_mail

from PySide6.QtWidgets import (
    QFrame,
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
    QSizePolicy,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
)
from PySide6.QtCore import Qt, Slot, QThread


class BlackWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QtGPT")
        self.resize(1080, 800)
        self.setStyleSheet("background-color: #1f1e1e;")
        self.user_question = ""
        self.chat_answer = ""
        self._threads: list[QThread] = []  # <- keep live threads

        # main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 7, 15)
        main_layout.setSpacing(0)

        # Top spacer
        main_layout.addSpacing(30)

        # label in top layout
        top_label = QLabel("QtGPT Open-Source ChatBot", self)
        top_label.setAlignment(Qt.AlignCenter)
        top_label.setStyleSheet("color: #ffffff; font-size: 18px;")
        main_layout.addWidget(top_label)

        # Spacer
        main_layout.addSpacing(20)

        # Middle container
        self.prompt_textarea = QWidget(self)
        self.prompt_textarea.setObjectName("container")
        self.prompt_textarea.setMaximumSize(800, 175)
        self.prompt_textarea.setMinimumSize(500, 175)

        self.prompt_textarea.setStyleSheet(
            """
            QWidget#container {
                background-color: #3d3c3c;
                border-radius: 12px;
            }
        """
        )

        # Layout inside the container
        container_layout = QVBoxLayout(self.prompt_textarea)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(5)

        # The QLineEdit with placeholder
        self.input_line = QPlainTextEdit(self.prompt_textarea)
        self.input_line.setPlaceholderText("Ask me something…")

        self.input_line.setStyleSheet(
            """
            QPlainTextEdit {
                background-color: #2e2d2d;
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            QPlainTextEdit:focus {
                border: 1px solid #575757;
            }
        """
        )
        self.input_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        container_layout.addWidget(self.input_line, 1)

        # Optional: stretch so the lineedit sits at the top of the container
        container_layout.addStretch()

        # Add container into the main layout
        main_layout.addWidget(self.prompt_textarea, alignment=Qt.AlignCenter)

        btn_row = QHBoxLayout()
        btn_row.addStretch()  # pushes button to the right

        self.button = QPushButton("Send", self.prompt_textarea)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setStyleSheet(
            """
            QPushButton {
                background-color: #5a5a5a;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
            QPushButton:pressed {
                background-color: #4a4a4a;
            }
        """
        )
        # Make sure it doesn’t expand vertically
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_row.addWidget(self.button)

        # when button clicked then copy the text and delete it from the textbox

        self.button.clicked.connect(self.on_send_clicked)
        self.button.clicked.connect(self.input_line.clear)

        container_layout.addLayout(btn_row)

        main_layout.addSpacing(20)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)  # no frame border
        scroll.setStyleSheet(
            """
    QScrollBar:vertical {
        background: #030303;
        width: 12px;
        margin: 0px 0px 0px 0px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background: #808080;
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background: #a0a0a0;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
        subcontrol-origin: margin;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
        """
        )
        scroll.setWidgetResizable(True)  # fit content to width
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )  # or Qt.ScrollBarAlwaysOn

        container = QWidget()
        container.setStyleSheet("background: transparent;")  # keep it see-through
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(125, 125, 100, 125)
        vbox.setSpacing(40)
        scroll.setWidget(container)
        main_layout.addWidget(scroll, 3)
        # Bottom stretch to push everything upwards
        main_layout.addStretch()

        # self.button.clicked.connect(lambda: self.user_message(container,vbox,self.user_question,self.chat_answer))
        vbox.addStretch()
        self.container = container  # ① FIX – keep for later
        self.vbox = vbox  # ② FIX

    def on_send_clicked(self):
        question = self.input_line.toPlainText().strip()
        if not question:
            return

        self.user_question = question  # keep prompt
        self.add_user_message(question)
        self.input_line.clear()

        thread = QThread(self)
        worker = AskWorker(question)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.finished.connect(self.on_answer_ready)
        worker.finished.connect(thread.quit)

        # keep both objects alive
        self._threads.append((thread, worker))  # ③ FIX

        # safe deletion after finish
        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(lambda: self._threads.remove((thread, worker)))

        thread.start()

    # ────────────────────────────────────────────
    @Slot(str)
    def on_answer_ready(self, answer: str):
        self.add_bot_message(answer)  # quick console print
        self.user_message(  # real GUI bubbles
            self.container, self.vbox, self.user_question, answer
        )
        send_local_mail(self.user_question, answer)

    def _handle_answer(self, answer, thread, worker):
        self.add_bot_message(answer)
        thread.quit()

    # dummy helpers so example runs
    def add_user_message(self, text):
        print("YOU:", text)

    def add_bot_message(self, text):
        print("BOT:", text)

    def user_message(self, container, vbox, user_question, chat_answer):
        chat_container = QWidget(container)
        chat_container.setStyleSheet(
            """
            border-radius: 8px;
            padding: 6px;
        """
        )
        chat_layout = QHBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)

        # Put the user's text on the right
        user_text = QLabel(user_question, chat_container)
        user_text.setStyleSheet(
            "color: white; font-size: 20px; background-color: #3d3c3c;"
        )
        chat_layout.addStretch()  # push label to the right
        chat_layout.addWidget(user_text)

        second_bubble = QWidget(container)
        second_bubble.setStyleSheet(
            """

            border-radius: 8px;
            padding: 6px;
        """
        )

        second_layout = QHBoxLayout(second_bubble)

        second_layout.addStretch()
        lbl2 = QLabel(chat_answer, second_bubble)
        lbl2.setStyleSheet("color: white; font-size: 20px; background-color: #3d3c3c;")

        second_layout.addWidget(lbl2)

        user_text.setWordWrap(True)
        lbl2.setWordWrap(True)
        user_text.setMaximumWidth(int(container.width() * 0.7))
        lbl2.setMaximumWidth(int(container.width() * 0.7))
        vbox.insertWidget(vbox.count() - 1, chat_container)
        vbox.insertWidget(vbox.count() - 1, second_bubble, alignment=Qt.AlignLeft)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BlackWindow()
    win.show()
    sys.exit(app.exec())
