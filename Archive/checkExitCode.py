#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
"""
@title: checkExitCode.py
@credits: Shahin Pirooz
@company: Emruz
@created: Sun Mar  8 12:22:33 2020
@python: 3.7
"""
# =============================================================================
"""
This script can check whether a file was last modified before a time X. If it was modified after that,
an error is raised. It can also check, whether the file contains
 a specific string (e.g. "exit 0"). If it's not there, an error is raised.

 Example:
 checkExitCode.py --exitcode -t 20 /path/to/logfile
"""
# =============================================================================
# Change History
# Date              Version              Notes
# 20190312          0.1                  Initial Version
#
# -----------------------------------------------------------------------------
# Imports
import os
import argparse
import time
import re

# -----------------------------------------------------------------------------
# Variable Declarations
LOGGERNAME = ""

# Parse arguments
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("logfile", help="Specify the logfile to monitor.")
parser.add_argument("-t", "--time", help="Time in minutes which a log file can be unmodified before raising CRITICAL"
                                     " alert.", type=int)
parser.add_argument("--exitcode", help="If specified, check if \"exit 0\" exists in logfile.", action="store_true")

args = parser.parse_args()


# =============================================================================
# Classes
# -----------------------------------------------------------------------------


# =============================================================================
# Functions
# -----------------------------------------------------------------------------


# =============================================================================
# Main Function
def main():
    # -------------------------------------------------------------------------
    if not (args.time or args.exitcode):
        print(f'At least one argument (--time, --exitcode) is required.')
        exit(2)
    
    #variables
    log = args.logfile
    
    # Check if file exists and is readable by user
    try:
        f = open(log)
    except IOError:
        print(f'Cannot open the file. Check if it exists and you have the right permissions to open it.')
        exit(1)
    
    # check exit code
    if args.exitcode:
        logfile = f.read()
        if not re.search("exit 0", logfile, flags=re.I):
            print(f'CRITICAL: Exit code not found in File {log}')
            exit(2)
    
    # Check last file modification time
    if args.time:
        # File Modification time in seconds since epoch
        fileModificationTime = os.stat(log).st_mtime
    
        # Time in seconds since epoch for time, in which logfile can be unmodified.
        t = time.time()
        shouldTime = t - (args.time * 3600)
    
        # Time in minutes since last modification of file
        minutesSinceLastModification = (t - fileModificationTime) / 60
    
        if minutesSinceLastModification > args.time:
            print(f'CRITICAL: {log} last modified {minutesSinceLastModification:.2f} minutes. Threshold set to {args.time:.2f} minutes')
            exit(2)
    
    # If nothin went wrong, print OK and exit.
    print('OK. Exitcode found or last modification time not exceeded.')
    exit(0)

if __name__ == '__main__':
    main() 
