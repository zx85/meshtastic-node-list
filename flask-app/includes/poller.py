import threading
import time
import logging
import meshtastic.serial_interface
from includes.db import upsert_nodes, prune_nodes

logger = logging.getLogger(__name__)


def update_nodes_task(dev_path):
    logger.info(f"Starting Meshtastic poller on {dev_path}")
    last_reboot_time = time.time()

    while True:
        interface = None
        try:
            # Connect to the Meshtastic device
            interface = meshtastic.serial_interface.SerialInterface(dev_path)

            # Synchronize time immediately upon connection/reconnection
            try:
                interface.localNode.setTime()
                logger.info("Local node time synchronized with system time.")
            except Exception as e:
                logger.error(f"Failed to set node time: {e}")

            while True:
                current_nodes = interface.nodes
                if current_nodes:
                    to_upsert = {}
                    active_ids = []

                    for num, data in current_nodes.items():
                        node_id = data.get("user", {}).get("id")

                        if not data.get("lastHeard"):
                            logger.info(
                                f"Removing zombie node {node_id or num} from device..."
                            )
                            try:
                                interface.localNode.removeNode(num)
                            except Exception as e:
                                logger.error(
                                    f"Failed device removal for {node_id}: {e}"
                                )
                        else:
                            to_upsert[num] = data
                            if node_id:
                                active_ids.append(node_id)

                    if to_upsert:
                        upsert_nodes(to_upsert)
                    if active_ids:
                        prune_nodes(active_ids)

                # Check if 6 hours (21600 seconds) have passed for the reboot cycle
                if time.time() - last_reboot_time > 21600:
                    logger.info("6-hour interval reached. Triggering node reboot...")
                    interface.localNode.reboot()
                    last_reboot_time = time.time()
                    # Break inner loop to allow connection logic to handle the device going offline
                    break

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
