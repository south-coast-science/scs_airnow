#!/usr/bin/env python3

"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.aqcsv.connector.datum_mapping import DatumMapping

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

pm1_mapping = DatumMapping("particulates", "pm1")
print(JSONify.dumps(pm1_mapping), file=sys.stderr)
print("-")

pm2p5_mapping = DatumMapping("particulates", "pm2p5")
print(JSONify.dumps(pm2p5_mapping), file=sys.stderr)
print("-")

pm10_mapping = DatumMapping("particulates", "pm10")
print(JSONify.dumps(pm10_mapping), file=sys.stderr)
print("-")

for line in sys.stdin:
    jstr = line.strip()
    datum = PathDict.construct_from_jstr(jstr)

    record = pm1_mapping.aqcsv_record(datum)
    print(JSONify.dumps(record))

    record = pm2p5_mapping.aqcsv_record(datum)
    print(JSONify.dumps(record))

    record = pm10_mapping.aqcsv_record(datum)
    print(JSONify.dumps(record))
