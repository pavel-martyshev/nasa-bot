import builtins

from .config import app_config


def install():
    builtins.app_config = app_config


__all__ = ["app_config", "install"]
