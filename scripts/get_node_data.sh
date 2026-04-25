#!/usr/bin/bash
work_dir="/home/james/meshtastic-node-list/node_data"
/home/james/.venv/bin/python -m meshtastic --serial /dev/ttyUSB0 --nodes > ${work_dir}/nodes_tmp.txt 2> ${work_dir}/error.log
mv ${work_dir}/nodes_tmp.txt ${work_dir}/nodes.txt
