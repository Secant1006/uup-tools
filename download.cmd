@echo off
echo UUP-Tools v2.2 - UUPDownloader
echo Copyright (C) 2012-2024 BetaWorld
aria2c.exe -x16 -s16 -j5 -c -R -i"download.txt"
pause>nul