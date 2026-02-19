import json
import os

# Directory for internal saves (relative to app root)
SAVES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saves")


class FileHandler:
    @staticmethod
    def _ensure_saves_dir():
        """Create the saves directory if it doesn't exist"""
        os.makedirs(SAVES_DIR, exist_ok=True)

    @staticmethod
    def list_saves():
        """List all saved layout names (without .json extension)"""
        FileHandler._ensure_saves_dir()
        saves = []
        for f in os.listdir(SAVES_DIR):
            if f.endswith(".json"):
                saves.append(f[:-5])  # Remove .json
        saves.sort()
        return saves

    @staticmethod
    def save_internal(name, data):
        """Save a layout internally with the given name"""
        FileHandler._ensure_saves_dir()
        # Sanitize filename
        safe_name = "".join(c for c in name if c not in r'\/:*?"<>|').strip()
        if not safe_name:
            safe_name = "Sem Nome"
        filepath = os.path.join(SAVES_DIR, f"{safe_name}.json")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    @staticmethod
    def load_internal(name):
        """Load a layout by name from internal storage"""
        filepath = os.path.join(SAVES_DIR, f"{name}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading file: {e}")
            return None

    @staticmethod
    def delete_save(name):
        """Delete a saved layout by name"""
        filepath = os.path.join(SAVES_DIR, f"{name}.json")
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
        return False

    # Keep old methods for backward compatibility
    @staticmethod
    def save_layout(data, filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    @staticmethod
    def load_layout(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
