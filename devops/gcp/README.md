# DevOps Scripts
The scripts in the scripts directory can be used to generate a new site.  Currently the secrets and ingress are manual, the rest are scripted.
The script gen_site.sh is a roll up script to generate each piece.  All of the gen_ scripts currently take 1 parameter of "SITENUM" e.g. website0126
The script gen_sites.sh uses site_list.txt to generate all from a list of sites.

## Pipelines
There are 4 pipelines currently configured, the stage channel may be on the old hardware. [bitbucket-pipelines.yml](https://bitbucket.org/pinogycorp/pinogy-new-base/src/master/bitbucket-pipelines.yml) contains all the details of how each of these work.
1. Tag gcp* to configure cluster for all channels
1. Tag v* to build and release to the stable channel
1. Tag beta* to build and release to the beta channel
1. Tag hotfix to build and release to hotfix channel
### Configuring channels
All sites need to be on the stable site_list.txt. If you need to advance them to other channels you add them to the appropriate list and leave them on the master site_list (stable).
* [stable](https://bitbucket.org/pinogycorp/pinogy-new-base/src/master/devops/gcp/scripts/site_list.txt)
* [beta](https://bitbucket.org/pinogycorp/pinogy-new-base/src/master/devops/gcp/scripts/site_list_beta.txt)
* [hotfix](https://bitbucket.org/pinogycorp/pinogy-new-base/src/master/devops/gcp/scripts/site_list_hotfix.txt)

## New sites
A new site's resources and configuration can be deployed to production by adding it to the site_list.txt file.
1. Script the creation of the database, schema, user and put in bash script to be ran by pipeline.
1. Create script to add to ingress or add ingress to part of gen_sites
1. Update new site pipeline to call gen_site with image tag (SITENUM)
1. Create django fixtures to use for the base data

## Migration Process
To move the existing sites over for the test round the process is this:

### Add Ingress Stanzas
* Each site has 2 ingress domains, public and private, add both domains at once.
* The 2 stanzas are the http stanzas inside the "rules".
* Copy and change the values for the domains.
* Also change the backend service which contains the SITENUM in the format SITENUM-service.

### Database User & Permissions
* Create the database user and password using the values from the retrieved secret in the cloud SQL web UI.
* Connect to database using your preferred client and run the appropriate user-permissions.sql found in this folder.

### Run the script and deploy
* Add the SITENUM to the site_list.txt file in the scripts directory 
* Be sure to keep a blank line at the end of the file.
* Commit and push


