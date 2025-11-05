from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit,
                               QCheckBox, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from abc import ABC, abstractmethod


class WidgetFactoryInterface(ABC):
    @abstractmethod
    def create_widget(self, field_data: 'FieldData') -> QWidget:
        pass


class DefaultWidgetFactory(WidgetFactoryInterface):
    def create_widget(self, field_data: 'FieldData') -> QWidget:
        if field_data.widget_type == "label":
            return self._create_label(field_data)
        elif field_data.widget_type == "line_edit":
            return self._create_line_edit(field_data)
        elif field_data.widget_type == "text_edit":
            return self._create_text_edit(field_data)
        elif field_data.widget_type == "checkbox":
            return self._create_checkbox(field_data)
        elif field_data.widget_type == "combo_box":
            return self._create_combo_box(field_data)
        elif field_data.widget_type == "custom":
            return self._create_custom_widget(field_data)
        else:
            # По умолчанию создаем label
            raise Exception(f"Ошибка WidgetFactory: Неизвестный тип поля \"{field_data.widget_type}\".")

    def _create_label(self, field_data: 'FieldData') -> QLabel:
        label = QLabel(field_data.default_text)
        self._apply_base_styles(label, field_data)
        self._apply_text_styles(label, field_data)
        return label

    def _create_line_edit(self, field_data: 'FieldData') -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setText(field_data.default_text)
        self._apply_base_styles(line_edit, field_data)
        self._apply_input_styles(line_edit, field_data)
        return line_edit

    def _create_text_edit(self, field_data: 'FieldData') -> QTextEdit:
        text_edit = QTextEdit()
        text_edit.setPlainText(field_data.default_text)
        self._apply_base_styles(text_edit, field_data)
        self._apply_input_styles(text_edit, field_data)
        return text_edit

    def _create_checkbox(self, field_data: 'FieldData') -> QCheckBox:
        checkbox = QCheckBox(field_data.default_text)

        # Для чекбокса применяем базовые стили, но не стили полей ввода
        self._apply_base_styles(checkbox, field_data)

        # Специальные стили для чекбокса
        if field_data.text_color:
            current_style = checkbox.styleSheet()
            checkbox.setStyleSheet(f"{current_style} color: {field_data.text_color};")

        return checkbox

    def _create_combo_box(self, field_data: 'FieldData') -> QComboBox:
        combo = QComboBox()

        # Добавляем опции если они есть
        if field_data.options:
            combo.addItems(field_data.options)

        # Устанавливаем текст по умолчанию если он есть в опциях
        if field_data.default_text and field_data.default_text in field_data.options:
            index = field_data.options.index(field_data.default_text)
            combo.setCurrentIndex(index)
        elif field_data.default_text:
            combo.setCurrentText(field_data.default_text)

        self._apply_base_styles(combo, field_data)
        self._apply_input_styles(combo, field_data)
        return combo

    def _create_custom_widget(self, field_data: 'FieldData') -> QWidget:
        """Создает кастомный виджет на основе настроек"""
        try:
            # Импортируем класс кастомного виджета по имени
            import importlib
            module_name, class_name = field_data.custom_widget_class.rsplit('.', 1)
            module = importlib.import_module(module_name)
            widget_class = getattr(module, class_name)

            # Создаем экземпляр виджета
            widget = widget_class(self.parent_widget)

            # Применяем базовые стили
            self._apply_base_styles(widget, field_data)

            # Устанавливаем кастомные свойства
            for prop_name, prop_value in field_data.custom_properties.items():
                if hasattr(widget, prop_name):
                    setattr(widget, prop_name, prop_value)

            return widget

        except Exception as e:
            print(f"Ошибка при создании кастомного виджета {field_data.custom_widget_class}: {e}")
            # Возвращаем заглушку в случае ошибки
            label = QLabel(f"Ошибка: {field_data.field_id}")
            label.setStyleSheet("background-color: red; color: white;")
            return label

    def _apply_base_styles(self, widget: QWidget, field_data: 'FieldData'):
        # Базовые стили для всех виджетов
        font = QFont()
        font.setPointSize(field_data.font_size)
        font.setBold(field_data.bold)
        widget.setFont(font)

        if field_data.background_color:
            widget.setStyleSheet(f"background-color: {field_data.background_color};")

    def _apply_text_styles(self, label: QLabel, field_data: 'FieldData'):
        # Стили специфичные для текстовых элементов
        alignment_map = {
            "left": Qt.AlignLeft,
            "center": Qt.AlignCenter,
            "right": Qt.AlignRight,
            "top": Qt.AlignTop,
            "bottom": Qt.AlignBottom
        }

        if field_data.alignment in alignment_map:
            label.setAlignment(alignment_map[field_data.alignment])

        if field_data.text_color:
            current_style = label.styleSheet()
            label.setStyleSheet(f"{current_style} color: {field_data.text_color};")

    def _apply_input_styles(self, input_widget: QWidget, field_data: 'FieldData'):
        # Стили для полей ввода
        style_sheet = """
            background-color: rgba(255, 255, 255, 0.3);
            border: 1px solid #cccccc;
            border-radius: 3px;
            padding: 2px 5px;
            color: black;
        """

        if field_data.background_color:
            style_sheet = style_sheet.replace("rgba(255, 255, 255, 0.3)", field_data.background_color)

        input_widget.setStyleSheet(style_sheet)