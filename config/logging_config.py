import logging
import sys

def setup_logger():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create and return logger
    logger = logging.getLogger(__name__)
    
    return logger