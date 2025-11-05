# background_renderer.py
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QPoint, Qt
from renderer_interface import RendererInterface


class BackgroundRenderer(RendererInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image: QPixmap = QPixmap()
        self.scaled_background_image: QPixmap = QPixmap()
        self.fixed_width: int = 800
        self.offset_y: int = 0
        self.widget_width: int = 0
        self.widget_height: int = 0

    def set_background_image(self, path_to_image: str) -> None:
        pixmap = QPixmap(path_to_image)
        if not pixmap.isNull():
            self.background_image = pixmap
            self._update_scale()

    def set_fixed_width(self, width: int) -> None:
        self.fixed_width = width
        self._update_scale()

    def set_offset_y(self, offset_y: int) -> None:
        self.offset_y = offset_y

    def _update_scale(self) -> None:
        if not self.background_image.isNull():
            self.scaled_background_image = self.background_image.scaledToWidth(
                self.fixed_width, Qt.SmoothTransformation
            )

    def get_scaled_size(self) -> tuple[int, int]:
        """Возвращает размеры scaled изображения (width, height)"""
        if self.scaled_background_image.isNull():
            return 0, 0
        return self.scaled_background_image.width(), self.scaled_background_image.height()

    def get_background_offset(self) -> QPoint:
        """Вычисляет смещение фона для центрирования"""
        if self.scaled_background_image.isNull():
            return QPoint(0, 0)

        if self.scaled_background_image.width() >= self.widget_width:
            image_x = 0
        else:
            image_x = (self.widget_width - self.scaled_background_image.width()) // 2

        return QPoint(image_x, -self.offset_y)

    def render(self, painter: QPainter) -> None:
        if self.scaled_background_image.isNull():
            return

        bg_offset = self.get_background_offset()
        painter.drawPixmap(bg_offset.x(), bg_offset.y(), self.scaled_background_image)

    def handle_resize(self, width: int, height: int) -> None:
        self.widget_width = width
        self.widget_height = height