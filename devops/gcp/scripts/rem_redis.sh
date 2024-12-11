#!/bin/bash
# DO NOT RUN THIS FILE LOCAL THIS IS FOR PIPELINE USAGE ONLY!
find $(pwd)/devops/gcp/secrets -type f -exec sed -i "/REDIS_SERVICE/d" {} \;