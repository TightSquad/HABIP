#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

# HABIP
# Startup scripts
## Root
if [ -f /root/startup.sh ]; then
  bash -e /root/startup.sh &
fi
## Users in /home
for d in /home/*; do
if [ -d ${d} ]; then
  if [ -f ${d}/habip/startup/startup_pihat.sh ]; then
      username="$(basename ${d})"
      sudo --user="${username}" bash -e ${d}/habip/startup/startup_pihat.sh &
    fi
  fi
done
unset d

exit 0
