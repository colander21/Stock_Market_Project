import logging
from extract import run as extract_run
from transform import run as transform_run
from load import run as load_run

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    handlers=[
        logging.FileHandler("../logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info('Starting ETL pipeline')
    
    try:
        extract_run()
        transform_run()
        load_run()
        logging.info('Pipeline run successful')
    except Exception as e:
        logging.error(f"Pipeline run failed: {e}", exc_info=True)