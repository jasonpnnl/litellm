import os

def require_env_var(var_name):
    """Require environment variable to be set."""
    value = os.getenv(var_name)
    if value is None:
        raise Exception(f"Environment variable {var_name} is not set.")
    return value