#!/bin/bash
mkdir -p $(pwd)/devops/gcp/deployments
cp $(pwd)/devops/gcp/scripts/templates/deployment.yaml $1.yaml
sed -i "s/SITENUM/$1/g" $1.yaml
mv $1.yaml $(pwd)/devops/gcp/deployments/
echo "gen_deploy: mv $1.yaml $(pwd)/devops/gcp/deployments/"