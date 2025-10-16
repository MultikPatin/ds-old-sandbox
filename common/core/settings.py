from typing import Any

from pydantic_settings import SettingsConfigDict

from .constants import SETTINGS_DEFAULTS

__all__ = ["set_model_config"]


def set_model_config(**kwargs: Any) -> SettingsConfigDict:
    for k in SETTINGS_DEFAULTS:
        if k not in kwargs:
            kwargs[k] = SETTINGS_DEFAULTS[k]
    return SettingsConfigDict(**kwargs)  # type: ignore
