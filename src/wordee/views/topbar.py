from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QCursor, QIcon
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from wordee import __version__ as game_version


class Topbar(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMaximumHeight(110)

        self.setup_components()
        self.setup_layouts()
        self.setup_shadow()

    def setup_components(self) -> None:
        self.title_label = QLabel("WORDEE")
        self.title_label.setObjectName("title_label")

        self.version_label = QLabel(f"version {game_version}")
        self.version_label.setObjectName("version_label")

        self.game_icon = QPushButton()
        self.game_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.game_icon.setIcon(QIcon(":/icons/wordee-icon.svg"))
        self.game_icon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.game_icon.setMinimumSize(50, 50)
        self.game_icon.setIconSize(QSize(50, 50))

        self.help_icon = QPushButton()
        self.help_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.help_icon.setIcon(QIcon(":/icons/help-icon.svg"))
        self.help_icon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.help_icon.setIconSize(QSize(50, 50))

        self.statistics_icon = QPushButton()
        self.statistics_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.statistics_icon.setIcon(QIcon(":/icons/statistics-icon.svg"))
        self.statistics_icon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.statistics_icon.setMinimumSize(50, 50)
        self.statistics_icon.setIconSize(QSize(50, 50))

        self.settings_icon = QPushButton()
        self.settings_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.settings_icon.setIcon(QIcon(":/icons/settings-icon.svg"))
        self.settings_icon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_icon.setMinimumSize(50, 50)
        self.settings_icon.setIconSize(QSize(50, 50))

    def setup_layouts(self) -> None:
        topbar_layout = QHBoxLayout()

        title_labels_layout = QVBoxLayout()
        title_labels_layout.addWidget(self.title_label)
        title_labels_layout.addWidget(self.version_label)

        logo_area_layout = QHBoxLayout()
        logo_area_layout.addLayout(title_labels_layout)
        logo_area_layout.addWidget(self.game_icon)

        topbar_layout.addLayout(logo_area_layout)
        topbar_layout.addStretch()

        icon_area_layout = QHBoxLayout()
        icon_area_layout.addWidget(self.help_icon)
        icon_area_layout.addWidget(self.statistics_icon)
        icon_area_layout.addWidget(self.settings_icon)
        icon_area_layout.setSpacing(20)

        topbar_layout.addLayout(icon_area_layout)

        self.setLayout(topbar_layout)

    def setup_shadow(self) -> None:
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setYOffset(5)
        shadow.setColor(QColor(63, 80, 90, 20))

        self.setGraphicsEffect(shadow)
