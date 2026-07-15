from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QToolButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from wordle_gui.__init__ import __version__ as game_version


class ResponsiveToolButton(QToolButton):
    def resizeEvent(self, event):
        new_icon_size = int(min(self.width(), self.height()) * 0.9)
        self.setIconSize(QSize(new_icon_size, new_icon_size))
        super().resizeEvent(event)


class Topbar(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setContentsMargins(10, 0, 20, 0)
        self.setMaximumHeight(100)

        self.setup_components()
        self.setup_layouts()

        # self.setup_presenters()

    def setup_components(self) -> None:
        self.title_label = QLabel("WORDEE")
        self.title_label.setObjectName("title_label")
        self.version_label = QLabel(f"version {game_version}")
        self.version_label.setObjectName("version_label")

        self.game_icon = ResponsiveToolButton()
        self.game_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.game_icon.setIcon(QIcon(":/icons/wordee-icon.svg"))

        self.help_icon = ResponsiveToolButton()
        self.help_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.help_icon.setIcon(QIcon(":/icons/help-icon.svg"))

        self.statistics_icon = ResponsiveToolButton()
        self.statistics_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.statistics_icon.setIcon(QIcon(":/icons/statistics-icon.svg"))

        self.settings_icon = ResponsiveToolButton()
        self.settings_icon.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.settings_icon.setIcon(QIcon(":/icons/settings-icon.svg"))

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
        self.setStyleSheet("border: 1px solid red;")

    def setup_presenters(self) -> None:
        raise NotImplementedError(
            "setup_presenters() not implemented in views/topbar.py"
        )
