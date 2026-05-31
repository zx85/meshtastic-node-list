import sqlite3
import os

DB_PATH = os.environ.get("node_db_file", "/app/node_data/nodes.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                long_name TEXT,
                short_name TEXT,
                hw_model TEXT,
                public_key TEXT,
                role TEXT,
                latitude REAL,
                longitude REAL,
                altitude INTEGER,
                battery_level INTEGER,
                channel_utilization REAL,
                air_util_tx REAL,
                snr REAL,
                hops_away INTEGER,
                last_heard INTEGER,
                fav INTEGER
            )
        """)
        conn.commit()


def upsert_nodes(nodes_dict):
    with get_db_connection() as conn:
        for node_id, data in nodes_dict.items():
            user = data.get("user", {})
            pos = data.get("position", {})
            metrics = data.get("deviceMetrics", {})

            conn.execute(
                """
                INSERT INTO nodes (
                    node_id, long_name, short_name, hw_model, public_key, role,
                    latitude, longitude, altitude, battery_level, 
                    channel_utilization, air_util_tx, snr, hops_away, last_heard, fav
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(node_id) DO UPDATE SET
                    long_name=excluded.long_name, short_name=excluded.short_name,
                    hw_model=excluded.hw_model, public_key=excluded.public_key,
                    role=excluded.role, latitude=excluded.latitude,
                    longitude=excluded.longitude, altitude=excluded.altitude,
                    battery_level=excluded.battery_level, channel_utilization=excluded.channel_utilization,
                    air_util_tx=excluded.air_util_tx, snr=excluded.snr,
                    hops_away=excluded.hops_away, last_heard=excluded.last_heard, fav=excluded.fav
            """,
                (
                    user.get("id"),
                    user.get("longName"),
                    user.get("shortName"),
                    user.get("hwModel"),
                    user.get("publicKey"),
                    str(user.get("role", "N/A")),
                    pos.get("latitude"),
                    pos.get("longitude"),
                    pos.get("altitude"),
                    metrics.get("batteryLevel"),
                    metrics.get("channelUtilization"),
                    metrics.get("airUtilTx"),
                    data.get("snr"),
                    data.get("hopsAway"),
                    data.get("lastHeard"),
                    1 if data.get("fav") else 0,
                ),
            )
        conn.commit()


def prune_nodes(active_node_ids):
    """Remove nodes from the database that are no longer in the provided list of IDs."""
    if not active_node_ids:
        return
    with get_db_connection() as conn:
        placeholders = ",".join("?" for _ in active_node_ids)
        conn.execute(
            f"DELETE FROM nodes WHERE node_id NOT IN ({placeholders})",
            list(active_node_ids),
        )
        conn.commit()
