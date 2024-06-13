#!/bin/bash

echo -e "UUP-Tools v2.2 - UUPDownloader\nCopyright (C) 2012-2024 BetaWorld"
aria2c -R -c -s16 -x16 -k1M --allow-overwrite -i "download.txt"
