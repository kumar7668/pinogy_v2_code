#!/bin/bash
echo "Deleting sites"
while read d; do
  echo "Deleting the deploy for $d"
  kubectl delete deploy --ignore-not-found -n websites-v2 $d
  echo "Deleting the service for $d-service"
  kubectl delete service --ignore-not-found -n websites-v2 $d-service
done <$(pwd)/devops/gcp/scripts/site_list_delete.txt