#!/usr/bin/env bash

# For development use only...
# Make (or update) hard links to source files in other repos
# - required, because PyCharm remakes files, rather than updating them.

SOURCE=../scs_analysis/src/scs_analysis
TARGET=src/scs_airnow

ln -vf ${SOURCE}/aws_api_auth.py                        ${TARGET}/aws_api_auth.py
ln -vf ${SOURCE}/aws_byline.py                          ${TARGET}/aws_byline.py
ln -vf ${SOURCE}/aws_mqtt_client.py                     ${TARGET}/aws_mqtt_client.py
ln -vf ${SOURCE}/aws_topic_history.py                   ${TARGET}/aws_topic_history.py
ln -vf ${SOURCE}/csv_join.py                            ${TARGET}/csv_join.py
ln -vf ${SOURCE}/csv_logger.py                          ${TARGET}/csv_logger.py
ln -vf ${SOURCE}/csv_logger_conf.py                     ${TARGET}/csv_logger_conf.py
ln -vf ${SOURCE}/csv_reader.py                          ${TARGET}/csv_reader.py
ln -vf ${SOURCE}/csv_writer.py                          ${TARGET}/csv_writer.py
ln -vf ${SOURCE}/node.py                                ${TARGET}/node.py
ln -vf ${SOURCE}/sample_aggregate.py                    ${TARGET}/sample_aggregate.py

ln -vf ${SOURCE}/cmd/cmd_aws_api_auth.py                ${TARGET}/cmd/cmd_aws_api_auth.py
ln -vf ${SOURCE}/cmd/cmd_aws_byline.py                  ${TARGET}/cmd/cmd_aws_byline.py
ln -vf ${SOURCE}/cmd/cmd_aws_topic_history.py           ${TARGET}/cmd/cmd_aws_topic_history.py
ln -vf ${SOURCE}/cmd/cmd_csv_join.py                    ${TARGET}/cmd/cmd_csv_join.py
ln -vf ${SOURCE}/cmd/cmd_csv_logger.py                  ${TARGET}/cmd/cmd_csv_logger.py
ln -vf ${SOURCE}/cmd/cmd_csv_logger_conf.py             ${TARGET}/cmd/cmd_csv_logger_conf.py
ln -vf ${SOURCE}/cmd/cmd_csv_reader.py                  ${TARGET}/cmd/cmd_csv_reader.py
ln -vf ${SOURCE}/cmd/cmd_csv_writer.py                  ${TARGET}/cmd/cmd_csv_writer.py
ln -vf ${SOURCE}/cmd/cmd_mqtt_client.py                 ${TARGET}/cmd/cmd_mqtt_client.py
ln -vf ${SOURCE}/cmd/cmd_node.py                        ${TARGET}/cmd/cmd_node.py
ln -vf ${SOURCE}/cmd/cmd_sample_aggregate.py            ${TARGET}/cmd/cmd_sample_aggregate.py

ln -vf ${SOURCE}/helper/aws_mqtt_client_handler.py      ${TARGET}/helper/aws_mqtt_client_handler.py
ln -vf ${SOURCE}/helper/aws_topic_history_reporter.py   ${TARGET}/helper/aws_topic_history_reporter.py
ln -vf ${SOURCE}/helper/mqtt_reporter.py                ${TARGET}/helper/mqtt_reporter.py
ln -vf ${SOURCE}/helper/sample_aggregate.py             ${TARGET}/helper/sample_aggregate.py
