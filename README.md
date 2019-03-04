# Notifier
inotify-based folder monitoring script

```
usage: notifier.py [-h] [-r] -m MONITORED_FOLDER [-o OUTPUT_FOLDER] [-e]

Monitoring the filesystem powered by oRoCiock

optional arguments:
  -h, --help            show this help message and exit
  -r, --read            read new files on-the-fly
  -m MONITORED_FOLDER, --monitor MONITORED_FOLDER
                        The monitored folder
  -o OUTPUT_FOLDER, --out OUTPUT_FOLDER
                        folder where the catched files will be stored
  -e, --events          shows only the events on monitored folder
  ```
