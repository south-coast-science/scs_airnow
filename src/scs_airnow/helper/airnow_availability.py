"""
Created on 25 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow
"""

import json
import sys

from subprocess import check_output, CalledProcessError

from scs_core.aws.manager.byline.byline import Byline


# --------------------------------------------------------------------------------------------------------------------

class AirNowAvailability(object):
    """
    classdocs
    """

    OK =                    0
    NOT_AVAILABLE =         1

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def check(cls, script_name, task, period_end, verbose):
        if verbose:
            print(script_name + ": checking data availability...", end='', file=sys.stderr)
            sys.stderr.flush()

        # find latest...
        args = ['./aws_byline.py', '-l', '-t', task.environment_path()]

        try:
            jstr = check_output(args).decode().strip()
        except CalledProcessError as ex:
            print("availability check failed with exit code %s." % ex.returncode, file=sys.stderr)
            return ex.returncode

        if not jstr:
            print("no published data for %s." % task.environment_path(), file=sys.stderr)
            return cls.NOT_AVAILABLE

        byline = Byline.construct_from_jdict(json.loads(jstr))

        # compare...
        if byline.rec < period_end:
            print("latest report (%s) is earlier than the requested period end." % byline.rec.as_iso8601(),
                  file=sys.stderr)
            return cls.NOT_AVAILABLE

        # OK...
        if verbose:
            print("done.", file=sys.stderr)

        return cls.OK
