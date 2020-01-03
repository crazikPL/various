#!/bin/bash

GAPI="https://grafana.url/api"
API_TOKEN=""

for i in `curl -s -k -H "Authorization: Bearer ${API_TOKEN}" ${GAPI}/search\?query\=\&  |jq '.' |grep -i uri |awk -F \" '{print $4}'`; do 
    curl -sSL -k -H  "Authorization: Bearer ${API_TOKEN}"  ${GAPI}/dashboards/$i > $(echo $i | sed 's,db/,,g').json
done

