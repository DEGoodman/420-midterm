##!/usr/bin/python
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
        if not os.path.exists(path + "/modified_fits/"):
            new_path = os.makedirs(path + "/modified_fits/")
        write_mf(lst, new_path)
    except Exception, e:
        print("Could not find your fits file directory. Is it a child directory of this script?")


# create makeflow file
def write_mf(fits_list, path):
    makeflow = open(r'go.makeflow', 'w')
    sf_path = "gsfs1/xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/bin"
    ''' loop through all fits files and add makeflow lines

        /gsfs1/xdisk/dkapellusch/midterm/data/Fits_files/modified_fits/<filename> : fitsdata.py + <filename>
            python fitsdata.py <filename> > /gsfs1/xdisk/dkapellusch/midterm/data/fitsfiles/modified_fits/<filename>


        (row with )

        /gsfs1/xdisk/dkapellusch/midterm/data/Fits_files/modified_fits/comp_<filename> : /xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg <fitsfilename>
            ./solve-field -u app -L 0.3 -H 3.0 --backend-config /xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg  --overwrite <fitsfilename> > "nameofinputfile.cfg"
    '''
    for fit in fits_list:
        # modify headers
        makeflow.write(path + str(fit[0]) + " : " + fitsdata.py + " " + str(fit[0])+ " \n")
        makeflow.write("\python fitsdata.py " + str(fit[0])  + " > " + path + str(fit[0]) "\n")
        makeflow.write("\n")

        # run ./solve-field
        new_fname = path + str(fit[0])
        makeflow.write(path + "comp_" + fit[0] + " : "  + "/xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg" + " " + new_fname + " \n")
        makeflow.write("\t./solve-field -u app -L 0.3 -H 3.0 --backend-config /xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg  --overwrite " + new_fname + " > " + path + "comp_" + fit[0])
        makeflow.write("\n")

    makeflow.close()

if __name__ == "__main__":
    get_files()
