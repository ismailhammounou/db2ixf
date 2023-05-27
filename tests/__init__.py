# coding: utf-8
"""Tests package"""
from os.path import abspath, dirname, join

# Root directory
TEST_DIR: str = abspath(dirname(__file__))  # PROJECT_DIR/tests
ROOT_DIR: str = abspath(dirname(TEST_DIR))

# Target directory for testing
TARGET_DIR: str = abspath(join(ROOT_DIR, "target"))
