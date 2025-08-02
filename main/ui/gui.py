import sys
from PySide6.QtWidgets import QFrame,QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QSizePolicy, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtCore import Qt

class BlackWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QtGPT")
        self.resize(1080, 800)
        self.setStyleSheet("background-color: #1f1e1e;")
        self.user_question=""

        #main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
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

        #Middle container
        self.prompt_textarea = QWidget(self)
        self.prompt_textarea.setObjectName("container")
        self.prompt_textarea.setMaximumSize(800, 175)
        self.prompt_textarea.setMinimumSize(500, 175)

        self.prompt_textarea.setStyleSheet("""
            QWidget#container {
                background-color: #3d3c3c;
                border-radius: 12px;
            }
        """)

        # Layout inside the container
        container_layout = QVBoxLayout(self.prompt_textarea)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(5)
        
        # The QLineEdit with placeholder
        self.input_line = QPlainTextEdit(self.prompt_textarea)
        self.input_line.setPlaceholderText("Ask me something…")

        self.input_line.setStyleSheet("""
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
        """)
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
        self.button.setStyleSheet("""
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
        """)
        # Make sure it doesn’t expand vertically
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_row.addWidget(self.button)
        
        #when button clicked then copy the text and delete it from the textbox

        self.button.clicked.connect(self.on_send_clicked)
        self.button.clicked.connect(self.input_line.clear)
        
        container_layout.addLayout(btn_row)
        
        main_layout.addSpacing(20)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)      # no frame border
        scroll.setStyleSheet("background: transparent;")  # transparent background
        scroll.setSizePolicy(
            QSizePolicy.Expanding,    # horizontal
            QSizePolicy.Expanding     # vertical
        )
        
        container = QWidget()
        container.setStyleSheet("background: transparent;")  # keep it see-through
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.setSpacing(0)
        vbox.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll,3)
        # Bottom stretch to push everything upwards
        main_layout.addStretch()
    

        self.button.clicked.connect(lambda: self.user_message(container,vbox,self.user_question))
        vbox.addStretch()

        
    def on_send_clicked(self):
        text = self.input_line.toPlainText()
        self.user_question=text
        
    def user_message(self,container,vbox,user_question):
        chat_container = QWidget(container)
        chat_container.setStyleSheet("""
            border-radius: 8px;
            padding: 6px;
        """)
        chat_layout = QHBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        

        # Put the user's text on the right
        user_text = QLabel(user_question, chat_container)
        user_text.setStyleSheet("color: black; font-size: 16px; background-color: #3d3c3c;")
        chat_layout.addStretch()             # push label to the right
        chat_layout.addWidget(user_text)
        
        second_bubble = QWidget(container)
        second_bubble.setStyleSheet("""
            border-radius: 8px;
            padding: 6px;
        """)
        
        second_layout = QHBoxLayout(second_bubble)
        second_layout.addStretch()
        lbl2 = QLabel("How are you?", second_bubble)
        lbl2.setStyleSheet("color: white;")
        second_layout.addWidget(lbl2)
                
        vbox.addWidget(chat_container, alignment=Qt.AlignTop)
        vbox.addWidget(second_bubble,alignment=Qt.AlignLeft)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BlackWindow()
    win.show()
    sys.exit(app.exec())


