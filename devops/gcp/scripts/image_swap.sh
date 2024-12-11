#!/bin/bash
# DO NOT RUN THIS FILE LOCAL THIS IS FOR PIPELINE USAGE ONLY!
echo "find $(pwd)/devops/gcp/jobs -type f -exec sed -i \"s/IMAGE_TAG/$1/g\" {} \;"
find $(pwd)/devops/gcp/jobs -type f -exec sed -i "s/IMAGE_TAG/$1/g" {} \;
echo "find $(pwd)/devops/gcp/deployments -type f -exec sed -i \"s/IMAGE_TAG/$1/g\" {} \;"
find $(pwd)/devops/gcp/deployments -type f -exec sed -i "s/IMAGE_TAG/$1/g" {} \;
echo "find $(pwd)/pinogy_app/settings -type f -exec sed -i \"s/IMAGE_TAG/$1/g\" {} \;"
find $(pwd)/pinogy_app/settings -type f -exec sed -i "s/IMAGE_TAG/$1/g" {} \;
