    
import logging
import sys

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # StreamHandler für die Konsole
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    return logger