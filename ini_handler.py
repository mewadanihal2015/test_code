import re
from safe_writer import atomic_write

class IniHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, "r") as f:
            self.lines = f.readlines()

    def _convert_type(self, value):
        if value.lower() in ["true", "false"]:
            return value.lower() == "true"
        if re.match(r"^\d+$", value):
            return int(value)
        if re.match(r"^\d+\.\d+$", value):
            return float(value)
        return value

    def get(self, section, key):
        current_section = None

        for line in self.lines:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1]

            elif "=" in stripped and current_section == section:
                k, v = map(str.strip, stripped.split("=", 1))
                if k == key:
                    return self._convert_type(v)

        return None

    def set(self, section, key, value):
        current_section = None

        for i, line in enumerate(self.lines):
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1]

            elif "=" in stripped and current_section == section:
                k, _ = map(str.strip, stripped.split("=", 1))
                if k == key:
                    self.lines[i] = f"{key} = {value}\n"
                    return

        # add key if not found
        for i, line in enumerate(self.lines):
            if line.strip() == f"[{section}]":
                self.lines.insert(i + 1, f"{key} = {value}\n")
                return

        # add section if missing
        self.lines.append(f"\n[{section}]\n{key} = {value}\n")

    def save(self):
        atomic_write(self.file_path, "".join(self.lines))
