import sys
from loguru import logger
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

logger.remove()

# Console — readable
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - {message}",
    colorize=True,
)

# File — JSON lines for debugging
logger.add(
    "logs/glassbox.log",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    serialize=True,
)

log = logger