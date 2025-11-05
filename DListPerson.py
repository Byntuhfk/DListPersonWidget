# DListPerson.py
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QPainter, QMouseEvent, QWheelEvent, QResizeEvent
from background_renderer import BackgroundRenderer
from scrollbar_renderer import ScrollBarRenderer
from fields_renderer import FieldsRenderer
from debug_renderer import DebugRenderer


class DListPerson(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Инициализация рендереров
        self.background_renderer = BackgroundRenderer(self)
        self.scrollbar_renderer = ScrollBarRenderer(self)
        self.fields_renderer = FieldsRenderer(self)
        self.debug_renderer = DebugRenderer(self)

        self.setMouseTracking(True)
        self._initialize()

        QTimer.singleShot(0, self._delayed_initialization)

    def _delayed_initialization(self) -> None:
        """Отложенная инициализация после показа виджета"""
        self._update_fields_position()

    def _update_fields_position(self) -> None:
        """Обновляет позиции полей на основе текущего состояния"""
        bg_offset = self.background_renderer.get_background_offset()
        current_offset = self.scrollbar_renderer.get_offset()
        self.fields_renderer.set_background_offset(bg_offset.x(), current_offset)

    def _initialize(self) -> None:
        self._calculate_width()
        self._setup_connections()

    def _calculate_width(self) -> None:
        screen = QApplication.primaryScreen()
        screen_width = screen.geometry().width()
        fixed_width = int(screen_width * 3 / 5)
        self.background_renderer.set_fixed_width(fixed_width)

    def _setup_connections(self) -> None:
        # Связываем скроллбар с обновлением позиций
        self.scrollbar_renderer.offset_changed.connect(self._on_offset_changed)

    def _on_offset_changed(self, offset_y: int) -> None:
        self.background_renderer.set_offset_y(offset_y)
        self._update_fields_position()
        self.update()

    def set_background_image(self, path_to_image: str) -> None:
        self.background_renderer.set_background_image(path_to_image)
        self._update_scroll_limits()

    def set_fields(self, field_xml_path: str) -> None:
        self.fields_renderer.load_fields(field_xml_path)
        self._update_fields_position()

    def _update_scroll_limits(self) -> None:
        bg_width, bg_height = self.background_renderer.get_scaled_size()
        widget_height = self.height()

        if bg_height > widget_height:
            max_offset = bg_height - widget_height
            page_step = widget_height // 2
        else:
            max_offset = 0
            page_step = 0

        self.scrollbar_renderer.set_range(max_offset, page_step)

    def get_field_value(self, field_id: str) -> str:
        return self.fields_renderer.get_field_value(field_id)

    def set_field_value(self, field_id: str, value: str) -> None:
        self.fields_renderer.set_field_value(field_id, value)

    def set_debug_mode(self, enabled: bool) -> None:
        self.debug_renderer.set_debug_mode(enabled)
        self.update()

    def get_absolute_coordinates(self, widget_x: int, widget_y: int) -> QPoint:
        bg_offset = self.background_renderer.get_background_offset()
        absolute_x = widget_x - bg_offset.x()
        absolute_y = widget_y - bg_offset.y()
        return QPoint(absolute_x, absolute_y)

    # Обработчики событий Qt
    def paintEvent(self, event):
        painter = QPainter(self)

        # Рендерим фон
        self.background_renderer.render(painter)

        # Рендерим отладочную информацию через DebugRenderer
        self.debug_renderer.render(painter)

    def resizeEvent(self, event: QResizeEvent) -> None:
        width, height = event.size().width(), event.size().height()

        # Обновляем все рендереры
        self.background_renderer.handle_resize(width, height)
        self.scrollbar_renderer.handle_resize(width, height)
        self.fields_renderer.handle_resize(width, height)
        self.debug_renderer.handle_resize(width, height)

        self._update_scroll_limits()
        self._update_fields_position()
        super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        scroll_amount = -delta // 3
        current_offset = self.scrollbar_renderer.get_offset()
        new_offset = max(0, min(current_offset + scroll_amount, self.scrollbar_renderer.max_offset_y))
        self.scrollbar_renderer.set_offset(new_offset)
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.debug_renderer.set_mouse_position(event.position().toPoint())
        if self.debug_renderer.debug_mode:
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            clicked_widget = self.childAt(event.position().toPoint())

            from PySide6.QtWidgets import (QLineEdit, QTextEdit, QComboBox,
                                           QCheckBox, QSpinBox, QDoubleSpinBox)

            focusable_widgets = (QLineEdit, QTextEdit, QComboBox,
                                 QCheckBox, QSpinBox, QDoubleSpinBox)

            if not isinstance(clicked_widget, focusable_widgets):
                self.fields_renderer.clear_focus_from_fields()

        super().mousePressEvent(event)