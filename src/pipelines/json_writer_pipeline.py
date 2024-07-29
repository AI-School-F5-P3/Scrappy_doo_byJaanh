import json
import logging
import os

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.items = []
        logging.info(f"Spider opened: {spider.name}")

    def close_spider(self, spider):
        filepath = f"data/raw/{spider.name}.json"
        try:
            self.validate_json(self.items)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.items, f, ensure_ascii=False, indent=4)
            logging.info(f"Data successfully written to {filepath}")
        except Exception as e:
            logging.error(f"Error writing to {filepath}: {e}")

    def process_item(self, item, spider):
        cleaned_item = self.clean_item(item)
        if cleaned_item:
            self.items.append(cleaned_item)
            logging.info(f"Processed item: {cleaned_item}")
        else:
            logging.warning(f"Item skipped due to validation failure: {item}")
        return item

    def clean_item(self, item):
        try:
            # Realiza cualquier limpieza o validación de datos aquí
            cleaned_item = {}
            for key, value in item.items():
                if isinstance(value, str):
                    cleaned_item[key] = value.strip()
                else:
                    cleaned_item[key] = value
            return cleaned_item
        except Exception as e:
            logging.error(f"Error cleaning item {item}: {e}")
            return None

    def validate_json(self, items):
        try:
            json.dumps(items)
            logging.info("JSON validation passed")
        except json.JSONDecodeError as e:
            logging.error(f"JSON validation error: {e}")
            raise
