#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis

DESCRIPTION
The aqcsv_mapper utility is used to

SYNOPSIS


EXAMPLES


FILES
~/SCS/aws/aqcsv_mapper.json

DOCUMENT EXAMPLE
{"endpoint": "aws.southcoastscience.com", "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"}

SEE ALSO
scs_analysis/aws_topic_history
"""

import sys

from scs_airnow.cmd.cmd_aqcsv_mapper import CmdAQCSVMapper

from scs_core.aqcsv.connector.datum_mapping import DatumMapping
from scs_core.aqcsv.connector.mapping_task import MappingTaskList

from scs_core.data.datum import Datum
from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAQCSVMapper()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if not Datum.is_numeric(cmd.task_loc):
        print("aqcsv_mapper: the loc value %s should be an integer." % cmd.task_loc, file=sys.stderr)
        exit(2)

    if not DatumMapping.is_valid_topic(cmd.task_topic):
        print("aqcsv_mapper: the topic %s is invalid." % cmd.task_topic, file=sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aqcsv_mapper: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MappingTask...
        tasks = MappingTaskList.load(Host)
        task = tasks.item((cmd.task_org, cmd.task_group, int(cmd.task_loc), cmd.task_topic))

        if task is None:
            print("aqcsv_mapper: task not found.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("aqcsv_mapper: %s" % task, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            jstr = line.strip()
            datum = PathDict.construct_from_jstr(jstr)

            for mapping in task.mappings():
                record = mapping.aqcsv_record(datum)
                print(JSONify.dumps(record))

            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("aqcsv_mapper: KeyboardInterrupt", file=sys.stderr)
