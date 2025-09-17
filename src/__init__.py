"""
FinTech Data Curator - Source Package
"""

from .config import Config
from .data_collector import FinancialDataCollector
from .structured_data import StructuredDataCollector
from .unstructured_data import UnstructuredDataCollector
from .utils import setup_logging

__version__ = "1.0.0"
__author__ = "CS4063 Student"

__all__ = [
    'Config',
    'FinancialDataCollector',
    'StructuredDataCollector', 
    'UnstructuredDataCollector',
    'setup_logging'
]