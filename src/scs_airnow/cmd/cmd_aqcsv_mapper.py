"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAQCSVMapper(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -t ORG GROUP LOC TOPIC [-d DIR] [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--task", "-t", type="string", nargs=4, action="store", dest="task",
                                 help="specify the task")

        # optional...
        self.__parser.add_option("--include-header", "-i", action="store_true", dest="header", default=False,
                                 help="report narrative to stderr")

        self.__parser.add_option("--dir", "-d", type="string", nargs=1, action="store", dest="dir",
                                 help="write the output to a CSV file in the named directory")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.task is None:
            return False

        return True


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
    def header(self):
        return self.__opts.header


    @property
    def dir(self):
        return self.__opts.dir


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAQCSVMapper:{task:%s, header:%s, dir:%s, verbose:%s}" % \
               (self.__opts.task, self.header, self.dir, self.verbose)
