class SmartAutoCorrection:
    """
    Listens to compatibility errors and suggests immediate fixes to the user.
    """
    
    def __init__(self):
        self.correction_map = {
            "Fork wheel size does not match frame specification": self._fix_wheel_size_mismatch,
            "Boost spacing mismatch": self._fix_boost_mismatch,
            "Drivetrain components speed count mismatch": self._fix_drivetrain_mismatch
        }

    def generate_fixes(self, compatibility_errors: list, state_dict: dict) -> list:
        fixes = []
        for error in compatibility_errors:
            for error_key, handler in self.correction_map.items():
                if error_key in error:
                    fix = handler(state_dict)
                    if fix:
                        fixes.append(fix)
        return fixes

    def _fix_wheel_size_mismatch(self, state_dict):
        frame_ws = state_dict.get('frame', {}).get('front_wheel_size')
        if frame_ws:
            return f"Auto-Fix: Change fork wheel size to {frame_ws} to match the frame."
        return "Auto-Fix: Align fork and frame wheel sizes."

    def _fix_boost_mismatch(self, state_dict):
        frame_boost = state_dict.get('frame', {}).get('is_boost')
        if frame_boost is not None:
            status = "Boost" if frame_boost else "Non-Boost"
            return f"Auto-Fix: Change wheelset to {status} to match the frame."
        return "Auto-Fix: Ensure both wheelset and frame are Boost or Non-Boost."

    def _fix_drivetrain_mismatch(self, state_dict):
        cassette_speeds = state_dict.get('drivetrain', {}).get('cassette_speeds')
        if cassette_speeds:
            return f"Auto-Fix: Change derailleur and shifter to {cassette_speeds}-speed."
        return "Auto-Fix: Ensure derailleur, shifter, and cassette speed counts match."

smart_auto_correction = SmartAutoCorrection()
