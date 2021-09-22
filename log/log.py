#  logger.py
import logging
import os
import yaml
import logging.config

def setupLogging(default_path='log/config.yaml', default_level=logging.INFO):
    path = default_path
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    # subpressing logging information from third-party pakcages
    for name, logger in logging.root.manager.loggerDict.items():
        if not isinstance(logger, logging.PlaceHolder):
            logger.setLevel(logging.INFO) 

