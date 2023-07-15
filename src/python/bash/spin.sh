#!/usr/bin/env bash
gatttool -i hci0 -b 90:84:2B:66:5B:2B --char-write -a 0x003d -n 01010164
sleep 1
gatttool -i hci0 -b 90:84:2B:66:5B:2B --char-write -a 0x003d -n 01010100