import os
import logging

logger = logging.getLogger("GW:file_processor")


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        msg = f"{k} not supplied"
        logger.info(msg)
        exit(msg)
    return val


class Config(object):
    download_path = "/usr/src/app/storage"
    MINIO_URL = get_envar("MINIO_URL")
    MINIO_ACCESS_KEY = get_envar("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = get_envar("MINIO_SECRET_KEY")
    virustotal_url = get_envar("virustotal_url")
    virustotal_key = get_envar("virustotal_key")
