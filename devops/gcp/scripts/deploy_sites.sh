#!/bin/bash
while read p; do
  if [ "$p" != "website0995" ]; then
    echo "Setting image for $p = $1 via the deploy_sites script"
    kubectl set image deploy -n websites-v2 $p $p=$1
  fi
done <$(pwd)/devops/gcp/scripts/site_list.txt