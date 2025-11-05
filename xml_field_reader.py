# xml_field_reader.py
import xml.etree.ElementTree as ET
from field_data import FieldData


class XMLFieldReader:
    def read_fields_from_xml(self, xml_path: str) -> list:
        fields_data = []

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            for field_elem in root.findall('field'):
                field_data = FieldData()

                # Базовые свойства
                field_data.widget_type = self._get_text(field_elem, 'type', 'label')
                field_data.x = int(self._get_text(field_elem, 'x', '0'))
                field_data.y = int(self._get_text(field_elem, 'y', '0'))
                field_data.width = int(self._get_text(field_elem, 'width', '100'))
                field_data.height = int(self._get_text(field_elem, 'height', '30'))
                field_data.default_text = self._get_text(field_elem, 'default_text', '')
                field_data.font_size = int(self._get_text(field_elem, 'font_size', '12'))
                field_data.field_id = self._get_text(field_elem, 'field_id', '')

                # Стилизация
                field_data.bold = self._get_bool(field_elem, 'bold', False)
                field_data.alignment = self._get_text(field_elem, 'alignment', 'left')
                field_data.background_color = self._get_text(field_elem, 'background_color', '')
                field_data.text_color = self._get_text(field_elem, 'text_color', '')

                # Опции для комбобоксов
                options_elem = field_elem.find('options')
                if options_elem is not None:
                    field_data.options = [option.text for option in options_elem.findall('option')]

                # Кастомные свойства
                custom_props_elem = field_elem.find('custom_properties')
                if custom_props_elem is not None:
                    for prop_elem in custom_props_elem:
                        field_data.custom_properties[prop_elem.tag] = prop_elem.text

                fields_data.append(field_data)

        except Exception as e:
            print(f"Ошибка при чтении XML: {e}")

        return fields_data

    def _get_text(self, element, tag, default):
        elem = element.find(tag)
        return elem.text if elem is not None else default

    def _get_bool(self, element, tag, default):
        text = self._get_text(element, tag, str(default))
        return text.lower() in ('true', '1', 'yes')