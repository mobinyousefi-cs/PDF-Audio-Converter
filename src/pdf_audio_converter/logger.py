#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: logger.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Simple logging configuration used by CLI and GUI.

Usage: 
from .logger import get_logger

Notes: 
- Writes to console; you can extend to file handlers if needed.

===================================================================
"""
from __future__ import annotations

import logging
from logging import Logger


def get_logger(name: str = "pdf-audio") -> Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    h = logging.StreamHandler()
    fmt = "[%(levelname)s] %(asctime)s — %(message)s"
    h.setFormatter(logging.Formatter(fmt))
    logger.addHandler(h)
    return logger
