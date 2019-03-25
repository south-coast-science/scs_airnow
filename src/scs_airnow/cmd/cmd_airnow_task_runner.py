"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class CmdAirNowTaskRunner(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -p [[DD-]HH:]MM -d DIR [-e END] [-c] [-v]",
                                              version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--sample-period", "-p", type="string", nargs=1, action="store", dest="sample_period",
                                 help="reporting period days / hours / minutes")

        self.__parser.add_option("--dir", "-d", type="string", nargs=1, action="store", dest="dir",
                                 help="directory for temporary CSV files")

        # optional...
        self.__parser.add_option("--end", "-e", type="string", nargs=1, action="store", dest="end",
                                 help="ISO 8601 datetime reporting end")

        self.__parser.add_option("--check-availability", "-c", action="store_true", dest="check", default=False,
                                 help="stop processing topic when data is not available")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.sample_period is None or self.__opts.dir is None:
            return False

        return True


    def is_valid_sample_period(self):
        return Timedelta.construct_from_flag(self.__opts.sample_period) is not None


    def is_valid_end(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.end) is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sample_period(self):
        return None if self.__opts.sample_period is None else Timedelta.construct_from_flag(self.__opts.sample_period)


    @property
    def dir(self):
        return self.__opts.dir


    @property
    def end(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.end)


    @property
    def check(self):
        return self.__opts.check


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAirNowTaskRunner:{sample_period:%s, dir:%s, end:%s, check:%s, verbose:%s}" %  \
               (self.sample_period, self.dir, self.end, self.check, self.verbose)
