import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class BlackWindow(QWidget):
    """Main window with a pure‑black background and a brighter centred container."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QtGPT")
        self.resize(800, 600)

        # --- Black background -------------------------------------------------
        self.setStyleSheet("background-color: #1f1e1e;")

        # --- Centring layout --------------------------------------------------
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 220)
        outer_layout.setSpacing(0)

        # --- Brighter middle container ---------------------------------------
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setMinimumSize(400, 100)  # tweak to taste
        outer_layout.addWidget(self.container, alignment=Qt.AlignCenter)

        # Style: a touch lighter than black
        self.container.setStyleSheet(
            """
            QWidget#container {
                background-color: #3d3c3c;   /* charcoal grey */
                border-radius: 12px;          /* soft corners */
            }
            """
        )

        # --- Placeholder content (centre‑aligned label) ----------------------
        label = QLabel("Text goes here", self.container)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #ffffff; font-size: 16px;")

        inner_layout = QVBoxLayout(self.container)
        inner_layout.addWidget(label, alignment=Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BlackWindow()
    win.show()
    sys.exit(app.exec())
