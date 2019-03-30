#!/usr/bin/env python3

"""
Created on 21 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The aws_api_auth utility is used to

SYNOPSIS
airnow_uploader_conf.py [{ -c HOST USERNAME PASSWORD [-p PORT] [-r REMOTE_PATH] | -d }] [-v]

EXAMPLES
./airnow_uploader_conf.py -c sftp.airnowdata.org UNEPdatauser xxx -r /UNEP/AQCSV

FILES
~/SCS/conf/airnow_uploader_conf.json

DOCUMENT EXAMPLE
{"host": "sftp.airnowdata.org", "port": 22, "username": "UNEPdatauser", "password": "xxx",
"remote-path": "/UNEP/AQCSV"}

SEE ALSO
scs_analysis/airnow_uploader
"""

import sys

from scs_core.aqcsv.conf.airnow_uploader_conf import AirNowUploaderConf
from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_airnow.cmd.cmd_airnow_uploader_conf import CmdAirNowUploaderConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowUploaderConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("airnow_uploader_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # ClientAuth...
    conf = AirNowUploaderConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        port = AirNowUploaderConf.DEFAULT_PORT if cmd.port is None else cmd.port

        conf = AirNowUploaderConf(cmd.host, port, cmd.username, cmd.password, cmd.remote_path)
        conf.save(Host)

    if cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
