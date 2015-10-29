#!/usr/bin/python
''' usage: generates a makeflow file to process fits data for astrometry.net.
    This script currently assumes the metadata for each file has already been updated.

author: Erik Goodman

NOTE: this file must be executed in the parent directory of the fits files.
'''
import csv
from datetime import *
import math
import os


# read list of fits files for input
def get_files():
    path = os.getcwd() # get current working directory
    try:
        path = "/gsfs1/xdisk/dkapellusch/midterm/data/Fits_files"
        lst = os.listdir(path)
        # create target directory
        # if not os.path.exists(path + "/modified_fits/"):
        #     new_path = os.makedirs(path + "/modified_fits/")
        write_mf(lst, path)
    except Exception, e:
        print("Could not find your fits file directory. Is it a child directory of this script?")


# create makeflow file
def write_mf(fits_list, path):
    makeflow = open(r'go.makeflow', 'w')
    sf_path = "gsfs1/xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/bin"
    '''
        /gsfs1/xdisk/dkapellusch/midterm/data/Fits_files/<nameofinputfile>.cfg : /xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg <fitsfilename>
            ./solve-field -u app -L 0.3 -H 3.0 --backend-config /xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg  --overwrite <fitsfilename> > <nameofinputfile>.cfg

        none.txt : movefile.py /gsfs1/xdisk/dkapellusch/midterm/data/Fits_files/<fitsfilename>
            movefile.py -i <fitsfilename> > none.txt

        /gsfs1/xdisk/dkapellusch/midterm/data/Fits_files/<filename>_updated.fits : fixcfg.py <inputfile>
            python fixCfgAndMetaData.py -i <inputfile.cfg> -o <inputfile.cfg> -n <inputfile.new> > /gsfs1/xdisk/dkapellusch/midterm/data/Fits_files/<outputfile>_updated.fits

    '''
    for fit in fits_list:
        full_fname = path + str(fit[0])
        # run ./solve-field
        makeflow.write(full_fname + ".cfg" + " : "  + "/xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg" + " " + full_fname + "\n")
        makeflow.write("\tsolve-field -u app -L 0.3 -H 3.0 --backend-config /xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg  --overwrite " + full_fname + " > " + full_fname + ".cfg" + "\n")
        makeflow.write("\n")

        # 'move' files
        makeflow.write("none.txt : movefile.py " + full_fname + "\n")
        makeflow.write("\tmovefile.py -i " + full_fname + " > none.txt")
        makeflow.write("\n")

        # modify files
        makeflow.write( full_fname + "_updated.fits" + " : " + fixcfg.py + " " + full_fname + ".cfg" + " \n")
        makeflow.write("\tpython fixCfgAndMetaData.py -i " + full_fname + ".cfg" + " -o " + full_fname + ".cfg" + " -n " + full_fname + ".new > " + full_fname + "_updated.fits\n")
        makeflow.write("\n")

    makeflow.close()

if __name__ == "__main__":
    get_files()
