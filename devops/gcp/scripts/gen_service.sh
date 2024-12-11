#!/bin/bash
mkdir -p $(pwd)/devops/gcp/services
cp $(pwd)/devops/gcp/scripts/templates/service.yaml $1.yaml
sed -i "s/SITENUM/$1/g" $1.yaml
mv $1.yaml $(pwd)/devops/gcp/services/
echo "gen_deploy: mv $1.yaml $(pwd)/devops/gcp/services/"