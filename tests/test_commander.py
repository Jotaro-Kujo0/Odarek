import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "odradek-core"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.voice.commander import Commander


def test_commander_initializes_without_errors():
    commander = Commander()
    assert commander is not None
    assert commander.recognizer is None
    assert commander.audio_stream is None
