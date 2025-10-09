from includes.maths import parse_coord, parse_height, line_of_sight_distance

google_prefix='https://www.google.com/maps/place/'
google_suffix=',12z/data=!4m4!3m3!8m2!3d52.2803!4d0.657!5m1!1e1'
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
              cols[8]="Lat/Long"
            elif idx == 1:
              cols.insert(11,'0m')
              home=coords
            else:
              if 'N/A' not in coords[0:2]:
                cols.insert(11,line_of_sight_distance(home,coords))
              else:
                cols.insert(11,'N/A')
            parts = [cols[i+1].strip() for i in field_list_filter if i < len(cols)]
        # add google maps URL to co-ords
            if idx!=0 and 'N/A' not in coords[0:2]:
              google_url=f'<A HREF="{google_prefix}{parts[5]}+{parts[6]}/@{parts[5]},{parts[6]}{google_suffix}" TARGET="maps">'.replace('°','')
              parts[5]=f'{google_url}{parts[5]}, {parts[6]}</A>'
            del parts[6]
            rows.append(parts)

    if not rows:
        return [], []

    headers = rows[0]
    data = rows[1:]

    return headers, data
