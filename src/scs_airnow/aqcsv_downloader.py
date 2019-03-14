#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis

DESCRIPTION
The aqcsv_downloader utility is used to

SYNOPSIS
aqcsv_downloader.py -t ORG GROUP LOC TOPIC -s START -e END [-d DIR] [-v]

EXAMPLES


FILES
~/SCS/aws/aqcsv_downloader.json

DOCUMENT EXAMPLE
{"endpoint": "aws.southcoastscience.com", "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"}

SEE ALSO
scs_analysis/aws_topic_history
"""

import json
import os
import subprocess
import sys

from scs_airnow.cmd.cmd_aqcsv_downloader import CmdAQCSVDownloader

from scs_core.aqcsv.connector.mapping_task import MappingTaskList

from scs_core.aws.data.byline import Byline

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAQCSVDownloader()

    if not cmd.is_valid_start():
        print("aqcsv_downloader: invalid format for start datetime.", file=sys.stderr)
        exit(2)

    if not cmd.is_valid_end():
        print("aqcsv_downloader: invalid format for end datetime.", file=sys.stderr)
        exit(2)

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    verbose = ['-v'] if cmd.verbose else []

    if cmd.verbose:
        print("aqcsv_downloader: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MappingTask...
        tasks = MappingTaskList.load(Host)
        task = tasks.item((cmd.task_org, cmd.task_group, int(cmd.task_loc), cmd.task_topic))

        if task is None:
            print("aqcsv_downloader: task not found.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("aqcsv_downloader: %s" % task, file=sys.stderr)
            sys.stderr.flush()

        # datetimes...
        start = cmd.start.as_iso8601()
        end = cmd.end.as_iso8601()

        # available data...
        if cmd.verbose:
            print("checking for availability...", file=sys.stderr)

        args = ['aws_byline.py', '-t', task.environment_path()]
        jstr = subprocess.check_output(args + verbose).decode().strip()

        byline = Byline.construct_from_jdict(json.loads(jstr))              # TODO: handle multiple lines

        if byline.rec < cmd.end:
            print("aqcsv_downloader: latest report (%s) is earlier than the requested end." % byline.rec.as_iso8601(),
                  file=sys.stderr)
            exit(1)

        # directories...
        if cmd.verbose:
            print("-", file=sys.stderr)
            print("making directories...", file=sys.stderr)

        dir_name =  task.site_code if cmd.dir is None else os.path.join(cmd.dir, task.site_code)
        file_prefix = task.filename() if cmd.file_prefix is None else cmd.file_prefix

        file_path = os.path.join(dir_name, file_prefix)

        args = ['mkdir', dir_name]
        ps1 = subprocess.Popen(args)

        ps1.wait()


        # ------------------------------------------------------------------------------------------------------------
        # run env download...

        topic_filename = file_path + '-' + task.topic + '.csv'

        if cmd.verbose:
            print("-", file=sys.stderr)
            print("downloading %s data..." % task.topic, file=sys.stderr)

        args = ['aws_topic_history.py', task.environment_path(), '-s', start, '-e', end]
        ps1 = subprocess.Popen(args + verbose, stdout=subprocess.PIPE)

        args = ['node.py', 'rec', 'tag', 'src'] + ['val.' + param for param in task.parameters]
        ps2 = subprocess.Popen(args + verbose, stdin=ps1.stdout, stdout=subprocess.PIPE)

        args = ['sample_aggregate.py', '-c', task.checkpoint]
        ps3 = subprocess.Popen(args + verbose, stdin=ps2.stdout, stdout=subprocess.PIPE)

        args = ['csv_writer.py', topic_filename]
        ps4 = subprocess.Popen(args, stdin=ps3.stdout)

        ps4.wait()


        # ------------------------------------------------------------------------------------------------------------
        # run status download...

        status_filename = file_path + '-status.csv'

        if cmd.verbose:
            print("-", file=sys.stderr)
            print("downloading status data...", file=sys.stderr)

        args = ['aws_topic_history.py', task.status_path(), '-s', start, '-e', end]
        ps1 = subprocess.Popen(args + verbose, stdout=subprocess.PIPE)

        args = ['node.py', 'rec', 'val.tz', 'val.sch', 'val.gps', 'val.airnow']
        ps2 = subprocess.Popen(args + verbose, stdin=ps1.stdout, stdout=subprocess.PIPE)

        args = ['sample_aggregate.py', '-c', task.checkpoint]
        ps3 = subprocess.Popen(args + verbose, stdin=ps2.stdout, stdout=subprocess.PIPE)

        args = ['csv_writer.py', status_filename]
        ps4 = subprocess.Popen(args, stdin=ps3.stdout)

        ps4.wait()


        # ------------------------------------------------------------------------------------------------------------
        # run join...

        joined_filename = file_path + '-joined.csv'

        if cmd.verbose:
            print("-", file=sys.stderr)
            print("joining data...", file=sys.stderr)

        args = ['csv_join.py', '-i', '-l', task.topic, 'rec', topic_filename, '-r', 'status', 'rec', status_filename]
        ps1 = subprocess.Popen(args + verbose, stdout=subprocess.PIPE)

        args = ['csv_writer.py', joined_filename]
        ps2 = subprocess.Popen(args, stdin=ps1.stdout)

        ps2.wait()

        if cmd.verbose:
            print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("aqcsv_downloader: KeyboardInterrupt", file=sys.stderr)
