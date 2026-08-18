from PySide6.QtCore import QObject, Signal


class GameSignals(QObject):
    alphabet_key_pressed = Signal(str)
    enter_key_pressed = Signal()
    backspace_key_pressed = Signal()
    switch_mode_requested = Signal()


game_signals = GameSignals()
