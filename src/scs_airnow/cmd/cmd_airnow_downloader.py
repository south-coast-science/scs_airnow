"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_airnow import version
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class CmdAirNowDownloader(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -t ORG GROUP LOC TOPIC -s START -e END [-d DIR] "
                                                    "[-f FILE_PREFIX] [-c] [-v]", version=version())

        # compulsory...
        self.__parser.add_option("--task", "-t", type="string", nargs=4, action="store", dest="task",
                                 help="specify the task")

        self.__parser.add_option("--start", "-s", type="string", action="store", dest="start",
                                 help="ISO 8601 datetime start")

        self.__parser.add_option("--end", "-e", type="string", action="store", dest="end",
                                 help="ISO 8601 datetime end")

        # optional...
        self.__parser.add_option("--dir", "-d", type="string", action="store", dest="dir",
                                 help="write the output to a CSV file in the named directory")

        self.__parser.add_option("--file-prefix", "-f", type="string", action="store", dest="file_prefix",
                                 help="use the specified file prefix (instead of auto-generated)")

        self.__parser.add_option("--check-availability", "-c", action="store_true", dest="check", default=False,
                                 help="check availability of data before proceeding")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.task is None or self.__opts.start is None or self.__opts.end is None:
            return False

        return True


    def is_valid_start(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.start) is not None


    def is_valid_end(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.end) is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def task_org(self):
        return None if self.__opts.task is None else self.__opts.task[0]


    @property
    def task_group(self):
        return None if self.__opts.task is None else self.__opts.task[1]


    @property
    def task_loc(self):
        return None if self.__opts.task is None else self.__opts.task[2]


    @property
    def task_topic(self):
        return None if self.__opts.task is None else self.__opts.task[3]


    @property
    def start(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.start)


    @property
    def end(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.end)


    @property
    def dir(self):
        return self.__opts.dir


    @property
    def file_prefix(self):
        return self.__opts.file_prefix


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
        return "CmdAirNowDownloader:{task:%s, start:%s, end:%s, dir:%s, file_prefix:%s, check:%s, verbose:%s}" % \
               (self.__opts.task, self.start, self.end, self.dir, self.file_prefix, self.check, self.verbose)
