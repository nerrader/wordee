from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QCursor
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from wordle_gui.constants import GameMode


class BlockSwitchModeDialog(QDialog):
    def __init__(self, game_mode: GameMode):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)

        layout = QVBoxLayout(self)

        result_container = QFrame()
        result_container.setObjectName("block_switch_mode_container")
        result_container.setContentsMargins(10, 10, 10, 10)

        stop_header_label = QLabel("STOP!!")
        stop_header_label.setObjectName("block_switch_mode_stop_header_label")
        stop_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        daily_content_message = (
            "no switching game modes till you're done with today's daily."
        )
        unlimited_content_message = (
            "no switching modes till you're done with your unlimited game."
        )

        content_label = QLabel(
            daily_content_message if game_mode == "daily" else unlimited_content_message
        )
        content_label.setObjectName("block_switch_mode_contents_label")
        content_label.setWordWrap(True)

        ok_button = QPushButton("ok we get it")
        ok_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        ok_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        ok_button.setObjectName("block_switch_mode_ok_button")
        ok_button.clicked.connect(self.accept)

        ok_button_shadow = QGraphicsDropShadowEffect(ok_button)
        ok_button_shadow.setBlurRadius(15)
        ok_button_shadow.setYOffset(5)
        ok_button_shadow.setColor(QColor(58, 82, 95, 25))

        ok_button.setGraphicsEffect(ok_button_shadow)

        layout.setSpacing(20)
        layout.addWidget(stop_header_label)
        layout.addWidget(content_label)
        layout.addWidget(ok_button)

        self.setLayout(layout)
