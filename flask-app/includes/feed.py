from includes.maths import parse_coord, parse_height, line_of_sight_distance

def parse_feed(feed: str):
    """
    Convert the ASCII table feed into a list of lists:
    - First row -> headers
    - Remaining rows -> table data
    """

    rows = []
    field_list_filter=[0,1,3,4,6,7,8,9,10,11,14,15,17] 
    for idx,line in enumerate(feed):
        # Only process lines that look like table rows
        if line.strip().startswith("│") and "─" not in line:
            # Split on │ and strip whitespace
            cols = line.split("│")
            coords=[cols[8].strip(),cols[9].strip(),cols[10].strip()]
            # Geographic wonders to be worked
            if idx == 0:
              cols.insert(11,'Dist')
            elif idx == 1:
              cols.insert(11,'0m')
              home=coords
            else:
              if 'N/A' not in coords[0:2]:
                cols.insert(11,line_of_sight_distance(home,coords))
              else:
                cols.insert(11,'N/A')
            parts = [cols[i+1].strip() for i in field_list_filter if i < len(cols)]
            rows.append(parts)

    if not rows:
        return [], []

    headers = rows[0]
    data = rows[1:]

    return headers, data