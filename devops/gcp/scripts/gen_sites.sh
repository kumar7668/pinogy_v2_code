#!/bin/bash
echo "Creating sites via the gen_sites script"
while read p; do
  echo "Creating $p via the gen_site script"
  $(pwd)/devops/gcp/scripts/gen_site.sh $p
done <$(pwd)/devops/gcp/scripts/site_list.txt

echo "Listing the files in the gcp directory"
find $(pwd)/devops/gcp/ -ls

echo "Separating Dev Sites"
mkdir -p $(pwd)/devops/gcp/deployments_dev
mkdir -p $(pwd)/devops/gcp/jobs_dev
mkdir -p $(pwd)/devops/gcp/services_dev
mkdir -p $(pwd)/devops/gcp/configs_dev
while read v; do
  mv $(pwd)/devops/gcp/deployments/$v.yaml $(pwd)/devops/gcp/deployments_dev/$v.yaml
  mv $(pwd)/devops/gcp/jobs/$v.yaml $(pwd)/devops/gcp/jobs_dev/$v.yaml
  mv $(pwd)/devops/gcp/services/$v.yaml $(pwd)/devops/gcp/services_dev/$v.yaml
  mv $(pwd)/devops/gcp/configs/$v.yaml $(pwd)/devops/gcp/configs_dev/$v.yaml
done <$(pwd)/devops/gcp/scripts/site_list_dev.txt

echo "Separating Beta Sites"
mkdir -p $(pwd)/devops/gcp/deployments_beta
mkdir -p $(pwd)/devops/gcp/jobs_beta
mkdir -p $(pwd)/devops/gcp/services_beta
mkdir -p $(pwd)/devops/gcp/configs_beta
while read v; do
  mv $(pwd)/devops/gcp/deployments/$v.yaml $(pwd)/devops/gcp/deployments_beta/$v.yaml
  mv $(pwd)/devops/gcp/jobs/$v.yaml $(pwd)/devops/gcp/jobs_beta/$v.yaml
  mv $(pwd)/devops/gcp/services/$v.yaml $(pwd)/devops/gcp/services_beta/$v.yaml
  mv $(pwd)/devops/gcp/configs/$v.yaml $(pwd)/devops/gcp/configs_beta/$v.yaml
done <$(pwd)/devops/gcp/scripts/site_list_beta.txt

echo "Separating Hotfix Sites"
mkdir -p $(pwd)/devops/gcp/deployments_hotfix
mkdir -p $(pwd)/devops/gcp/jobs_hotfix
while read v; do
  mv $(pwd)/devops/gcp/deployments/$v.yaml $(pwd)/devops/gcp/deployments_hotfix/$v.yaml
  mv $(pwd)/devops/gcp/jobs/$v.yaml $(pwd)/devops/gcp/jobs_hotfix/$v.yaml
done <$(pwd)/devops/gcp/scripts/site_list_hotfix.txt
echo "Completed the gen_sites script"