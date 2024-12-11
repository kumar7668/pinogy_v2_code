#!/bin/bash
mkdir -p $(pwd)/devops/gcp/pdbs
cp $(pwd)/devops/gcp/scripts/templates/pdb.yaml $1.yaml
sed -i "s/SITENUM/$1/g" $1.yaml
mv $1.yaml $(pwd)/devops/gcp/pdbs/
echo "gen_deploy: mv $1.yaml $(pwd)/devops/gcp/pdbs/"