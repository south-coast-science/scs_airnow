"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAirNowUploader(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-v] LOCAL_FILENAME [REMOTE_FILENAME]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.local_filename is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def local_filename(self):
        return self.__args[0] if len(self.__args) > 0 else None


    @property
    def remote_filename(self):
        return self.__args[1] if len(self.__args) > 1 else None


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAirNowUploader:{local_filename:%s, remote_filename:%s, verbose:%s}" % \
               (self.local_filename, self.remote_filename, self.verbose)
