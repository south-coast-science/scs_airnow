#!/usr/bin/env python3

"""
Created on 13 March 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The aqcsv_task_manager utility is used to

SYNOPSIS
aqcsv_task_manager.py [{ -l | -s [-c CODE] ORG GROUP LOC TOPIC DEVICE CHECKPOINT P1..PN | -d ORG GROUP LOC TOPIC }] [-v]

EXAMPLES
./aqcsv_task_manager.py -v -s -c 321MM987654321 scs demo 1 particulates praxis-000401 **:/01:00 val.pm1 val.pm2p5

FILES
~/SCS/aws/aqcsv_mapping_tasks.json

DOCUMENT EXAMPLE
{"tasks": {"('south-coast-science-demo', 'brighton', 1, 'particulates')": {"org": "south-coast-science-demo",
"group": "brighton", "loc": 1, "topic": "particulates", "device": "praxis-000401",
"parameters": ["val.pm1", "val.pm2p5", "val.pm10"], "checkpoint": "**:/01:00",
"site-code": "123MM123456789", "pocs": {"88101": 2, "85101": 3},
"latest-rec": "2019-03-13T12:45:00Z"}}}

SEE ALSO
scs_airnow/aqcsv_mapper
"""

import sys

from scs_airnow.cmd.cmd_aqcsv_task_manager import CmdAQCSVTaskManager

from scs_core.aqcsv.connector.datum_mapping import DatumMapping
from scs_core.aqcsv.connector.mapping_task import MappingTask, MappingTaskList

from scs_core.data.checkpoint_generator import CheckpointGenerator
from scs_core.data.datum import Datum
from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# TODO: should be able to handle POCs

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAQCSVTaskManager()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aqcsv_task_manager: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    tasks = MappingTaskList.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # list...
    if cmd.list:
        for task in tasks.items():
            print(JSONify.dumps(task))

        exit(0)

    # set...
    if cmd.is_set():
        if not Datum.is_numeric(cmd.set_loc):
            print("aqcsv_task_manager: the loc value %s should be an integer." % cmd.delete_loc,
                  file=sys.stderr)
            exit(2)

        if not DatumMapping.is_valid_topic(cmd.set_topic):
            print("aqcsv_task_manager: the topic %s is invalid." % cmd.set_topic,
                  file=sys.stderr)
            exit(2)

        if not CheckpointGenerator.is_valid(cmd.set_checkpoint):
            print("aqcsv_task_manager: the checkpoint specification %s is invalid." % cmd.set_checkpoint,
                  file=sys.stderr)
            exit(2)

        site_code = None if cmd.code is None else cmd.code

        task = MappingTask(cmd.set_org, cmd.set_group, cmd.set_loc, cmd.set_topic, cmd.set_device,
                           cmd.set_parameters, cmd.set_checkpoint, site_code, {}, None)

        tasks.insert(task)
        tasks.save(Host)

    # delete...
    if cmd.is_delete():
        if not Datum.is_numeric(cmd.delete_loc):
            print("aqcsv_task_manager: the loc value %s should be an integer." % cmd.delete_loc,
                  file=sys.stderr)
            exit(2)

        if not DatumMapping.is_valid_topic(cmd.delete_topic):
            print("aqcsv_task_manager: the topic %s is invalid." % cmd.delete_topic,
                  file=sys.stderr)
            exit(2)

        tasks.remove((cmd.delete_org, cmd.delete_group, int(cmd.delete_loc), cmd.delete_topic))
        tasks.save(Host)

    # report...
    if tasks:
        print(JSONify.dumps(tasks))
