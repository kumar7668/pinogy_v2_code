#!/bin/bash
echo "Deploying $1"
bash $(pwd)/devops/gcp/scripts/gen_deploy.sh $1
echo "HPA"
bash $(pwd)/devops/gcp/scripts/gen_hpa.sh $1
echo "Jobs"
bash $(pwd)/devops/gcp/scripts/gen_job.sh $1
echo "Service"
bash $(pwd)/devops/gcp/scripts/gen_service.sh $1
echo "Pod Disruption Budget"
bash $(pwd)/devops/gcp/scripts/gen_pdb.sh $1
echo "Backend Config"
bash $(pwd)/devops/gcp/scripts/gen_config.sh $1
echo "Completed $1"
