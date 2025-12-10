from decouple import config

environment = config("ENVIRONMENT", default="dev")

if environment == "prod":
    # For production environment
    from .prod import *
else:
    # For development environment
    from .dev import *