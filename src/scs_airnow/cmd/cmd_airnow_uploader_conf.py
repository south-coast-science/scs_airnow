"""
Created on 21 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_airnow import version
from scs_core.aqcsv.conf.airnow_uploader_conf import AirNowUploaderConf


# --------------------------------------------------------------------------------------------------------------------

class CmdAirNowUploaderConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -c HOST USERNAME PASSWORD [-p PORT] "
                                                    "[-r REMOTE_PATH] | -d }] [-v]", version=version())

        # optional...
        self.__parser.add_option("--connection", "-c", type="string", nargs=3, action="store", dest="connection",
                                 help="set HOST, USERNAME and PASSWORD")

        self.__parser.add_option("--port", "-p", type="int", action="store", dest="port",
                                 help="specify the port (default %s)" % AirNowUploaderConf.DEFAULT_PORT)

        self.__parser.add_option("--remote-path", "-r", type="string", action="store", dest="remote_path",
                                 help="specify a remote path")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if (self.port or self.remote_path) and not self.__opts.connection:
            return False

        if self.delete and self.__opts.connection:
            return False

        return True


    def set(self):
        return self.__opts.connection is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def host(self):
        return None if self.__opts.connection is None else self.__opts.connection[0]


    @property
    def username(self):
        return None if self.__opts.connection is None else self.__opts.connection[1]


    @property
    def password(self):
        return None if self.__opts.connection is None else self.__opts.connection[2]


    @property
    def port(self):
        return self.__opts.port


    @property
    def remote_path(self):
        return self.__opts.remote_path


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAirNowUploaderConf:{connection:%s, port:%s, remote_path:%s, delete:%s, verbose:%s}" % \
               (self.__opts.connection, self.port, self.remote_path, self.delete, self.verbose)
