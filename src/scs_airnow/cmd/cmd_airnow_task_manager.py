"""
Created on 13 March 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_airnow import version


# TODO: split off SiteConf functions

# --------------------------------------------------------------------------------------------------------------------

class CmdAirNowTaskManager(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-v] [{ -l | -s [-c AGENCY_CODE SITE_CODE] ORG GROUP LOC "
                                                    "TOPIC DEVICE DURATION CHECKPOINT UPLOAD_START P1..PN | "
                                                    "-d ORG GROUP LOC TOPIC }]",
                                              version=version())

        # optional...
        self.__parser.add_option("--list", "-l", action="store_true", dest="list", default=False,
                                 help="list tasks")

        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="set a task")

        self.__parser.add_option("--codes", "-c", type="string", nargs=2, action="store", dest="codes",
                                 help="specify an agency code and site code (when setting a task)")

        self.__parser.add_option("--delete", "-d", type="string", nargs=4, action="store", dest="delete",
                                 help="delete a task")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.list and (self.is_set() or self.is_delete()):
            return False

        if self.is_set() and len(self.__args) < 9:
            return False

        return True


    def is_set(self):
        return self.__opts.set


    def is_delete(self):
        return self.__opts.delete is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def list(self):
        return self.__opts.list


    @property
    def set_org(self):
        return None if not self.__opts.set else self.__args[0]


    @property
    def set_group(self):
        return None if not self.__opts.set else self.__args[1]


    @property
    def set_loc(self):
        return None if not self.__opts.set else self.__args[2]


    @property
    def set_topic(self):
        return None if not self.__opts.set else self.__args[3]


    @property
    def set_device(self):
        return None if not self.__opts.set else self.__args[4]


    @property
    def set_duration(self):
        return None if not self.__opts.set else self.__args[5]


    @property
    def set_checkpoint(self):
        return None if not self.__opts.set else self.__args[6]


    @property
    def set_upload_start(self):
        return None if not self.__opts.set else self.__args[7]


    @property
    def set_parameters(self):
        return None if not self.__opts.set else self.__args[8:]


    @property
    def agency_code(self):
        return None if not self.__opts.codes else self.__opts.codes[0]


    @property
    def site_code(self):
        return None if not self.__opts.codes else self.__opts.codes[1]


    @property
    def delete_org(self):
        return None if self.__opts.delete is None else self.__opts.delete[0]


    @property
    def delete_group(self):
        return None if self.__opts.delete is None else self.__opts.delete[1]


    @property
    def delete_loc(self):
        return None if self.__opts.delete is None else self.__opts.delete[2]


    @property
    def delete_topic(self):
        return None if self.__opts.delete is None else self.__opts.delete[3]


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        settings = self.__args if self.__opts.set else None

        return "CmdAirNowTaskManager:{list:%s, set:%s, codes:%s, delete:%s, verbose:%s}" % \
               (self.list, settings, self.__opts.codes, self.__opts.delete, self.verbose)
