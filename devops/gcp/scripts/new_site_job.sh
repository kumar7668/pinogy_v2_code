#!/bin/bash
mkdir -p $(pwd)/devops/gcp/jobs
cp $(pwd)/devops/gcp/scripts/templates/newsitejob.yaml $1-newsite.yaml
sed -i "s/SITENUM/$1/g" $1-newsite.yaml
mv $1-newsite.yaml $(pwd)/devops/gcp/jobs/