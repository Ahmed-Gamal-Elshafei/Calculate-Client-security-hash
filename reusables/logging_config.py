import logging


logging.basicConfig(
    filename="../project.log",
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)