from loguru import logger


logger.add(
    f"logs/bot.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{function}:{line} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="3 days",
)


def get_logger():
    return logger
