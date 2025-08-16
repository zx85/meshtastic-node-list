# meshtastic-node-list
A simple Flask app that takes the --nodes info from the meshtastic CLI and displays it as a table

## Requirements

- A meshtastic node with a USB connection
- A Linux device (a Raspberry Pi 4 works) with a spare USB port
- A cable to connect the meshtastic node to the Linux device
- The meshtastic CLI installed somewhere on the linux device - this can be found [here](https://meshtastic.org/docs/software/python/cli/)

## Configuration

The meshtastic CLI has a `--nodes` parameter, which outputs (in a 'pretty' text table) the list of the nodes seen by the meshtastic device, sorted by time last seen.

Once the CLI is installed it's necessary to install a crontab that runs it every minute (or less often if you'd prefer) and output the file to a known location (creating any directories necessary beforehand).

eg.
```
* * * * * /home/james/.local/bin/meshtastic --nodes > /home/james/node_data/nodes.txt
```

Then, modify the `docker-compose` entries to map the filename and directory where the nodes.txt is stored for use within the app:

eg.
```
   .
   .
      - node_data_file="/app/node_data/nodes.txt"
    volumes:
      - /home/james/node_data:/app/node_data
```

That's about it, so far. Hopefully it'll end up being nicely formatted and sortable and all that.