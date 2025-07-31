# remiel/modes.py

class ModeError(Exception):
    pass

class ModeManager:
    VALID_MODES = {
        "strict_mode": "MODE_STRICT",
        "dynamic_mode": "MODE_DYNAMIC",
        "universal_mode": "MODE_UNIVERSAL",
    }

    def __init__(self):
        self.current_mode = None

    def set_mode(self, raw_mode: str):
        raw_mode = raw_mode.strip()
        if raw_mode not in self.VALID_MODES:
            raise ModeError(f"[ModeError] Unknown mode '{raw_mode}'. Valid modes are: {', '.join(self.VALID_MODES.keys())}")
        self.current_mode = self.VALID_MODES[raw_mode]
        print(f"[Mode] Mode declared: {self.current_mode}")

    def require_mode(self):
        if not self.current_mode:
            raise ModeError("[ModeError] No mode declared. Your program must start with strict_mode, dynamic_mode, or universal_mode.")

    def is_strict(self):
        return self.current_mode == "MODE_STRICT"

    def is_dynamic(self):
        return self.current_mode == "MODE_DYNAMIC"

    def is_universal(self):
        return self.current_mode == "MODE_UNIVERSAL"

# Singleton mode manager
mode_manager = ModeManager()
