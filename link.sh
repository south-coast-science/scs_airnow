#!/usr/bin/env bash

# make (or update) hard links to source files in other repos

SOURCE_DIR=../scs_analysis/src/scs_analysis
TARGET_DIR=src/scs_airnow

ln -vf ${SOURCE_DIR}/aws_api_auth.py                        ${TARGET_DIR}/aws_api_auth.py
ln -vf ${SOURCE_DIR}/aws_byline.py                          ${TARGET_DIR}/aws_byline.py
ln -vf ${SOURCE_DIR}/aws_mqtt_client.py                     ${TARGET_DIR}/aws_mqtt_client.py
ln -vf ${SOURCE_DIR}/aws_topic_history.py                   ${TARGET_DIR}/aws_topic_history.py
ln -vf ${SOURCE_DIR}/csv_join.py                            ${TARGET_DIR}/csv_join.py
ln -vf ${SOURCE_DIR}/csv_logger.py                          ${TARGET_DIR}/csv_logger.py
ln -vf ${SOURCE_DIR}/csv_logger_conf.py                     ${TARGET_DIR}/csv_logger_conf.py
ln -vf ${SOURCE_DIR}/csv_reader.py                          ${TARGET_DIR}/csv_reader.py
ln -vf ${SOURCE_DIR}/csv_writer.py                          ${TARGET_DIR}/csv_writer.py
ln -vf ${SOURCE_DIR}/node.py                                ${TARGET_DIR}/node.py
ln -vf ${SOURCE_DIR}/sample_aggregate.py                    ${TARGET_DIR}/sample_aggregate.py

ln -vf ${SOURCE_DIR}/cmd/cmd_aws_api_auth.py                ${TARGET_DIR}/cmd/cmd_aws_api_auth.py
ln -vf ${SOURCE_DIR}/cmd/cmd_aws_byline.py                  ${TARGET_DIR}/cmd/cmd_aws_byline.py
ln -vf ${SOURCE_DIR}/cmd/cmd_aws_topic_history.py           ${TARGET_DIR}/cmd/cmd_aws_topic_history.py
ln -vf ${SOURCE_DIR}/cmd/cmd_csv_join.py                    ${TARGET_DIR}/cmd/cmd_csv_join.py
ln -vf ${SOURCE_DIR}/cmd/cmd_csv_logger.py                  ${TARGET_DIR}/cmd/cmd_csv_logger.py
ln -vf ${SOURCE_DIR}/cmd/cmd_csv_logger_conf.py             ${TARGET_DIR}/cmd/cmd_csv_logger_conf.py
ln -vf ${SOURCE_DIR}/cmd/cmd_csv_reader.py                  ${TARGET_DIR}/cmd/cmd_csv_reader.py
ln -vf ${SOURCE_DIR}/cmd/cmd_csv_writer.py                  ${TARGET_DIR}/cmd/cmd_csv_writer.py
ln -vf ${SOURCE_DIR}/cmd/cmd_mqtt_client.py                 ${TARGET_DIR}/cmd/cmd_mqtt_client.py
ln -vf ${SOURCE_DIR}/cmd/cmd_node.py                        ${TARGET_DIR}/cmd/cmd_node.py
ln -vf ${SOURCE_DIR}/cmd/cmd_sample_aggregate.py            ${TARGET_DIR}/cmd/cmd_sample_aggregate.py

ln -vf ${SOURCE_DIR}/helper/aws_mqtt_client_handler.py      ${TARGET_DIR}/helper/aws_mqtt_client_handler.py
ln -vf ${SOURCE_DIR}/helper/aws_topic_history_reporter.py   ${TARGET_DIR}/helper/aws_topic_history_reporter.py
ln -vf ${SOURCE_DIR}/helper/mqtt_reporter.py                ${TARGET_DIR}/helper/mqtt_reporter.py
ln -vf ${SOURCE_DIR}/helper/sample_aggregate.py             ${TARGET_DIR}/helper/sample_aggregate.py
