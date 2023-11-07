"""Enum helpers"""


from sqlalchemy import Enum


def enum_serializer(obj):
    """
    Custom JSON serializer for UserStatusEnums"""
    if isinstance(obj, Enum):
        return obj.value

    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')