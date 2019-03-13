#!/usr/bin/env bash

org=south-coast-science-demo
group=brighton
loc=1

topic=particulates
device=praxis-000401

ep1=val.pm1
ep2=val.pm2p5
ep3=val.pm10

period=10

checkpoint=**:/01:00

wd=../src/scs_airnow

# environment...
${wd}/aws_topic_history.py -v ${org}/${group}/loc/${loc}/${topic} -t ${period} | \
${wd}/node.py -v rec tag src ${ep1} ${ep2} ${ep3} | \
${wd}/sample_aggregate.py -v -c ${checkpoint} | \
${wd}/csv_writer.py -v data/${topic}-1min.csv
echo -

# device status...
${wd}/aws_topic_history.py -v ${org}/${group}/device/${device}/status -t ${period} | \
${wd}/node.py -v rec tag val.tz val.sch val.gps val.airnow | \
${wd}/sample_aggregate.py -v -c ${checkpoint} | \
${wd}/csv_writer.py -v data/status-1min.csv
echo -

# join...
${wd}/csv_join.py -v -i -l ${topic} rec data/${topic}-1min.csv -r status rec data/status-1min.csv | \
${wd}/csv_writer.py -v data/joined-1min.csv
echo -
