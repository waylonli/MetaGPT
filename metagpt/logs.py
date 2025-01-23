#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/6/1 12:41
@Author  : alexanderwu
@File    : logs.py
"""

import sys
import os
from datetime import datetime

from loguru import logger as _logger

from metagpt.const import METAGPT_ROOT

_print_level = "INFO"


def define_log_level(print_level="INFO", logfile_level="DEBUG", name: str = None):
    """Adjust the log level to above level"""
    global _print_level
    _print_level = print_level

    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d")
    log_name = f"{name}_{formatted_date}" if name else formatted_date  # name a log with prefix name
    # get the max number of folders in the logs directory
    logs_dirs = [int(x.name) for x in METAGPT_ROOT.glob("logs/*") if x.is_dir()]
    new_log_dir = str(max(logs_dirs)+1) if len(logs_dirs) > 0 else "1"
    os.makedirs(METAGPT_ROOT / f"logs/{new_log_dir}", exist_ok=False)
    log_name = new_log_dir + "/" + log_name

    _logger.remove()
    _logger.add(sys.stderr, level=print_level)
    _logger.add(METAGPT_ROOT / f"logs/{log_name}.txt", level=logfile_level)
    return _logger


logger = define_log_level()


def log_llm_stream(msg):
    _llm_stream_log(msg)


def set_llm_stream_logfunc(func):
    global _llm_stream_log
    _llm_stream_log = func


def _llm_stream_log(msg):
    if _print_level in ["INFO"]:
        print(msg, end="")
