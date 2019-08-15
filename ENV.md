# Using Anaconda envirnoment

There is support for Anaconda in this project, it is not necessary but allows for easy environment and dependency building


## Install Anaconda

Install Anaconda [here](https://docs.anaconda.com/anaconda/install/). Do not install with pip or easy_install.

Anaconda will append commands to the `.bash_profile`. Be sure to review these commands, comment them out if not needed

The use of Anaconda is intended to:   
*  Ensure packages dependencies are consistent   
*  Ensure versions are managed and easily match that of production (i.e. AWS EMR)   
*  Prevent conflicts in dependencies and versions with other DataHub projects   
*  Persist across operating systems   


## Dependencies

The dependencies for this project are listed in `.conda` in the YAML file 
The current YAML is `.conda/bota_env_1.yml`

To create the environment run:
`conda env create -f .conda/bota_env_1.yml`

To activate the environment run:
`conda activate bota_env_1`

To update the local environment from changes in the repo:
`conda activate bota_env_1`
`conda env update --file .conda/bota_env_1.yml`

Once an environment has been created and `.conda/fix_env.sh` the only necessary 
future action is `conda activate aws_emr_5.24`. 

To leave the Anaconda environment use `conda deactivate`. It is recommended that a new
session be started for work outside the environment as the environment scripts will not
set environment variables back to what they were before activating an environment

To remove the environment `conda remove --name bota_env_1 --all`
