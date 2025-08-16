import math
def parse_coord(coord_str):
    """Convert a coordinate string like '52.2499°' into float."""
    try:
      return float(coord_str.replace('°','').strip())
    except:
      return 0

def parse_height(height_str, default_height=0):
    """Convert a height string like '67m' into float meters."""
    if height_str and height_str!='N/A':
        try:
          return float(height_str.replace('m','').strip())
        except:
          return default_height
    return default_height

def line_of_sight_distance(home_row, target_row):
    """
    Calculates the 3D distance from home_row to target_row.
    
    home_row: [lat, lon, height]
    target_row: [lat, lon, height] (height may be missing or None)
    
    Returns distance in meters.
    """
    # Parse lat/lon
    lat1 = parse_coord(home_row[0])
    lon1 = parse_coord(home_row[1])
    h1 = parse_height(home_row[2], default_height=0)

    lat2 = parse_coord(target_row[0])
    lon2 = parse_coord(target_row[1])
    
    # Use target height if present, otherwise assume home height
    h2 = parse_height(target_row[2], default_height=h1)

    # Convert lat/lon to radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Earth's radius in meters
    R = 6371000  

    # Haversine formula for surface distance
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    surface_distance = R * c

    # Line-of-sight 3D distance including height difference
    delta_h = h2 - h1
    distance = math.sqrt(surface_distance**2 + delta_h**2)
    if isinstance(distance,float) or isinstance(distance,int):
      return f'{int(distance)}m'
    else:
      return 'N/A'