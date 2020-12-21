#/bin/sh

set -eux

DATADIR=/home/esowc24/data/openaq

# for DATE in $dates; do
startdate=2018-01-01
enddate=2019-01-01

DATE="$startdate"

while true; do
    echo "$DATE"
    [ "$DATE" \< "$enddate" ] || break
    mkdir -p $DATADIR/$DATE
    aws s3 cp --recursive s3://openaq-fetches/realtime-gzipped/$DATE $DATADIR/$DATE
    DATE=$( date +%Y-%m-%d --date "$DATE +1 day" )
done
