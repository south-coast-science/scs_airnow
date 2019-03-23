#!/usr/bin/env python3

"""
Created on 13 March 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The airnow_task_manager utility is used to

SYNOPSIS
airnow_task_manager.py [-v] [{ -l | -s [-c CODE] ORG GROUP LOC TOPIC DEVICE CHECKPOINT UPLOAD_START P1..PN |
-d ORG GROUP LOC TOPIC }]

EXAMPLES
./airnow_task_manager.py -v -s -c 321MM987654321 scs demo 1 particulates praxis-000401 **:/01:00 val.pm1 val.pm2p5

FILES
~/SCS/aws/aqcsv_mapping_tasks.json

DOCUMENT EXAMPLE
{"tasks": {"('south-coast-science-demo', 'brighton', 1, 'particulates')": {"org": "south-coast-science-demo",
"group": "brighton", "loc": 1, "topic": "particulates", "device": "praxis-000401",
"parameters": ["pm1", "pm2p5", "pm10"], "checkpoint": "**:/01:00", "agency-code": "SSSSSSSSSS",
"site-code": "123MM123456789", "pocs": {}, "upload-start": "2019-02-01T00:00:00Z", "upload-end": null}}}

SEE ALSO
scs_analysis/aqcsv_mapper
scs_analysis/airnow_task_manager
"""

import sys

from scs_airnow.cmd.cmd_airnow_task_manager import CmdAirNowTaskManager

from scs_core.aqcsv.connector.datum_mapping import DatumMapping
from scs_core.aqcsv.connector.airnow_mapping_task import MappingTask, AirNowMappingTaskList

from scs_core.data.checkpoint_generator import CheckpointGenerator
from scs_core.data.datum import Datum
from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# TODO: should be able to handle POCs

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowTaskManager()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("airnow_task_manager: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # MappingTaskList...
    tasks = AirNowMappingTaskList.load(Host)


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
            print("airnow_task_manager: the loc value %s should be an integer." % cmd.delete_loc,
                  file=sys.stderr)
            exit(2)

        if not DatumMapping.is_valid_topic(cmd.set_topic):
            print("airnow_task_manager: the topic %s is invalid." % cmd.set_topic,
                  file=sys.stderr)
            exit(2)

        if not CheckpointGenerator.is_valid(cmd.set_checkpoint):
            print("airnow_task_manager: the checkpoint specification %s is invalid." % cmd.set_checkpoint,
                  file=sys.stderr)
            exit(2)

        task = MappingTask(cmd.set_org, cmd.set_group, cmd.set_loc, cmd.set_topic, cmd.set_device,
                           cmd.set_parameters, cmd.set_checkpoint, cmd.agency_code, cmd.site_code, {},
                           cmd.set_upload_start, None)

        tasks.insert(task)
        tasks.save(Host)

    # delete...
    if cmd.is_delete():
        if not Datum.is_numeric(cmd.delete_loc):
            print("airnow_task_manager: the loc value %s should be an integer." % cmd.delete_loc,
                  file=sys.stderr)
            exit(2)

        if not DatumMapping.is_valid_topic(cmd.delete_topic):
            print("airnow_task_manager: the topic %s is invalid." % cmd.delete_topic,
                  file=sys.stderr)
            exit(2)

        tasks.remove((cmd.delete_org, cmd.delete_group, int(cmd.delete_loc), cmd.delete_topic))
        tasks.save(Host)

    # report...
    if tasks:
        print(JSONify.dumps(tasks))
