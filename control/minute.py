# Version 1.0
# Author Rainer Schatzmayr
#
# This is the script that is called every minute. It reads the names of
# all .dat files in a folder and calls the loader with one of them randomly
import os
import time
import random

if __name__ == "__main__":
    # check that nothing has happen for the last 60 seconds
    # this should avoid the minute.py to overwrite the web interface
    if (time.time() - os.path.getmtime('/var/www/html/data.dat')) > 60 :
        playlistPath = '/var/www/html/playfiles/'
        playlistFiles = [f for f in os.listdir(playlistPath) if f.endswith('.dat')]
        cmd = "python /var/www/html/loader.py -f " + playlistPath + random.choice(playlistFiles)
        os.system(cmd)
    # check if the /var/www/html/loader.log file is too l arge
    # it should be a rolling log, but not implemented yet
    if os.stat('/var/www/html/loader.log').st_size > 64000 :
        os.remove('/var/www/html/loader.log')
