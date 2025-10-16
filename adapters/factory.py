"""
Adapter Factory

This module provides a factory pattern for creating and managing adapters.
It supports dynamic registration of new adapters and maintains singleton instances.
"""

from typing import Dict, Type
from adapters.database.base import BaseAdapter


class AdapterFactory:
    """
    Factory class for creating and managing adapters.
    
    This factory uses the singleton pattern to ensure only one instance
    of each adapter type exists. It also supports dynamic registration
    of new adapter types.
    """
    
    # Registry of adapter types
    _registry: Dict[str, Type[BaseAdapter]] = {}
    
    # Cache of adapter instances (singleton pattern)
    _instances: Dict[str, BaseAdapter] = {}
    
    @classmethod
    def register(cls, name: str, adapter_class: Type[BaseAdapter]) -> None:
        """
        Register a new adapter type.
        
        Args:
            name: Unique identifier for the adapter (e.g., 'postgres', 'mysql')
            adapter_class: The adapter class to register
            
        Raises:
            ValueError: If the adapter name is already registered
        """
        if name in cls._registry:
            raise ValueError(f"Adapter '{name}' is already registered")
        
        if not issubclass(adapter_class, BaseAdapter):
            raise TypeError(f"Adapter class must inherit from BaseAdapter")
        
        cls._registry[name] = adapter_class
    
    @classmethod
    def unregister(cls, name: str) -> None:
        """
        Unregister an adapter type.
        
        Args:
            name: Unique identifier of the adapter to unregister
        """
        if name in cls._registry:
            del cls._registry[name]
        if name in cls._instances:
            del cls._instances[name]
    
    @classmethod
    def create(cls, name: str) -> BaseAdapter:
        """
        Create or retrieve an adapter instance.
        
        Uses singleton pattern - returns existing instance if available,
        otherwise creates a new one.
        
        Args:
            name: Unique identifier of the adapter to create
            
        Returns:
            Instance of the requested adapter
            
        Raises:
            ValueError: If the adapter name is not registered
        """
        # Return cached instance if it exists
        if name in cls._instances:
            return cls._instances[name]
        
        # Check if adapter is registered
        if name not in cls._registry:
            raise ValueError(
                f"Adapter '{name}' is not registered. "
                f"Available adapters: {list(cls._registry.keys())}"
            )
        
        # Create new instance and cache it
        adapter_class = cls._registry[name]
        instance = adapter_class()
        cls._instances[name] = instance
        
        return instance
    
    @classmethod
    def get_registered_adapters(cls) -> list[str]:
        """
        Get list of all registered adapter names.
        
        Returns:
            List of registered adapter names
        """
        return list(cls._registry.keys())
    
    @classmethod
    def reset(cls) -> None:
        """
        Reset all adapter instances.
        
        Useful for testing or when you need to recreate adapters.
        Does not clear the registry.
        """
        cls._instances = {}
    
    @classmethod
    def clear_registry(cls) -> None:
        """
        Clear the entire adapter registry and all instances.
        
        Warning: This will remove all registered adapters.
        Use with caution!
        """
        cls._registry = {}
        cls._instances = {}


def get_adapter(name: str) -> BaseAdapter:
    """
    Convenience function to get an adapter instance.
    
    Args:
        name: Unique identifier of the adapter (e.g., 'postgres', 'mysql')
        
    Returns:
        Instance of the requested adapter
        
    Raises:
        ValueError: If the adapter name is not registered
    """
    return AdapterFactory.create(name)


# Auto-register default database adapters
def _register_default_adapters():
    """Register the default database adapters."""
    try:
        from adapters.database import PostgresAdapter
        from adapters.database import MySQLAdapter
        
        AdapterFactory.register('postgres', PostgresAdapter)
        AdapterFactory.register('mysql', MySQLAdapter)
    except ImportError as e:
        # If imports fail, just log it (in production you might want proper logging)
        print(f"Warning: Could not register default adapters: {e}")


# Register adapters when module is imported
_register_default_adapters()

