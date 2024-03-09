import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
f_format = logging.Formatter(
    '%(asctime)s %(name)-22s %(levelname)-8s [%(lineno)-3s] %(message)s',
    "%Y-%m-%d %H:%M"
)
f_handler = logging.FileHandler("server.log")
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)