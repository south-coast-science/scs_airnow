#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The airnow_task utility is used to

SYNOPSIS
airnow_task.py -t ORG GROUP LOC TOPIC -s START -e END [-d DIR] [-v]

EXAMPLES
./airnow_task.py -t unep ethiopia 1 particulates -s 2019-03-20T00:00:00Z -e 2019-03-21T00:00:00Z -d data -v

SEE ALSO
scs_analysis/airnow_downloader
scs_analysis/aqcsv_mapper
scs_analysis/airnow_uploader
scs_analysis/aqcsv_task_manager
"""

import os
import sys

from glob import glob

from scs_airnow.cmd.cmd_airnow_task import CmdAirNowTask
from scs_airnow.helper.airnow_availability import AirNowAvailability

from scs_core.aqcsv.connector.airnow_mapping_task import AirNowMappingTaskList
from scs_core.data.datum import Datum
from scs_core.sys.subprocess import Pipe

from scs_host.sys.host import Host


# TODO: fix the issue of locality for external scripts

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowTask()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if not cmd.is_valid_start():
        print("airnow_task: invalid format for start datetime.", file=sys.stderr)
        exit(2)

    if not cmd.is_valid_end():
        print("airnow_task: invalid format for end datetime.", file=sys.stderr)
        exit(2)

    if not Datum.is_numeric(cmd.loc):
        print("airnow_task: the loc value %s should be an integer." % cmd.loc, file=sys.stderr)
        exit(2)

    if cmd.verbose:
        print("airnow_task: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MappingTask...
        tasks = AirNowMappingTaskList.load(Host)
        task = tasks.item((cmd.org, cmd.group, int(cmd.loc), cmd.topic))

        if task is None:
            print("airnow_task: task not found.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("airnow_task: %s" % task, file=sys.stderr)
            sys.stderr.flush()

        # files...
        task_prefix = task.file_prefix()
        dir_name =  task.site_code if cmd.dir is None else os.path.join(cmd.dir, task.site_code)
        file_path = os.path.join(dir_name, task_prefix)

        if cmd.verbose:
            print("airnow_task: temporary file group: %s" % file_path, file=sys.stderr)
            sys.stderr.flush()

        joined_filename = file_path + '-joined.csv'
        mapped_filename = '.'.join((file_path, task.agency_code))


        # ------------------------------------------------------------------------------------------------------------
        # validation...

        # datetimes...
        start = cmd.start.as_iso8601()
        end = cmd.end.as_iso8601()

        # data availability...
        if cmd.check:
            result = AirNowAvailability.check("airnow_task", task, cmd.end, cmd.verbose)

            if result != AirNowAvailability.OK:
                exit(result)


        # ------------------------------------------------------------------------------------------------------------
        # run: download...

        if cmd.verbose:
            print("airnow_task: downloading...", end='', file=sys.stderr)
            sys.stderr.flush()

        p = Pipe(('./airnow_downloader.py', '-t', cmd.org, cmd.group, cmd.loc, cmd.topic, '-s', start, '-e', end,
                  '-d', cmd.dir, '-f', task_prefix))

        return_code = p.wait()

        if return_code > 0:
            print("airnow_task: download failed with exit code %s." % return_code, file=sys.stderr)
            exit(return_code)

        if cmd.verbose:
            print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: mapping...

        if cmd.verbose:
            print("airnow_task: mapping...", end='', file=sys.stderr)
            sys.stderr.flush()

        p = Pipe(('./csv_reader.py', joined_filename),
                 ('./airnow_mapper.py', '-t', cmd.org, cmd.group, cmd.loc, cmd.topic),
                 ('./csv_writer.py', '-x', mapped_filename))

        return_code = p.wait()

        if return_code > 0:
            print("airnow_task: mapping failed with exit code %s." % return_code, file=sys.stderr)
            exit(return_code)

        if cmd.verbose:
            print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: upload...

        if cmd.verbose:
            print("airnow_task: uploading...", end='', file=sys.stderr)
            sys.stderr.flush()

        p = Pipe(('./airnow_uploader.py', mapped_filename))

        return_code = p.wait()

        if return_code > 0:
            print("airnow_task: upload failed with exit code %s." % return_code, file=sys.stderr)
            exit(return_code)

        if cmd.verbose:
            print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: update task record...

        if cmd.verbose:
            print("airnow_task: updating task upload-end to %s..." % cmd.end.as_iso8601(), end='', file=sys.stderr)
            sys.stderr.flush()

        task.upload_end = cmd.end
        tasks.save(Host)

        if cmd.verbose:
            print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: delete files...

        if cmd.verbose:
            print("airnow_task: deleting temporary files...", end='', file=sys.stderr)
            sys.stderr.flush()

        files = glob(file_path + '*')

        if files:
            p = Pipe(['rm'] + files)

            return_code = p.wait()

            if return_code > 0:
                print("airnow_task: delete failed with exit code %s." % return_code, file=sys.stderr)
                exit(return_code)

        if cmd.verbose:
            print("done.", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("airnow_task: KeyboardInterrupt", file=sys.stderr)
