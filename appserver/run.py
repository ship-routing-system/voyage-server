from .app import create_app
from .config import DevConfig

# gunicorn --bind 0.0.0.0:8890 --workers=2 appserver.run:app
app = create_app(DevConfig())
