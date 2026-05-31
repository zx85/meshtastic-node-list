import threading
import time
import logging
import meshtastic.serial_interface
from includes.db import upsert_nodes

logger = logging.getLogger(__name__)


def update_nodes_task(dev_path):
    logger.info(f"Starting Meshtastic poller on {dev_path}")
    while True:
        interface = None
        try:
            # Connect to the Meshtastic device
            interface = meshtastic.serial_interface.SerialInterface(dev_path)
            while True:
                nodes = interface.nodes
                if nodes:
                    upsert_nodes(nodes)
                time.sleep(60)  # Poll for updates every minute
        except Exception as e:
            logger.error(f"Meshtastic poller error: {e}. Retrying in 30s...")
            time.sleep(30)
        finally:
            if interface:
                try:
                    interface.close()
                except:
                    pass


def start_poller(dev_path):
    thread = threading.Thread(target=update_nodes_task, args=(dev_path,), daemon=True)
    thread.start()
