try:
    from src.api import app
except ModuleNotFoundError:
    from api import app
