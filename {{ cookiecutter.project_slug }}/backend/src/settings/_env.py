"""
Environment variable utilities with type conversion.

Load order: ``backend/.env`` is applied (via python-dotenv) before any ``Env`` lookups,
so values are available on ``os.environ``.

Usage in settings modules::

    from ._env import env

    debug = env.get_bool("DJANGO_DEBUG", default=False, required=False)
    secret = env.get_str("DJANGO_SECRET_KEY", required=True)
"""
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(_BACKEND_DIR / ".env", override=False)


class Env:
    """Environment variable loader with type conversion."""

    @staticmethod
    def get_str(
        key: str,
        default: str = "",
        required: bool = False,
    ) -> str:
        """
        Get string environment variable.

        Leading and trailing whitespace is stripped. Whitespace-only values are
        treated the same as unset (required raises; optional returns default).

        Args:
            key: Environment variable name
            default: Default value if not found (only used if required=False)
            required: If True, raise error if not set; if False, use default

        Returns:
            String value or default

        Raises:
            ValueError: If required=True and environment variable is not set
        """
        raw = os.environ.get(key)
        value = raw.strip() if raw is not None else ""
        if not value:
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default
        return value

    @staticmethod
    def get_int(
        key: str,
        default: int = 0,
        required: bool = False,
    ) -> int:
        """
        Get integer environment variable.

        Args:
            key: Environment variable name
            default: Default value if not found or invalid (only used if required=False)
            required: If True, raise error if not set; if False, use default

        Returns:
            Integer value or default

        Raises:
            ValueError: If required=True and environment variable is not set or invalid
        """
        value = os.environ.get(key)
        if value is None or value == "":
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            if required:
                raise ValueError(
                    f"Environment variable '{key}' has invalid integer value: '{value}'"
                )
            return default

    @staticmethod
    def get_float(
        key: str,
        default: float = 0.0,
        required: bool = False,
    ) -> float:
        """
        Get float environment variable.

        Args:
            key: Environment variable name
            default: Default value if not found or invalid (only used if required=False)
            required: If True, raise error if not set; if False, use default

        Returns:
            Float value or default

        Raises:
            ValueError: If required=True and environment variable is not set or invalid
        """
        value = os.environ.get(key)
        if value is None or value == "":
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            if required:
                raise ValueError(f"Environment variable '{key}' has invalid float value: '{value}'")
            return default

    @staticmethod
    def get_bool(
        key: str,
        default: bool = False,
        required: bool = False,
    ) -> bool:
        """
        Get boolean environment variable.

        Accepts: true, false, 1, 0, yes, no, on, off (case-insensitive)

        Args:
            key: Environment variable name
            default: Default value if not found or invalid (only used if required=False)
            required: If True, raise error if not set; if False, use default

        Returns:
            Boolean value or default

        Raises:
            ValueError: If required=True and environment variable is not set or invalid
        """
        value = os.environ.get(key)
        if value is None or value == "":
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default

        value_lower = str(value).lower().strip()
        true_values = {"true", "1", "yes", "on", "enabled"}
        false_values = {"false", "0", "no", "off", "disabled", ""}

        if value_lower in true_values:
            return True
        elif value_lower in false_values:
            return False
        else:
            if required:
                raise ValueError(
                    f"Environment variable '{key}' has invalid boolean value: '{value}'"
                )
            return default

    @staticmethod
    def get_list(
        key: str,
        default: list[str] | None = None,
        separator: str = ",",
        strip: bool = True,
        required: bool = False,
    ) -> list[str]:
        """
        Get list from environment variable.

        Supports:
        - Comma-separated values: "item1,item2,item3"
        - JSON array: '["item1", "item2", "item3"]'

        Args:
            key: Environment variable name
            default: Default list if not found (defaults to empty list, only used if required=False)
            separator: Separator for comma-separated values
            strip: Whether to strip whitespace from items
            required: If True, raise error if not set; if False, use default

        Returns:
            List of strings

        Raises:
            ValueError: If required=True and environment variable is not set
        """
        if default is None:
            default = []

        value = os.environ.get(key)
        if value is None or value == "":
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default

        # Try JSON first
        if value.strip().startswith("["):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except (json.JSONDecodeError, TypeError):
                pass

        # Fall back to separator-based parsing
        items = value.split(separator)
        if strip:
            items = [item.strip() for item in items]

        # Remove empty items
        return [item for item in items if item]

    @staticmethod
    def get_dict(
        key: str,
        default: dict[str, Any] | None = None,
        required: bool = False,
    ) -> dict[str, Any]:
        """
        Get dictionary from environment variable (JSON format).

        Args:
            key: Environment variable name
            default: Default dictionary if not found (defaults to empty dict, only used if required=False)
            required: If True, raise error if not set; if False, use default

        Returns:
            Dictionary parsed from JSON

        Raises:
            ValueError: If required=True and environment variable is not set or invalid
        """
        if default is None:
            default = {}

        value = os.environ.get(key)
        if value is None or value == "":
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default

        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
            else:
                if required:
                    raise ValueError(f"Environment variable '{key}' is not a valid JSON object")
                return default
        except (json.JSONDecodeError, TypeError) as e:
            if required:
                raise ValueError(f"Environment variable '{key}' has invalid JSON: {str(e)}")
            return default

    @staticmethod
    def get(
        key: str,
        default: Any = None,
        var_type: str = "str",
        required: bool = False,
    ) -> str | int | float | bool | list[str] | dict[str, Any]:
        """
        Get environment variable with automatic type conversion.

        Args:
            key: Environment variable name
            default: Default value if not found (only used if required=False)
            var_type: Type to convert to ("str", "int", "float", "bool", "list", "dict")
            required: If True, raise error if not set; if False, use default

        Returns:
            Converted value based on var_type

        Raises:
            ValueError: If required=True and environment variable is not set or invalid
        """
        type_map = {
            "str": Env.get_str,
            "int": Env.get_int,
            "float": Env.get_float,
            "bool": Env.get_bool,
            "list": Env.get_list,
            "dict": Env.get_dict,
        }

        converter = type_map.get(var_type.lower(), Env.get_str)
        if default is None:
            if var_type == "list":
                default = []
            elif var_type == "dict":
                default = {}
            elif var_type == "bool":
                default = False
            elif var_type in ("int", "float"):
                default = 0
            else:
                default = ""

        return converter(key, default, required=required)

    @staticmethod
    def require(
        key: str,
        var_type: str = "str",
    ) -> Any:
        """
        Require an environment variable to be set (raises error if missing).

        Args:
            key: Environment variable name
            var_type: Type to convert to

        Returns:
            Converted value

        Raises:
            ValueError: If environment variable is not set
        """
        value = os.environ.get(key)
        if value is None or value == "":
            raise ValueError(f"Required environment variable '{key}' is not set")

        return Env.get(key, var_type=var_type, required=True)


# Singleton used across settings modules
env = Env()
