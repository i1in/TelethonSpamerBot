import importlib
import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

class ModuleManager:
    def __init__(self, base_folder: Path):
        self.base_folder = base_folder
        self.modules = {
            'handlers': self.base_folder / "handlers",
            'events': self.base_folder / "events"
        }
        parent_folder = str(self.base_folder)
        if parent_folder not in sys.path:
            sys.path.append(parent_folder)

    def register_module(self, module_prefix: str):
        folder = self.modules.get(module_prefix)
        if folder and folder.exists():
            for filename in os.listdir(folder):
                if filename.endswith('.py') and not filename.startswith('__'):
                    module_name = f"{module_prefix}.{filename[:-3]}"
                    importlib.import_module(module_name)
                    logging.info(f"Зарегистрирован модуль {module_name}")
        else:
            logging.warning(f"Папка для модуля '{module_prefix}' не найдена.")

    def register_all(self):
        for module_prefix in self.modules:
            self.register_module(module_prefix)

def register():
    base_folder = Path(__file__).resolve().parent
    module_manager = ModuleManager(base_folder)

    module_manager.register_all()