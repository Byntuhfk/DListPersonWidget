# field_manager.py
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QCheckBox, QComboBox
from widget_factory import DefaultWidgetFactory
from field_data import FieldData


class FieldManager:
    def __init__(self, parent_widget: QWidget) -> None:
        self.parent_widget: QWidget = parent_widget
        self.fields: dict = {}
        self.field_data: dict = {}
        self.widget_factory = DefaultWidgetFactory()

    def load_from_xml(self, xml_path: str) -> None:
        from xml_field_reader import XMLFieldReader
        reader = XMLFieldReader()
        fields_data: list[FieldData] = reader.read_fields_from_xml(xml_path)

        for field_data in fields_data:
            self.create_field(field_data)

    def create_field(self, field_data: FieldData) -> None:
        """Создает поле на основе FieldData"""
        widget = self.widget_factory.create_widget(field_data)

        # Устанавливаем родительский виджет
        widget.setParent(self.parent_widget)

        # Сохраняем оригинальные координаты
        widget.original_x = field_data.x
        widget.original_y = field_data.y
        widget.field_id = field_data.field_id

        # Устанавливаем размер
        widget.setMinimumSize(field_data.width, field_data.height)

        # Сохраняем в словари
        self.fields[field_data.field_id] = widget
        self.field_data[field_data.field_id] = field_data

        return widget

    def register_custom_widget(self, widget_type: str, creator_func):
        """Регистрирует кастомный виджет"""
        self.widget_factory.register_custom_widget(widget_type, creator_func)

    def update_positions(self, background_offset_x: int, offset_y: int) -> None:
        """Обновляет позиции всех полей"""
        for field_id, widget in self.fields.items():
            field_data = self.field_data[field_id]
            absolute_x = background_offset_x + field_data.x
            absolute_y = field_data.y - offset_y
            widget.setGeometry(absolute_x, absolute_y, field_data.width, field_data.height)

    def get_value(self, field_id: str):
        """Возвращает значение поля"""
        widget = self.fields.get(field_id)
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QTextEdit):
            return widget.toPlainText()
        elif isinstance(widget, QLabel):
            return widget.text()
        elif isinstance(widget, QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        return None

    def set_value(self, field_id: str, value) -> None:
        """Устанавливает значение поля"""
        widget = self.fields.get(field_id)
        if isinstance(widget, QLineEdit):
            widget.setText(value)
        elif isinstance(widget, QTextEdit):
            widget.setPlainText(value)
        elif isinstance(widget, QLabel):
            widget.setText(value)
        elif isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))
        elif isinstance(widget, QComboBox):
            index = widget.findText(value)
            if index >= 0:
                widget.setCurrentIndex(index)

    def clear(self) -> None:
        """Очищает все поля"""
        for field in self.fields.values():
            field.deleteLater()
        self.fields.clear()
        self.field_data.clear()