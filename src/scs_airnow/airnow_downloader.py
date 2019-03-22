#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The airnow_downloader utility is used to

SYNOPSIS
airnow_downloader.py -t ORG GROUP LOC TOPIC -s START -e END [-d DIR] [-v]

EXAMPLES
./airnow_downloader.py -t unep ethiopia 1 particulates -s 2019-03-20T00:00:00Z -e 2019-03-21T00:00:00Z -d data -v

SEE ALSO
scs_analysis/aqcsv_mapper
scs_analysis/aqcsv_task_manager
"""

import json
import os
import sys

from subprocess import check_output, CalledProcessError, Popen, PIPE

from scs_airnow.cmd.cmd_airnow_downloader import CmdAirNowDownloader

from scs_core.aqcsv.connector.airnow_mapping_task import AirNowMappingTaskList

from scs_core.aws.data.byline import Byline

from scs_core.data.datum import Datum

from scs_core.sys.filesystem import Filesystem

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowDownloader()

    if not cmd.is_valid_start():
        print("airnow_downloader: invalid format for start datetime.", file=sys.stderr)
        exit(2)

    if not cmd.is_valid_end():
        print("airnow_downloader: invalid format for end datetime.", file=sys.stderr)
        exit(2)

    if not Datum.is_numeric(cmd.task_loc):
        print("airnow_downloader: the loc value %s should be an integer." % cmd.task_loc, file=sys.stderr)
        exit(2)

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("airnow_downloader: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MappingTask...
        tasks = AirNowMappingTaskList.load(Host)
        task = tasks.item((cmd.task_org, cmd.task_group, int(cmd.task_loc), cmd.task_topic))

        if task is None:
            print("airnow_downloader: task not found.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("airnow_downloader: %s" % task, file=sys.stderr)
            sys.stderr.flush()

        # files...
        task_prefix = task.file_prefix()
        dir_name =  task.site_code if cmd.dir is None else os.path.join(cmd.dir, task.site_code)
        file_prefix = task_prefix if cmd.file_prefix is None else cmd.file_prefix

        file_path = os.path.join(dir_name, file_prefix)

        if cmd.verbose:
            print("airnow_downloader: file group: %s" % file_path, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # validation...

        # datetimes...
        start = cmd.start.as_iso8601()
        end = cmd.end.as_iso8601()

        # available data...
        if cmd.check:
            if cmd.verbose:
                print("airnow_downloader: checking data availability...", end='', file=sys.stderr)
                sys.stderr.flush()

            args = ['./aws_byline.py', '-l', '-t', task.environment_path()]

            try:
                jstr = check_output(args).decode().strip()
            except CalledProcessError as ex:
                print("airnow_downloader: availability check failed with exit code %s." % ex.returncode,
                      file=sys.stderr)
                exit(ex.returncode)
                jstr = None

            byline = Byline.construct_from_jdict(json.loads(jstr))

            if byline.rec < cmd.end:
                print("airnow_downloader: latest report (%s) is earlier than the requested end." %
                      byline.rec.as_iso8601(), file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: directories...

        if cmd.verbose:
            print("airnow_downloader: making directories...", end='', file=sys.stderr)
            sys.stderr.flush()

        Filesystem.mkdir(dir_name)

        if cmd.verbose:
            print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: env download...

        env_filename = file_path + '-' + task.topic + '.csv'

        if cmd.verbose:
            print("airnow_downloader: downloading %s data..." % task.topic, end='', file=sys.stderr)
            sys.stderr.flush()

        args = ['./aws_topic_history.py', task.environment_path(), '-s', start, '-e', end]
        sp1 = Popen(args, stdout=PIPE)

        args = ['./node.py', 'rec', 'tag', 'src'] + ['val.' + param for param in task.parameters]
        sp2 = Popen(args, stdin=sp1.stdout, stdout=PIPE)

        args = ['./sample_aggregate.py', '-c', task.checkpoint]
        sp3 = Popen(args, stdin=sp2.stdout, stdout=PIPE)

        args = ['./csv_writer.py', env_filename]
        sp4 = Popen(args, stdin=sp3.stdout)

        sp4.wait()

        if sp4.returncode > 0:
            print("airnow_downloader: %s download failed with exit code %s." % (task.topic, sp4.returncode),
                  file=sys.stderr)
            exit(sp4.returncode)

        if cmd.verbose:
            print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: status download...

        status_filename = file_path + '-status.csv'

        if cmd.verbose:
            print("airnow_downloader: downloading status data...", end='', file=sys.stderr)
            sys.stderr.flush()

        args = ['./aws_topic_history.py', task.status_path(), '-s', start, '-e', end]
        sp1 = Popen(args, stdout=PIPE)

        args = ['./node.py', 'rec', 'tag', 'val.tz', 'val.sch', 'val.gps', 'val.airnow']
        sp2 = Popen(args, stdin=sp1.stdout, stdout=PIPE)

        args = ['./sample_aggregate.py', '-c', task.checkpoint]
        sp3 = Popen(args, stdin=sp2.stdout, stdout=PIPE)

        args = ['./csv_writer.py', status_filename]
        sp4 = Popen(args, stdin=sp3.stdout)

        sp4.wait()

        if sp4.returncode > 0:
            print("airnow_downloader: status download failed with exit code %s." % sp4.returncode, file=sys.stderr)
            exit(sp4.returncode)

        if cmd.verbose:
            print("done.", file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run: join...

        joined_filename = file_path + '-joined.csv'

        if cmd.verbose:
            print("airnow_downloader: joining...", end='', file=sys.stderr)
            sys.stderr.flush()

        args = ['./csv_join.py', '-i', '-l', task.topic, 'rec', env_filename, '-r', 'status', 'rec', status_filename]
        sp1 = Popen(args, stdout=PIPE)

        args = ['./csv_writer.py', joined_filename]
        sp2 = Popen(args, stdin=sp1.stdout)

        sp2.wait()

        if sp2.returncode > 0:
            print("airnow_downloader: join failed with exit code %s." % sp2.returncode, file=sys.stderr)
            exit(sp2.returncode)

        if cmd.verbose:
            print("done.", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("airnow_downloader: KeyboardInterrupt", file=sys.stderr)
