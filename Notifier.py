#!/usr/bin/python

import inotify.adapters
import argparse
import mmap
import os
from datetime import datetime


def leggi_file(cartella_controllata):
    i = inotify.adapters.Inotify()
    i.add_watch(cartella_controllata)
    try:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            if 'IN_CLOSE_WRITE' in str(type_names):
                path = "{}/{}".format(path, filename)
                print(datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f') + ":" + " Reading {} content:".format(path).replace('//','/'))
                try:
                    with open(path, 'rb') as f:
                        buffer=mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
                        data=buffer.readline()
                        while buffer:
                            print data
                            buffer=buffer.readline()
                except Exception as e:
                    print datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f') + ":" + e.message
    except KeyboardInterrupt:
        print ("\nQuit!")
        pass


def scrivi_file(cartella_controllata,folder_out):
    i = inotify.adapters.Inotify()
    i.add_watch(cartella_controllata)
    try:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            if 'IN_CLOSE_WRITE' in str(type_names):
                path = "{}/{}".format(path, filename)
                try:
                    with open(path, 'rb') as f:
                        buffer=mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
                        data=buffer.readline()
                        while buffer:
                            buffer=buffer.readline()
                    file = open(folder_out+"/Notify_" + filename, "wb")
                    print(datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f') + ":" + " Writing {} in {}".format(path, folder_out+"/Notify_" + filename).replace('//','/'))
                    file.write(data)
                    file.close()
                except Exception as e:
                    print datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f') + ":" + e.message
    except KeyboardInterrupt:
        print ("\nQuit!")
        pass


def eventi(cartella_controllata):
    i = inotify.adapters.Inotify()
    i.add_watch(cartella_controllata)
    try:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            print datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f') + " " + ' , '.join(type_names)+" event for file " + path + "/" + filename
    except KeyboardInterrupt:
        print ("\nQuit!")
        pass

parser = argparse.ArgumentParser(description='Monitoring the filesystem powered by oRoCiock')
parser.add_argument('-r', '--read', action="store_true", dest='read_file',help="read new files on-the-fly" )
parser.add_argument('-m','--monitor', action='store',dest='monitored_folder',help="The monitored folder", required=True)
parser.add_argument('-o','--out', action='store', dest='output_folder', help="folder where the catched files will be stored")
parser.add_argument('-e','--events', action='store_true', dest='events', help="shows only the events on monitored folder")

args = parser.parse_args()
if args.monitored_folder is not "":
    if not args.events:
        os.system("clear")
        if not args.output_folder:
            print "[*] Monitoring Files to read"
            leggi_file(args.monitored_folder)
        if args.output_folder:
            print "[*] Monitoring Files to write"
            scrivi_file(args.monitored_folder,args.output_folder)
    else:
        print "[*] Monitoring File Events"
        eventi(args.monitored_folder)
