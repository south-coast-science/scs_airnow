#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The airnow_mapper utility is used to

SYNOPSIS
airnow_mapper.py -t ORG GROUP LOC TOPIC [-v]

EXAMPLES


FILES
~/SCS/aws/airnow_mapper.json

DOCUMENT EXAMPLE
{"endpoint": "aws.southcoastscience.com", "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"}

SEE ALSO
scs_analysis/aqcsv_downloader
scs_analysis/aqcsv_task_manager
"""

import sys

from scs_airnow.cmd.cmd_airnow_mapper import CmdAirNowMapper

from scs_core.aqcsv.connector.datum_mapping import DatumMapping
from scs_core.aqcsv.connector.airnow_mapping_task import AirNowMappingTaskList

from scs_core.data.datum import Datum
from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    document_count = 0

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowMapper()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if not Datum.is_numeric(cmd.task_loc):
        print("airnow_mapper: the loc value %s should be an integer." % cmd.task_loc, file=sys.stderr)
        exit(2)

    if not DatumMapping.is_valid_topic(cmd.task_topic):
        print("airnow_mapper: the topic %s is invalid." % cmd.task_topic, file=sys.stderr)
        exit(2)

    if cmd.verbose:
        print("airnow_mapper: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MappingTask...
        tasks = AirNowMappingTaskList.load(Host)
        task = tasks.item((cmd.task_org, cmd.task_group, int(cmd.task_loc), cmd.task_topic))

        if task is None:
            print("airnow_mapper: task not found.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("airnow_mapper: %s" % task, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            datum = PathDict.construct_from_jstr(line.strip())

            if datum is None:
                continue

            document_count += 1

            for mapping in task.mappings():
                record = mapping.aqcsv_record(datum)
                jstr = JSONify.dumps(record)

                print(jstr)

            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("airnow_mapper: KeyboardInterrupt", file=sys.stderr)

    finally:
        if cmd.verbose:
            print("airnow_mapper: documents: %d" % document_count, file=sys.stderr)
