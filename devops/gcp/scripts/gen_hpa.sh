#!/bin/bash
mkdir -p $(pwd)/devops/gcp/hpas
cp $(pwd)/devops/gcp/scripts/templates/hpa.yaml $1.yaml
sed -i "s/SITENUM/$1/g" $1.yaml
mv $1.yaml $(pwd)/devops/gcp/hpas/
echo "gen_deploy: mv $1.yaml $(pwd)/devops/gcp/hpas/"