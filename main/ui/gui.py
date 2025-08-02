import sys
from PySide6.QtWidgets import QFrame,QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QSizePolicy, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtCore import Qt

class BlackWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QtGPT")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #1f1e1e;")

        #main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top spacer
        main_layout.addSpacing(30)

        # label in top layout
        top_label = QLabel("Ask me something", self)
        top_label.setAlignment(Qt.AlignCenter)
        top_label.setStyleSheet("color: #ffffff; font-size: 18px;")
        main_layout.addWidget(top_label)

        # Spacer 
        main_layout.addSpacing(20)

        #Middle container
        self.prompt_textarea = QWidget(self)
        self.prompt_textarea.setObjectName("container")
        self.prompt_textarea.setMinimumSize(400, 100)
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
        
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)      # no frame border
        scroll.setStyleSheet("background: green;")  # transparent background

        container = QWidget()
        container.setStyleSheet("background: white;")  # keep it see-through
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(8)

        

        # Bottom stretch to push everything upwards
        main_layout.addStretch()

        
        
        
    def on_send_clicked(self):
        text = self.input_line.toPlainText()
        print(text)    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BlackWindow()
    win.show()
    sys.exit(app.exec())
