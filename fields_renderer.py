# fields_renderer.py
from PySide6.QtGui import QPainter
from field_manager import FieldManager
from renderer_interface import RendererInterface


class FieldsRenderer(RendererInterface):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.field_manager = FieldManager(parent)
        self.background_offset_x: int = 0
        self.offset_y: int = 0

    def load_fields(self, xml_path: str) -> None:
        self.field_manager.load_from_xml(xml_path)
        self._update_fields_positions()

    def set_background_offset(self, offset_x: int, offset_y: int) -> None:
        self.background_offset_x = offset_x
        self.offset_y = offset_y
        self._update_fields_positions()

    def _update_fields_positions(self) -> None:
        self.field_manager.update_positions(self.background_offset_x, self.offset_y)

    def get_field_value(self, field_id: str) -> str:
        return self.field_manager.get_value(field_id)

    def set_field_value(self, field_id: str, value: str) -> None:
        self.field_manager.set_value(field_id, value)

    def register_custom_widget(self, widget_type: str, creator_func):
        self.field_manager.register_custom_widget(widget_type, creator_func)

    def clear_focus_from_fields(self) -> None:
        self.parent.setFocus()
        for widget in self.field_manager.fields.values():
            widget.clearFocus()

    def render(self, painter: QPainter) -> None:
        # Поля ввода рисуются автоматически как виджеты
        pass

    def handle_resize(self, width: int, height: int) -> None:
        self._update_fields_positions()