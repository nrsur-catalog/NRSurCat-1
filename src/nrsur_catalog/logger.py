import sys
import warnings

from loguru import logger

logger.remove(0)
logger.add(
    sys.stderr,
    format="|<blue>NURSUR CATALOG</blue>|{time:DD/MM HH:mm:ss}|{level}| <green>{message}</green> ",
    colorize=True,
    level="DEBUG",
)


warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
