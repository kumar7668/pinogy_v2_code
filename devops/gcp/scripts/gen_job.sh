#!/bin/bash
mkdir -p $(pwd)/devops/gcp/jobs
cp $(pwd)/devops/gcp/scripts/templates/migrationjob.yaml $1.yaml
sed -i "s/SITENUM/$1/g" $1.yaml
mv $1.yaml $(pwd)/devops/gcp/jobs/
echo "gen_deploy: mv $1.yaml $(pwd)/devops/gcp/jobs/"