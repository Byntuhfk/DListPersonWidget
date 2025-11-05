# renderer_interface.py
from abc import ABC, abstractmethod, ABCMeta
from PySide6.QtGui import QPainter
from PySide6.QtCore import QObject


class QObjectABCMeta(type(QObject), ABCMeta):
    pass

class RendererInterface(QObject, ABC, metaclass=QObjectABCMeta):
    """Интерфейс для всех рендереров"""

    def __init__(self, parent=None):
        super().__init__(parent)

    @abstractmethod
    def render(self, painter: QPainter) -> None:
        """Основной метод отрисовки"""
        pass

    @abstractmethod
    def handle_resize(self, width: int, height: int) -> None:
        """Обработка изменения размера"""
        pass
