from flask import request
from flask import make_response
from flask import current_app
from flask import logging
from flask import render_template
from app import app
import os
import requests
import yaml
import pdb
import json
import time


class ReadConfigYaml:
        """Parse yaml config file to get necessary data to run branch-protector"""
        def __init__(self, yaml_file_name):
            if not os.path.exists(yaml_file_name):
                app.logger.error('Missing main configuration file {}'.format(yaml_file_name))
            try:
                with open(yaml_file_name) as yaml_file:
                    app.logger.info('loading config file {}'.format(yaml_file_name))
                    params = yaml.load(yaml_file)
            except Exception as msg:
                app.logger.error('Can not load the YAML file {}, please review syntax with any online yaml pareser: {}'.format(yaml_file_name, msg))
            try:
                self.branchname = params['APP_CONF']['BRANCH']
                self.organame = params['APP_CONF']['ORGANIZATION']
                self.token = params['APP_CONF']['TOKEN']
            except Exception as msg:
                app.logger.error('{}: Missing  BRANCH, ORGANIZATION or TOKEN in {}'.format(msg, yaml_file_name))

            try:
                self.required_status_checks = params['APP_CONF']['REQUIRED_STATUS_CHECKS']
                self.enforce_admins = params['APP_CONF']['ENFORCE_ADMINS']
                self.required_pull_request_reviews = params['APP_CONF']['REQUIRED_PULL_REQUEST_REVIEWS']
                self.restrictions = params['APP_CONF']['RESTRICTIONS']
            except Exception as msg:
                app.logger.error('{}: Minimal config for REQUIRED_STATUS_CHECKS, REQUIRED_STATUS_CHECKS, \
                     REQUIRED_PULL_REQUEST_REVIEWS and RESTRICTIONS is needed'.format(msg))
            app.logger.info('Config params loaded')


def get_config():
    """ Get configuration form yaml config """
    config_dir = '../conf/'
    config_file_name = 'branch-protector-config.yaml'
    full_path_config = config_dir + config_file_name
    configs = ReadConfigYaml(full_path_config)
    return configs


def non_repo_creation_event():
    """ HTTP 200 response for non creation events """ 
    message = '{"message": "Not a repository creation event"}'
    response = make_response(message, 200)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    app.logger.warning(message)
    return response


def json_not_found():
    """ HTTP 400 for non json payloads """
    message = '{"message": "JSON payload not found"}'
    response = make_response(message, 400)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    app.logger.warning(message)
    return response


def update_branch_protection(token, owner, repo, branch):
    """ Protecting a branch requires admin or owner permissions to the repository.
    https://developer.github.com/v3/repos/branches/#update-branch-protection
    """
    headers = {'Authorization': 'bearer {}'.format(token), 'Accept':'application/vnd.github.luke-cage-preview+json'}
    url = 'https://api.github.com/repos/{}/{}/branches/{}/protection'.format(owner, repo, branch)
    try:
        with open('../payloads/branch-protector-payload.json') as json_file:
            json_data = json.load(json_file)
            json_data_clean = json.dumps(json_data, indent=4, sort_keys=True)
            time.sleep(8)
            api_call = requests.put(url, data=json_data_clean, headers=headers)
    except Exception as msg:
        message = '{{"message": "Could not run api call {}: {}"}}'.format(url, msg)
        response = make_response(message, 500)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.error(message)
        return response
    if (api_call.status_code == 200):
        message = '{{"message": "Protections applyed to branch {} on repo {}"}}'.format(branch, repo)
        response = make_response(message, 200)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.info(message)
        return response
    else:
        message = '{{"message": "update_branch_protection Api call returned {} {} and failed branch protectcion {} on repo {}"}}'.format(api_call.status_code, api_call.text, branch, repo)
        response = make_response(message, 500)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.error(message)
        return response


def enable_repo_issues(token, owner, repo):
    """ Enable isusues in a repository with Edit reposiotry API
    https://developer.github.com/v3/repos/#edit
    """
    headers = {'Authorization': 'bearer {}'.format(token)}
    url = 'https://api.github.com/repos/{}/{}'.format(owner, repo)
    payload = '{{"name":"{}","has_issues":"true"}}'.format(repo)
    # json_data = json.loads(payload)
    try:
        api_call = requests.patch(url, json=payload, headers=headers)
    except Exception as msg:
        message = 'Could not run api call {}: {}'.format(url, msg)
        response = make_response(message, 500)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.error(message)
        return response
    if (api_call.status_code == 200):
        message = 'Issue enabled in repository {}'.format(repo)
        response = make_response(message, 200)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.info(message)
        return response
    else:
        message = 'edit repo Api call returned {} {} and failed on repo {}'.format(api_call.status_code, api_call.text, repo)
        response = make_response(message, 500)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.error(message)
        return response


def create_an_issue(token, owner, repo):
    """ Create an isusue in a repository.
    https://developer.github.com/v3/issues/#create-an-issue
    """
    headers = {'Authorization': 'bearer {}'.format(token), 'Accept':'application/vnd.github.symmetra-preview+json'}
    url = 'https://api.github.com/repos/{}/{}/issues'.format(owner, repo)
    try:
        with open('../payloads/create-issue-payload.json') as json_file:
            json_data = json.load(json_file)
            json_data_clean = json.dumps(json_data, indent=4, sort_keys=True)
            api_call = requests.post(url, data=json_data_clean, headers=headers)
    except Exception as msg:
        message = '{{"message": "Could not run api call {}: {}"}}'.format(url, msg)
        response = make_response(message, 500)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.error(message)
        return response
    if (api_call.status_code == 201):
        message = '{{"message": "Issue created in repository {}"}}'.format(repo)
        response = make_response(message, 200)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.info(message)
        return response
    else:
        message = '{{"message": "create_an_issue Api call returned {} {} and failed on repo {}"}}'.format(api_call.status_code, api_call.text, repo)
        response = make_response(message, 500)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        app.logger.error(message)
        return response

@app.route('/')
@app.route('/index')
def index():
    return "Wellcome to branch-protector see documentation here https://github.com/theraulpareja/branch-protector"


@app.route('/branch-protector', methods=['POST'])
def branch_protector():
    if (request.is_json):
        app.logger.debug('JSON post detected')
    content = request.get_json()
    if content is None:
        app.logger.debug('Value of content is {}'.format(type(content)))
        return json_not_found()
    else:
        configs = get_config()
        app.logger.info('JSON payload loaded')
        if (content['action'] == 'created'):
            reponame = content['repository']['name']
            creation = content['repository']['created_at']
            # Protect repo branch
            rendered_update_branch_protection_json = render_template('update-branch-protection-template.json', configs=configs)
            with open("../payloads/branch-protector-payload.json", "w") as f:
                f.write(rendered_update_branch_protection_json)
            app.logger.info('Json payload generated for branch protection in ../payloads/branch-protector-payload.json')
            update_branch_protection(configs.token, configs.organame, reponame, configs.branchname)
            # Enable issue in repo
            """
            rendered_enable_issue_json = render_template('enable-issue-template.json', configs=configs, reponame=reponame)
            with open("../payloads/enable-issue-payload.json", "w") as f:
                f.write(rendered_enable_issue_json)
            app.logger.info('Json payload generated to enable issue in repo in ./payloads/enable-issue-payload.json')
            enable_repo_issues(configs.token, configs.organame, reponame)
            """
            # Create issue in repo
            rendered_create_issue_json = render_template('body-issue-template.json', configs=configs)
            with open("../payloads/create-issue-payload.json", "w") as f:
                f.write(rendered_create_issue_json)
            app.logger.info('Json payload generated for issue creation in ../payloads/create-issue-payload.json')
            create_an_issue(configs.token, configs.organame, reponame)
            return '{"mesage": "thank you for using branch-protector"}'
        else:
            return non_repo_creation_event()
