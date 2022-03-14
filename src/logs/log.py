from loguru import logger
import sys

#logger.add("ns_2d_aa",format="{message}")
logger.remove()
fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <cyan>{level}</cyan> | {message}"
logger.add(sys.stdout, format=fmt)
#logger.add("ns_2d_aa",format="{message}")
logger.add("ns_2d_aa",format=fmt)
logger.info("hello")
