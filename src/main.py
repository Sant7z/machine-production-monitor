from data_reader import load_data
from validator import validate_mass
from database import create_table, insert_data
from logger import setup_logger

logger = setup_logger()

print("Production Monitoring System\n")

logger.info("System started")

data = load_data("data/production_data.csv")
logger.info("Production data loaded")

create_table()
insert_data(data)
logger.info("Data inserted into database")

alerts = validate_mass(data)

if alerts:
    for alert in alerts:
        print("⚠️", alert)
        logger.warning(alert)
else:
    print("No anomalies detected")
    logger.info("No anomalies detected")

logger.info("System finished")