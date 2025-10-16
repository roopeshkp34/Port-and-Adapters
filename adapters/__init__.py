"""
Adapters package - Contains all data source adapters.

This package provides a unified interface for different data sources
(databases, APIs, caches, etc.) through the adapter pattern.
"""

from adapters.factory import AdapterFactory, get_adapter

__all__ = ["AdapterFactory", "get_adapter"]

