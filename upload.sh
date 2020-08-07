#!/bin/bash

export AMPY_PORT=/dev/ttyUSB0


target_files=(mqtt_client.py tb_client.py config.json service.py boot.py)

for filename in "${target_files[@]}"; do
  [ -e $filename ] || continue
  echo $filename uploading...
  ampy put $filename
  echo $filename uploading finished.
  echo
done

screen $AMPY_PORT 115200