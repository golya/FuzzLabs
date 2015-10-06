from behave import *
import os
import sys
import time
import inspect

ROOT_DIR = os.path.dirname(
                os.path.abspath(
                    inspect.getfile(inspect.currentframe()
                )))

sys.path.append(ROOT_DIR + "/../../classes")
from ConfigurationHandler import ConfigurationHandler
from DatabaseHandler import DatabaseHandler

@given('we have root and config and no issues')
def step_impl(context):
    assert os.path.isfile(ROOT_DIR + "/../../etc/engine.config")
    context.root        = ROOT_DIR + "/../../"
    config_file         = ROOT_DIR + "/../../etc/engine.config"
    context.config_data = ConfigurationHandler(config_file).get()

@given('we have root, config and issue data')
def step_impl(context):
    assert os.path.isfile(ROOT_DIR + "/../../etc/engine.config")
    context.root        = ROOT_DIR + "/../../"
    config_file         = ROOT_DIR + "/../../etc/engine.config"
    context.config_data = ConfigurationHandler(config_file).get()
    context.issue_data  = {
                          "job_id": "23d6609d6b31868fa15b0597255c5527",
                          "time": time.time(),
                          "name": "FUZZ_NODE_NAME",
                          "mutant_index": 1,
                          "process_status": {},
                          "request": "TEST DATA"
                          }

@when('we save an issue')
def step_impl(context):
    context.database   = DatabaseHandler(context.config_data, context.root)
    context.return_val = context.database.saveIssue(context.issue_data)

@then('we receive True')
def step_impl(context):
    assert context.return_val

@given('we have root directory and configuration')
def step_impl(context):
    assert os.path.isfile(ROOT_DIR + "/../../etc/engine.config")
    context.root        = ROOT_DIR + "/../../"
    config_file         = ROOT_DIR + "/../../etc/engine.config"
    context.config_data = ConfigurationHandler(config_file).get()

@when('we load the list of issues')
def step_impl(context):
    context.database   = DatabaseHandler(context.config_data, context.root)
    context.return_val = context.database.loadIssues()

@then('we receive a list without issues')
def step_impl(context):
    assert type(context.return_val) == list
    assert context.return_val == []

@then('we receive a list of dictionaries')
def step_impl(context):
    assert type(context.return_val) == list
    for issue in context.return_val:
        assert type(issue) == dict

@when('we load an issue')
def step_impl(context):
    context.database   = DatabaseHandler(context.config_data, context.root)
    context.return_val = context.database.loadIssue(1)

@then('we receive an empty dictionary without issue data')
def step_impl(context):
    assert type(context.return_val) == dict
    assert context.return_val == {}

@then('we receive a dictionary with issue data')
def step_impl(context):
    assert type(context.return_val) == dict
    assert context.return_val.get('job_id')
    assert context.return_val.get('payload')

@when('we delete an issue')
def step_impl(context):
    context.database   = DatabaseHandler(context.config_data, context.root)
    context.return_val = context.database.deleteIssue(1)

@then('we receive False as the issue was not found')
def step_impl(context):
    assert context.return_val == False

@then('we receive True if issue was deleted')
def step_impl(context):
    assert context.return_val

