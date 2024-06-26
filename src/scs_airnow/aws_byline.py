#!/usr/bin/env python3

"""
Created on 25 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis

DESCRIPTION
The aws_byline utility is used to find the date / time of the most-recently published message for a given topic
or device. The user may specify a topic path (find all devices that have published to the given topic), or a device tag
(find all topics which the given device has published to), but not both. A further option --all reports all bylines.

Output is in the form of zero or more JSON documents, indicating the device, topic and localised date / time for each
latest sense event.

Note that deleting a device / topic pair does not affect the topic messages - the corresponding messages should be
deleted using the scs_lambda aws_message_delete utility as required.

The --credentials flag is only required where the user wishes to store multiple identities. Setting the credentials
is done interactively using the command line interface.

SYNOPSIS
aws_byline.py [-c CREDENTIALS] { -F { -d DEVICE | -t TOPIC [-l] | -a } [-x EXCLUDED] [-s] [-m] |
-D DEVICE TOPIC } [-i INDENT] [-v]

EXAMPLES
aws_byline.py -t south-coast-science-demo -v -x /control

DOCUMENT EXAMPLE - OUTPUT
{"device": "scs-bgx-401", "topic": "south-coast-science-demo/brighton/loc/1/climate",
"lastSeenTime": "2020-10-23T08:52:20Z", "last_write": "2020-10-23T08:52:20Z",
"message": "{\"val\": {\"hmd\": 68.4, \"tmp\": 19.8, \"bar\": null}, \"rec\": \"2020-10-23T08:52:20Z\",
\"tag\": \"scs-bgx-401\"}"}

SEE ALSO
scs_analysis/aws_topic_history
scs_analysis/aws_topic_origin
scs_analysis/cognito_user_credentials

scs_lambda/aws_message_delete
"""

import sys

from scs_analysis.cmd.cmd_aws_byline import CmdAWSByline
from scs_analysis.handler.batch_download_reporter import BatchDownloadReporter

from scs_core.aws.manager.byline.byline_finder import BylineFinder
from scs_core.aws.manager.byline.byline_manager import BylineManager

from scs_core.aws.security.cognito_client_credentials import CognitoClientCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.client.http_exception import HTTPException
from scs_core.client.network import Network

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    group = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSByline()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('aws_byline', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # authentication...

        credentials = CognitoClientCredentials.load_for_user(Host, name=cmd.credentials_name)

        if not credentials:
            exit(1)

        gatekeeper = CognitoLoginManager()
        auth = gatekeeper.user_login(credentials)

        if not auth.is_ok():
            logger.error("login: %s." % auth.authentication_status.description)
            exit(1)


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        finder = BylineFinder(reporter=BatchDownloadReporter('bylines'))

        manager = BylineManager()


        # ------------------------------------------------------------------------------------------------------------
        # check...

        if not Network.is_available():
            logger.info("waiting for network")
            Network.wait()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        latest = None

        if cmd.delete:
            manager.delete(auth.id_token, cmd.delete_device, cmd.delete_topic)
            group = finder.find_bylines_for_device(auth.id_token, cmd.delete_device, include_messages=False)

        elif cmd.find:
            if cmd.topic:
                group = finder.find_bylines_for_topic(auth.id_token, cmd.topic, excluded=cmd.excluded,
                                                      strict_tags=cmd.strict, include_messages=cmd.include_messages)

            elif cmd.device:
                group = finder.find_bylines_for_device(auth.id_token, cmd.device, excluded=cmd.excluded,
                                                       include_messages=cmd.include_messages)

            else:
                group = finder.find_bylines(auth.id_token, excluded=cmd.excluded, include_messages=cmd.include_messages)

        # report...
        report = []
        for byline in group.bylines:
            if cmd.latest:
                if latest is None or latest.rec < byline.rec:
                    latest = byline

            else:
                report.append(byline.as_json())

        if cmd.latest and latest is not None:
            jdict = latest.as_json()
            print(JSONify.dumps(jdict, indent=cmd.indent))

        else:
            print(JSONify.dumps(report, indent=cmd.indent))

            try:
                logger.info("found: %s" % len(report))
            except TypeError:
                pass


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except HTTPException as ex:
        logger.error(ex.error_report)
        exit(1)

    except Exception as ex:
        logger.error(ex.__class__.__name__)
        exit(1)

    finally:
        if cmd.verbose and cmd.find and group is not None and len(group):
            latest_pub = group.latest_pub()
            latest_iso = None if latest_pub is None else latest_pub.as_iso8601()

            logger.info("latest_pub: %s" % latest_iso)
