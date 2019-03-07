#!/usr/bin/env python3

"""
Created on 18 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The csv_logger_conf utility is used to specify the filesystem path to the log files generated by csv_logger. It also
specifies the csv_logger behaviour when the volume becomes full: if delete-oldest is true, the oldest logs are
removed to make space, if false, then logging stops. A write-interval parameter may be used to specify time between
flushes, in order to extend the life of SD cards.

Note that the logging process(es) must be restarted for changes to take effect.

SYNOPSIS
csv_logger_conf.py { [-r ROOT_PATH] [-o DELETE_OLDEST] [-i WRITE_INTERVAL] | -d } [-v]

EXAMPLES
csv_logger_conf.py -r /srv/removable_data_storage -o 1 -i 0

FILES
~/SCS/conf/csv_logger_conf.json

DOCUMENT EXAMPLE
{"root-path": "/srv/removable_data_storage", "delete-oldest": true, "write-interval": 0}

SEE ALSO
scs_dev/csv_logger
"""

import sys

from scs_analysis.cmd.cmd_csv_logger_conf import CmdCSVLoggerConf

from scs_core.csv.csv_logger_conf import CSVLoggerConf
from scs_core.data.json import JSONify
from scs_core.sys.filesystem import Filesystem

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdCSVLoggerConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("csv_logger_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # check for existing document...
    conf = CSVLoggerConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("csv_logger_conf: No configuration is present. You must therefore set all fields:", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        root_path = conf.root_path if cmd.root_path is None else cmd.root_path
        delete_oldest = conf.delete_oldest if cmd.delete_oldest is None else cmd.delete_oldest
        write_interval = conf.write_interval if cmd.write_interval is None else cmd.write_interval

        try:
            Filesystem.mkdir(root_path)
        except PermissionError:
            print("csv_logger_conf: You do not have permission to write in that directory.", file=sys.stderr)
            exit(1)

        conf = CSVLoggerConf(root_path, delete_oldest, write_interval)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
