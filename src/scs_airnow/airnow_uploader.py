#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The aqcsv_mapper utility is used to

SYNOPSIS
airnow_uploader.py [-v] LOCAL_FILENAME [REMOTE_FILENAME]

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

        client = SFTPClient(conf.host)
        client.connect(username=conf.username, password=conf.password, log=True)

        if conf.remote_path:
            client.chdir(conf.remote_path)

        if cmd.verbose:
            print("airnow_uploader: %s" % client, file=sys.stderr)
            sys.stderr.flush()

        client.put(cmd.local_filename, remote_path=cmd.remote_filename, preserve_mtime=True)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("airnow_uploader: KeyboardInterrupt", file=sys.stderr)

    finally:
        if client:
            client.close()
