#!/bin/bash

# List of channel names (edit as needed)
channels=(
  channel,
)

sudo systemctl daemon-reload

for channel in "${channels[@]}"; do
  echo "Restarting blacknfreeze@${channel}.service ..."
  sudo systemctl disable blacknfreeze@"$channel".service
  sudo systemctl stop blacknfreeze@"$channel".service
  sudo systemctl start blacknfreeze@"$channel".service
  sudo systemctl enable blacknfreeze@"$channel".service
done