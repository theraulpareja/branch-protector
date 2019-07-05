# branch-protector

Automate master branch protection for brand new repositories in your GitHub organization.

## Configuration

## Basic configuration

There are 2 main config files:

* Edit the `branch-protector/app-branch-protector/.flaskenv` To control flask app ports and environments

```
# Flask app vars
FLASK_APP=app-branch-protector.py
# Do not use development environment in prodution!, change FLASK_ENV to production
FLASK_ENV=development
# FLASK_ENV=prodution
FLASK_RUN_PORT=9090
```

* Create the `branch-protector/conf/branch-protector-config.yaml` editing by copying/renameing branch-protector/conf/branch-protector-config.yaml_example as an example, mind that you will need a `Personal access tokens`, you can create yours in https://github.com/settings/tokens
  
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

## How to use it

There are serveral ways to run branch-protector

* flask standalone
* docker
* Cloud providers

**IMPORTANT: In all cases** you will need to:
* Create a webhook in your GitHiub organization, you will need admin or owner permitions and go to https://github.com/organizations/<ORGANIZATION>/settings/hooks
* You will need to expose the flask app with a public IP and a exposed port and configure properly the file branch-protector/app-branch-protector/.flaskenv to expose the `Payload URL`

### flask standalone 

Clone the repo and create a python3 virtualenv to use branch-protector within

```
git clone https://github.com/theraulpareja/branch-protector.git
cd cd branch-protector
python3 -m venv env
source  env/bin/activate
pip install -r requirements.txt
```

Check configuration section to setup `branch-protector/app-branch-protector/.flaskenv` and `branch-protector/conf/branch-protector-config.yaml` and make sure github.com can reach your `Payload URL`

Run the flask application on your server
```
cd app-branch-protector
flask run
```

Go to section "Setup webhook in your GitHub organization" to setup GitHub side

## Setup webhook in your GitHub organization 

* Create a webhook in your GitHiub organization, you will need admin or owner permitions (use your organization to complete the url) https://github.com/organizations/<ORGANIZATION>/settings/hooks .
* Click radio button `Let me select individual events.` and select **ONLY** `Repositories` check box.
* Select `Acitve` check box an push `Add Webhook`


### Docker 

TODO

### Google Cloud Run

TODO

## How to test

Please check the tests/how-to-test.md file for information in regards testing
