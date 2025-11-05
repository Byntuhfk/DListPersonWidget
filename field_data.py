# field_data.py
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FieldData:
    """Расширенный класс для хранения данных о поле"""
    widget_type: str = "label"  # "label", "line_edit", "text_edit", "checkbox", "combo_box", "custom"
    x: int = 0
    y: int = 0
    width: int = 100
    height: int = 30
    default_text: str = ""
    font_size: int = 12
    field_id: str = ""

    # Стилизация
    bold: bool = False
    alignment: str = "left"  # "left", "center", "right", "top", "bottom"
    background_color: str = ""  # CSS цвет
    text_color: str = ""  # CSS цвет

    # Для выпадающих списков
    options: list = None

    # Для кастомных виджетов
    custom_widget_class: str = ""
    custom_properties: Dict[str, Any] = None

    def __post_init__(self):
        if self.options is None:
            self.options = []
        if self.custom_properties is None:
            self.custom_properties = {}