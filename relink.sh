#!/usr/bin/env bash

# For development use only...
# Make (or update) hard links to source files in other repos
# - required, because PyCharm remakes files, rather than updating them.

# https://unix.stackexchange.com/questions/231955/why-wont-my-hard-links-update-each-other

SOURCE=../scs_analysis/src/scs_analysis
TARGET=src/scs_airnow

ln -vf ${SOURCE}/aws_api_auth.py                        ${TARGET}/aws_api_auth.py
ln -vf ${SOURCE}/aws_byline.py                          ${TARGET}/aws_byline.py
ln -vf ${SOURCE}/aws_topic_history.py                   ${TARGET}/aws_topic_history.py
ln -vf ${SOURCE}/csv_join.py                            ${TARGET}/csv_join.py
ln -vf ${SOURCE}/csv_reader.py                          ${TARGET}/csv_reader.py
ln -vf ${SOURCE}/csv_writer.py                          ${TARGET}/csv_writer.py
ln -vf ${SOURCE}/node.py                                ${TARGET}/node.py
ln -vf ${SOURCE}/sample_aggregate.py                    ${TARGET}/sample_aggregate.py

ln -vf ${SOURCE}/cmd/cmd_aws_api_auth.py                ${TARGET}/cmd/cmd_aws_api_auth.py
ln -vf ${SOURCE}/cmd/cmd_aws_byline.py                  ${TARGET}/cmd/cmd_aws_byline.py
ln -vf ${SOURCE}/cmd/cmd_aws_topic_history.py           ${TARGET}/cmd/cmd_aws_topic_history.py
ln -vf ${SOURCE}/cmd/cmd_csv_join.py                    ${TARGET}/cmd/cmd_csv_join.py
ln -vf ${SOURCE}/cmd/cmd_csv_reader.py                  ${TARGET}/cmd/cmd_csv_reader.py
ln -vf ${SOURCE}/cmd/cmd_csv_writer.py                  ${TARGET}/cmd/cmd_csv_writer.py
ln -vf ${SOURCE}/cmd/cmd_node.py                        ${TARGET}/cmd/cmd_node.py
ln -vf ${SOURCE}/cmd/cmd_sample_aggregate.py            ${TARGET}/cmd/cmd_sample_aggregate.py

ln -vf ${SOURCE}/handler/aws_topic_history_reporter.py   ${TARGET}/helper/aws_topic_history_reporter.py
ln -vf ${SOURCE}/handler/sample_aggregate.py             ${TARGET}/helper/sample_aggregate.py
