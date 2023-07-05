import logging
import sys
import warnings

from loguru import logger

logger.remove(0)
logger.add(
    sys.stderr,
    format="|<blue>NURSUR CATALOG</blue>|{time:DD/MM HH:mm:ss}|{level}| <green>{message}</green> ",
    colorize=True,
    level="INFO",
)


warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
