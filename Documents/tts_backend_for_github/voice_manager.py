
# voice_manager.py

# Dictionary of voice options
VOICE_OPTIONS = {
    "default": "EXAVITQu4vr4xnSDxMaL",
    "female_soft": "21m00Tcm4TlvDq8ikWAM", 
    "male_deep": "pNInz6obpgDQGcFmaJgB",
    "narrator": "AZnzlk1XvdvUeBnXmlld"
}

def get_voice_id(voice_name: str = "default") -> str:
    """
    Returns the voice ID for the given voice name.
    Defaults to the 'default' voice ID if name not found.
    """
    return VOICE_OPTIONS.get(voice_name, VOICE_OPTIONS["default"])

def list_available_voices() -> list:
    """
    Returns a list of available voice names.
    """
    return list(VOICE_OPTIONS.keys())
