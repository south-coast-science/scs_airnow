#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The aqcsv_mapper utility is used to

SYNOPSIS
airnow_uploader.py [-v] LOCAL_FILENAME [REMOTE_FILENAME]

EXAMPLES
./airnow_uploader.py -v data/231000000000/201903252001_231.NRB

FILES
~/SCS/conf/airnow_uploader_conf.json

SEE ALSO
scs_analysis/airnow_uploader_conf
"""

import os
import sys

from scs_airnow.cmd.cmd_airnow_uploader import CmdAirNowUploader

from scs_core.aqcsv.conf.airnow_uploader_conf import AirNowUploaderConf

from scs_host.client.sftp_client import SFTPClient
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

def __listdir():
    ls = client.listdir()

    if cmd.verbose:
        cwd = client.cwd()
        path = '/' if cwd is None else cwd

        print("airnow_uploader: %s: %s" % (path, ls), file=sys.stderr)
        sys.stderr.flush()


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    client = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowUploader()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if not os.path.exists(cmd.local_filename):
        print("airnow_uploader: file '%s' does not exist." % cmd.local_filename, file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print("airnow_uploader: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # conf...
        conf = AirNowUploaderConf.load(Host)

        if conf is None:
            print("airnow_uploader: no AirNowUploaderConf available.", file=sys.stderr)
            exit(1)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # connect...
        client = SFTPClient(conf.host)
        client.connect(username=conf.username, password=conf.password)

        if cmd.verbose:
            print("airnow_uploader: %s" % client, file=sys.stderr)
            sys.stderr.flush()

        __listdir()

        # chdir...
        for node in conf.remote_path.split('/'):
            client.chdir(node)
            __listdir()

        # put...
        client.put(cmd.local_filename)

        __listdir()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("airnow_uploader: KeyboardInterrupt", file=sys.stderr)

    finally:
        if client:
            client.close()
