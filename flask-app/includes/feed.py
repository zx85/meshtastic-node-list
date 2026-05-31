from datetime import datetime
from includes.maths import line_of_sight_distance

google_prefix = "https://www.google.com/maps/place/"
google_suffix = ",12z/data=!4m4!3m3!8m2!3d52.2803!4d0.657!5m1!1e1"

ROLE_MAP = {
    0: "client",
    1: "client_mute",
    2: "client_base",
    3: "tracker",
    4: "repeater",
    5: "router",
    6: "router",
}


def format_since(epoch):
    """Calculates a human-readable string for time since epoch."""
    if not epoch:
        return "N/A"
    diff = datetime.now().timestamp() - epoch
    if diff < 60:
        return "Just now"
    if diff < 3600:
        return f"{int(diff//60)}m ago"
    if diff < 86400:
        return f"{int(diff//3600)}h ago"
    return f"{int(diff//86400)}d ago"


def parse_feed(rows):
    """
    Convert database rows into a list of lists for the template.
    """
    if not rows:
        return [], []

    headers = [
        "Number",
        "User",
        "AKA",
        "Hardware",
        "Role",
        "Lat/Long",
        "Altitude",
        "Battery",
        "Dist",
        "SNR",
        "Hops",
        "LastHeard",
        "Since",
    ]

    # Use the first row as the 'Home' reference for distance calculation
    home_row = rows[0]
    home_coords = [home_row["latitude"], home_row["longitude"], home_row["altitude"]]

    table_data = []
    for i, row in enumerate(rows):
        # Coordinates and Maps link
        lat_long = "N/A"
        if row["latitude"] and row["longitude"]:
            l1, l2 = row["latitude"], row["longitude"]
            url = f"{google_prefix}{l1}+{l2}/@{l1},{l2}{google_suffix}"
            lat_long = f'<A HREF="{url}" TARGET="maps">{l1}, {l2}</A>'

        # Distance calculation
        dist = "0m"
        if i > 0:
            if (
                row["latitude"]
                and row["longitude"]
                and home_coords[0]
                and home_coords[1]
            ):
                dist = line_of_sight_distance(
                    home_coords, [row["latitude"], row["longitude"], row["altitude"]]
                )
            else:
                dist = "N/A"

        # Role formatting
        role_raw = row["role"]
        try:
            role_int = int(role_raw)
            role = ROLE_MAP.get(role_int, "other")
        except (ValueError, TypeError):
            role = str(role_raw).lower().replace("role_", "")

        # Last Heard string
        lh_str = (
            datetime.fromtimestamp(row["last_heard"]).strftime("%H:%M:%S")
            if row["last_heard"]
            else "N/A"
        )

        # Construct table row
        table_row = [
            i + 1,  # Number
            row["long_name"] or row["node_id"],  # User
            row["short_name"] or "N/A",  # AKA
            row["hw_model"] or "N/A",  # Hardware
            role,  # Role
            lat_long,  # Lat/Long
            f"{row['altitude']}m" if row["altitude"] else "N/A",  # Altitude
            f"{row['battery_level']}%" if row["battery_level"] is not None else "N/A",
            dist,  # Dist
            row["snr"] if row["snr"] is not None else "N/A",  # SNR
            row["hops_away"] if row["hops_away"] is not None else "N/A",
            lh_str,  # LastHeard
            format_since(row["last_heard"]),  # Since
        ]
        table_data.append(table_row)

    return headers, table_data
