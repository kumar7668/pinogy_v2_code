#!/bin/bash
mkdir -p $(pwd)/devops/gcp/configs
cp $(pwd)/devops/gcp/scripts/templates/config.yaml $1.yaml
sed -i "s/SITENUM/$1/g" $1.yaml
mv $1.yaml $(pwd)/devops/gcp/configs/
echo "gen_deploy: mv $1.yaml $(pwd)/devops/gcp/configs/"