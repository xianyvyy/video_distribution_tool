"""
Platform adapter layer: isolates platform API and mock differences.
Service layer calls unified interface only.
"""
from .base_adapter import BasePlatformAdapter

__all__ = ["BasePlatformAdapter"]
