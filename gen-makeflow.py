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
    try:
        # path = "/gsfs1/xdisk/dkapellusch/midterm/data/Fits_files/"
        path = "/xdisk/dkapellusch/midterm/data/test/"
        ''' directory structure
            data
                |- Fits_files
                |- test
                    |-gen_makeflow
                    |-go.makeflow
                    |-samplefile.cfg
                    |-two python scripts
                    |-Fits_files (input files)
        '''
        fits_dir = path + "/Fits_files/"
        lst = os.listdir(fits_dir)
        print(lst)
        write_mf(lst, fits_dir)
    except Exception, e:
        print(e)
        print("Could not find your fits file directory. Is it a child directory of this script?")

# create makeflow file
def write_mf(fits_list, fits_path):
    makeflow = open(r'go.makeflow', 'w')

    count = 0
    for fit in fits_list:
        full_fname = fits_path + str(fit)
        # base_fname = path + str(fit)

        # run ./solve-field
        makeflow.write(full_fname + ".cfg" + " : " + "/xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/bin/solve-field " + "/xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg " + full_fname + "\n")
        makeflow.write("\t/xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/bin/solve-field -u app -L 0.3 -H 3.0 --backend-config /xdisk/dkapellusch/cfitsio_stuff/astrometry_dir/etc/astrometry.cfg  --overwrite " + full_fname + " > " + full_fname + ".cfg" + "\n")
        makeflow.write("\n")

        # # 'move' files
        # makeflow.write("none" + str(count) + ".txt : movefile.py " + full_fname + "\n")
        # makeflow.write("\tpython movefile.py -i " + full_fname + " > none" + str(count) + ".txt\n")
        # makeflow.write("\n")
        # count += 1
        #
        # base_fname=base_fname[:-5]
        # # modify files
        # makeflow.write( full_fname + "_UPDATED.fits" + " : " + "FixCfgAndMetaData.py " + full_fname + ".cfg " + base_fname + ".new \n")
        # makeflow.write("\tpython FixCfgAndMetaData.py -i " + full_fname + ".cfg" + " -o " + full_fname + ".cfg" + " -n " + base_fname + ".new > " + full_fname + "_UPDATED.fits\n")
        # makeflow.write("\n")

    makeflow.close()

if __name__ == "__main__":
    get_files()
