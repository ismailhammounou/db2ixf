# coding: utf-8
"""Tests package"""
from pathlib import Path

# Root directory
TEST_DIR = Path(__file__).resolve().parent  # PROJECT_DIR/tests
ROOT_DIR = TEST_DIR.parent

# Target directory for testing
TARGET_DIR = ROOT_DIR / "target"

# Resources directory
RESOURCES_DIR = TEST_DIR / "resources"
