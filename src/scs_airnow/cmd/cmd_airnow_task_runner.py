"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class CmdAirNowTaskRunner(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -p [[DD-]HH:]MM -d DIR [-c] [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--sample-period", "-p", type="string", nargs=1, action="store", dest="sample_period",
                                 help="reporting period days / hours / minutes")

        self.__parser.add_option("--dir", "-d", type="string", nargs=1, action="store", dest="dir",
                                 help="directory for temporary CSV files")

        # optional...
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


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sample_period(self):
        return None if self.__opts.sample_period is None else Timedelta.construct_from_flag(self.__opts.sample_period)


    @property
    def dir(self):
        return self.__opts.dir


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
        return "CmdAirNowTaskRunner:{sample_period:%s, dir:%s, check:%s, verbose:%s}" %  \
               (self.sample_period, self.dir, self.check, self.verbose)
