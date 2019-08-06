# branch-protector

**branch-protector** automates branch protection ( e.g master) for any brand new repositories under your GitHub organization and creates an issue with a mention to you (or any owner) with information of your branch protection rules set.

## Set up and configurations

### Requirements

**IMPORTANT:**  You will need a `Personal access tokens` first, you can create yours in https://github.com/settings/tokens, more information about personal access tokens [here](https://help.github.com/en/articles/)


### Configuration files

There are 2 main config files that need to be edited:

* `branch-protector/app-branch-protector/.flaskenv`
* `branch-protector/conf/branch-protector-config.yaml`

### branch-protector/app-branch-protector/.flaskenv

Edit the `branch-protector/app-branch-protector/.flaskenv` to set up the flask app port and environments (please mind to set FLASK_ENV to production once you are ready to go live).

```
# Flask app vars
FLASK_APP=app-branch-protector.py
# Do not use development environment in production!, change FLASK_ENV to production
FLASK_ENV=development
# FLASK_ENV=prodution
FLASK_RUN_PORT=8080
```

### branch-protector/conf/branch-protector-config.yaml

* **Create** the `branch-protector/conf/branch-protector-config.yaml` by copying the example yaml template `branch-protector/conf/branch-protector-config.yaml_example`) 
 ```
cd branch-protector/conf
cp branch-protector-config.yaml_example branch-protector-config.yaml
```

* Edit the recently created file `branch-protector/conf/branch-protector-config.yaml` with the right data for your organization and credentials. Please read carefully the comments, this is the https://developer.github.com/v3/repos/branches/#update-branch-protection API abstraction adapted to a yaml configuration file.

```
APP_CONF:
 # The branch you want to protect
 BRANCH: master
 # Organization name (required)
 ORGANIZATION: conejillo-de-indias
 # Add personal access token of organization owner or admin (required) you can create one in https://github.com/settings/tokens
 TOKEN: 'your-token'
 # Required. Require status checks to pass before merging. Set to null to disable.
 REQUIRED_STATUS_CHECKS:
 # Required if REQUIRED_STATUS_CHECKS is not left null. Require branches to be up to date before merging True or False.
   - strict: True
 # Required if REQUIRED_STATUS_CHECKS is not left null. The list of status checks to require in order to merge into this branch
     contexts:
       - continuous-integration/travis-ci
 # Required. Enforce all configured restrictions for administrators. Set to True to enforce required status checks for repository administrators. Set to null to disable.
 ENFORCE_ADMINS: True
 # Required. Require at least one approving review on a pull request, before merging. Set to null to disable.
 REQUIRED_PULL_REQUEST_REVIEWS:
 # Specify which users and teams can dismiss pull request reviews. Pass an empty dismissal_restrictions object to disable. User and team dismissal_restrictions are only available for organization-owned repositories. Omit this parameter for personal repositories.
   - dismissal_restrictions:
     users:
       - chucknorris
     teams:
       - A-Team
 # Set to true if you want to automatically dismiss approving reviews when someone pushes a new commit.
   - dismiss_stale_reviews: True
 # Blocks merging pull requests until code owners review them.
   - require_code_owner_reviews: True
 # Specify the number of reviewers required to approve pull requests. Use a number between 1 and 6.
   - required_approving_review_count: 1
 # Required. Restrict who can push to this branch. Team and user restrictions are only available for organization-owned repositories. Set to null to disable.
 RESTRICTIONS:
   users:
     - brucelee
   teams:
     - fcbarcelona
```

## How to run it

There are several ways to run branch-protector, some of them are:

* flask standalone application
* docker

### First set up the webhook in your GitHub organization

**IMPORTANT: In all cases** you will need to:
* Create a webhook in your GitHub organization, you will need an admin or owner permissions https://github.com/organizations/<ORGANIZATION>/settings/hooks
* Click radio button `Let me select individual events.` and select **ONLY** `Repositories` check box.
* **IMPORTANT:** Select Content type `application/json`
* Select `Active` check box and push `Add Webhook`
* You will need to **expose the flask app with a public IP and a exposed port** check config file branch-protector/app-branch-protector/.flaskenv to match the exposed port and IP or DNS for the `Payload URL`.


### branch-protector as a flask standalone app

* Clone the repo and create a python3 virtualenv to use branch-protector within

```
git clone https://github.com/theraulpareja/branch-protector.git
cd branch-protector
python3 -m venv env
source  env/bin/activate
pip install -r requirements.txt
```

* Review section **Basic webservice configuration** to setup `branch-protector/app-branch-protector/.flaskenv` and `branch-protector/conf/branch-protector-config.yaml` and make sure github.com can reach your `Payload URL`

* Run the flask application on your server
```
cd app-branch-protector
flask run  --host=0.0.0.0
```

* Go to "Setup webhook in your GitHub organization" section to setup the GitHub webhook that calls branch-protector URL.

* Please check the docs in `tests/how-to-test.md` file for information in regards testing.



### Dockerize branch-protector

* Clone the repo with `git clone https://github.com/theraulpareja/branch-protector.git'

```
git clone https://github.com/theraulpareja/branch-protector.git
```

* Edit config files `branch-protector/app-branch-protector/.flaskenv` and  `branch-protector/conf/branch-protector-config.yaml`  described in section **Basic web service configuration**

* Build the image once configuration is set up using the `Dockerfile`, and upload it to your private docker registry.
**IMPORTANT!:** Do not upload the image to the public docker hub as it contains sensible data within `conf/`

```
cd branch-protector
docker build -f Docker/Dockerfile . -t theraulpareja/branch-protector:v0
```

* Run the branch-protector web service container, mind to **select a port strategy** to expose your node port externally wether with mapped or ephemeral ports (check documentation [here] (https://docs.docker.com/engine/reference/run/#expose-incoming-ports)).

```
# To see live requests processing:
docker run  -p 8080:8080 --rm --name branch-protector theraulpareja/branch-protector:v0

# To run in detached mode (recommended)
docker run -d -p 8080:8080 --rm --name branch-protector theraulpareja/branch-protector:v0
```

* To create a container with interactive shell for debugging

```
docker run -it -p 8080 --rm theraulpareja/branch-protector:v0 sh
# once in run flask
flask run  --host=0.0.0.0
```

## Expose branch-protector 'Payload url`  to GitHub

Please consider to:

* (Recommended) Use a Kubernetes ingress to expose the `Payload url` running the docker container with branch-protector  webservice.
* Run the flask app in [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
* Run the docker container in [https://cloud.google.com/run/](https://cloud.google.com/run/)

## How to test and debug

Please check the `tests/how-to-test.md` file for information in regards to testing the application

