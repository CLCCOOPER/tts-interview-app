"""
Very small helper that maps friendly names -> ElevenLabs voice_id.
Feel free to extend the VOICE_MAP dictionary.
"""
from VOICE_ID import voices  # noqa: this is your JSON list

# build simple lookup: key is lower-cased pretty name, value is voice_id
VOICE_MAP = {v["name"].lower(): v["voice_id"] for v in voices}

def get_voice_id(friendly: str | None) -> str:
    """
    Returns a valid ElevenLabs voice_id.
    If friendly is None or unrecognised, default to the first voice.
    """
    if not friendly:
        return voices[0]["voice_id"]

    key = friendly.lower()
    return VOICE_MAP.get(key, voices[0]["voice_id"])
