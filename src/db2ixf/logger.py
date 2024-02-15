# coding=utf-8
"""Centralized shared logger module"""
import logging

# Get a logger in debug level
logger = logging.getLogger("db2ixf")
logger.setLevel(logging.ERROR)

# Create formatter
_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(_format)

# Create handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(handler)

# What to import when doing `from db2ixf import *`
__all__ = ["logger"]
