#!/bin/bash
bash $(pwd)/devops/gcp/scripts/gen_site.sh $1
bash $(pwd)/devops/gcp/scripts/new_site_job.sh $1