# Imports
import os
import sys
from pathlib import Path

import environ
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

# Initialize environment variables
env = environ.Env()

# Resolve the base directory of the project
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Add the project directory to the Python path
sys.path.append(str(BASE_DIR / "apps"))

# Set the Django settings module to use for the application
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    env.str(var="DJANGO_SETTINGS_MODULE", default="config.settings"),
)

# Get the ASGI application for the Django project
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
    }
)
