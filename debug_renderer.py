# debug_renderer.py
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PySide6.QtCore import Qt
from renderer_interface import RendererInterface


class DebugRenderer(RendererInterface):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.debug_mode: bool = False
        self.debug_mouse_pos: QPoint = QPoint(0, 0)

    def set_debug_mode(self, enabled: bool) -> None:
        self.debug_mode = enabled

    def set_mouse_position(self, pos: QPoint) -> None:
        self.debug_mouse_pos = pos

    def render(self, painter: QPainter) -> None:
        if not self.debug_mode:
            return

        self._draw_debug_info(painter)

    def _draw_debug_info(self, painter: QPainter) -> None:
        """Рисует отладочную информацию"""
        cross_pen = QPen(QColor(255, 0, 0, 180))
        cross_pen.setWidth(1)
        cross_pen.setStyle(Qt.DashLine)
        painter.setPen(cross_pen)

        # Рисуем перекрестие
        painter.drawLine(self.debug_mouse_pos.x(), 0, self.debug_mouse_pos.x(), self.parent.height())
        painter.drawLine(0, self.debug_mouse_pos.y(), self.parent.width(), self.debug_mouse_pos.y())

        # Вычисляем абсолютные координаты
        abs_coords = self.parent.get_absolute_coordinates(self.debug_mouse_pos.x(), self.debug_mouse_pos.y())

        # Подготавливаем текст
        coord_text = f"X: {abs_coords.x()}, Y: {abs_coords.y()}\nWidget: {self.debug_mouse_pos.x()}, {self.debug_mouse_pos.y()}"

        # Настраиваем фон для текста
        font_metrics = QFontMetrics(painter.font())
        text_rect = font_metrics.boundingRect(coord_text)
        text_rect.adjust(-2, -8, 2, 8)

        # Позиционируем текст
        text_pos = QPoint(self.debug_mouse_pos.x() + 10, self.debug_mouse_pos.y() - text_rect.height() - 10)

        if text_pos.x() + text_rect.width() > self.parent.width():
            text_pos.setX(self.debug_mouse_pos.x() - text_rect.width() - 10)

        if text_pos.y() < 0:
            text_pos.setY(self.debug_mouse_pos.y() + 20)

        text_rect.moveTo(text_pos)

        # Рисуем фон и текст
        painter.fillRect(text_rect, QColor(0, 0, 0, 180))
        text_pen = QPen(QColor(255, 255, 255))
        painter.setPen(text_pen)
        painter.drawText(text_rect, Qt.AlignCenter, coord_text)

    def handle_resize(self, width: int, height: int) -> None:
        # Для DebugRenderer ресайз не требует специальной обработки
        pass