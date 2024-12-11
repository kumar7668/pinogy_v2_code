#!/bin/bash
# DO NOT RUN THIS FILE LOCAL THIS IS FOR PIPELINE USAGE ONLY!
find $(pwd)/devops/gcp/jobs_beta -type f -exec sed -i "s/IMAGE_TAG/$1/g" {} \;
find $(pwd)/devops/gcp/deployments_beta -type f -exec sed -i "s/IMAGE_TAG/$1/g" {} \;
find $(pwd)/pinogy_app/settings -type f -exec sed -i "s/IMAGE_TAG/$1/g" {} \;
