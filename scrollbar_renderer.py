# scrollbar_renderer.py
from PySide6.QtWidgets import QScrollBar
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, Signal
from renderer_interface import RendererInterface


class ScrollBarRenderer(RendererInterface):
    offset_changed = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.scrollbar = QScrollBar(Qt.Vertical, parent)
        self.scrollbar.setVisible(False)
        self.max_offset_y: int = 0
        self.current_offset: int = 0
        self.const_width: int = 18

        self._setup_connections()

    def _setup_connections(self) -> None:
        self.scrollbar.valueChanged.connect(self._on_scrollbar_changed)
        self.offset_changed.connect(self.scrollbar.setValue)

    def _on_scrollbar_changed(self, value: int) -> None:
        self.current_offset = value
        self.offset_changed.emit(value)

    def set_range(self, max_offset: int, page_step: int) -> None:
        self.max_offset_y = max_offset
        if max_offset > 0:
            self.scrollbar.setVisible(True)
            self.scrollbar.setRange(0, max_offset)
            self.scrollbar.setPageStep(page_step)
        else:
            self.scrollbar.setVisible(False)

    def set_offset(self, offset: int) -> None:
        self.current_offset = offset
        self.scrollbar.setValue(offset)

    def get_offset(self) -> int:
        return self.current_offset

    def render(self, painter: QPainter) -> None:
        # Скроллбар рисуется автоматически как виджет
        pass

    def handle_resize(self, width: int, height: int) -> None:
        self.scrollbar.setGeometry(
            width - self.const_width,
            0,
            self.const_width,
            height
        )
        self.scrollbar.raise_()