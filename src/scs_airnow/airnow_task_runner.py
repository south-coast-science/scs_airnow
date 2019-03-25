#!/usr/bin/env python3

"""
Created on 14 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_airnow

DESCRIPTION
The airnow_task_runner utility is used to

SYNOPSIS
airnow_task_runner.py -p [[DD-]HH:]MM -d DIR [-e END] [-c] [-v]

EXAMPLES


SEE ALSO
scs_analysis/airnow_task_manager
scs_analysis/aqcsv_task
"""

import sys

from subprocess import Popen

from scs_airnow.cmd.cmd_airnow_task_runner import CmdAirNowTaskRunner
from scs_airnow.helper.airnow_availability import AirNowAvailability

from scs_core.aqcsv.connector.airnow_mapping_task import AirNowMappingTaskList

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sync.interval_timer import IntervalTimer

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowTaskRunner()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if not cmd.is_valid_sample_period():
        print("airnow_task_runner: invalid format for sample period.", file=sys.stderr)
        exit(2)

    if not cmd.is_valid_end():
        print("airnow_task_runner: invalid format for end datetime.", file=sys.stderr)
        exit(2)

    if cmd.verbose:
        print("airnow_task_runner: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MappingTask...
        tasks = AirNowMappingTaskList.load(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        now = LocalizedDatetime.now() if cmd.end is None else cmd.end

        # tasks...
        for task in tasks.items():
            if cmd.verbose:
                print("airnow_task_runner: %s" % task, file=sys.stderr)
                sys.stderr.flush()

            # initialise...
            report_count = 0

            period_start = task.upload_end if task.upload_end is not None else task.upload_start
            period_end = period_start + cmd.sample_period

            timer = IntervalTimer(60)                           # minute intervals give filename integrity

            # periods...
            while timer.true():
                if period_end > now:
                    break

                print("airnow_task_runner: start: %s end: %s..." % (period_start.as_iso8601(), period_end.as_iso8601()),
                      file=sys.stderr)

                # data availability...
                if cmd.check:
                    result = AirNowAvailability.check("airnow_task_runner", task, period_end, cmd.verbose)

                    if result != AirNowAvailability.OK:         # no more data for this task
                        break

                # task...
                args = ['./airnow_task.py', '-v', '-t', task.org, task.group, str(task.loc), task.topic,
                        '-s', period_start.as_iso8601(), '-e', period_end.as_iso8601(), '-d', cmd.dir]
                sp1 = Popen(args)

                sp1.wait()

                report_count += 1

                # next...
                period_start = period_end
                period_end += cmd.sample_period

                print("-")

            # report...
            if cmd.verbose:
                print("airnow_task_runner: reports for task: %d" % report_count, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("airnow_task_runner: KeyboardInterrupt", file=sys.stderr)
