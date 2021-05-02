from .app import create_app
from .config import LiveConfig


app = create_app(LiveConfig())