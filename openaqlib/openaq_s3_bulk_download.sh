#!/bin/bash

set -eux
DATADIR=/tmp/openaq
AWS=/home/mod/software/aws

# for DATE in $dates; do
startdate=2020-01-01
enddate=2020-01-02

DATE="$startdate"

while true; do
    echo "$DATE"
    [ "$DATE" \< "$enddate" ] || break
    mkdir -p $DATADIR/$DATE
    $AWS s3 cp --recursive s3://openaq-fetches/realtime-gzipped/$DATE $DATADIR/$DATE
    DATE=$( date +%Y-%m-%d --date "$DATE +1 day" )
done
