import os


def get_data_inbound_dir():
    return os.getenv("DATA_INBOUND_DIR", "./data/inbound")


def get_data_outbound_dir():
    return os.getenv("DATA_OUTBOUND_DIR", "./data/outbound")


def get_mongo_uri():
    return os.getenv("MONGO_URI", "mongodb://localhost:27017/tractian")


DB_NAME = "tractian"
COLLECTION_NAME = "workorders"
