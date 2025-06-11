#!/bin/bash

# List of channel names (edit as needed)
channels=(
  channel,
)

sudo systemctl daemon-reload

for channel in "${channels[@]}"; do
  echo "Stopping blacknfreeze@${channel}.service ..."
  sudo systemctl disable blacknfreeze@"$channel".service
  sudo systemctl stop blacknfreeze@"$channel".service
done