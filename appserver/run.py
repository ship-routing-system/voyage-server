from .app import create_app
from .config import DevConfig

app = create_app(DevConfig())
