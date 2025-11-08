import logging

_s_logger = None


CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG


def create_logger(name: str = 'postproc', level: int = INFO) -> logging.Logger:
    global _s_logger
    if _s_logger is None:
        _s_logger = logging.getLogger(name)
        _s_logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        _s_logger.addHandler(ch)
    return _s_logger


def get_logger() -> logging.Logger:
    global _s_logger
    if _s_logger is None:
        _s_logger = create_logger()
    return _s_logger
