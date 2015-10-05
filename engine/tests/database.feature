Feature: saving and loading issue data

  Scenario: save an issue to the database
      Given we have root, config and issue data
       When we save an issue
       Then we receive True

  Scenario: get list of issues from database
      Given we have root directory and configuration
       When we load the list of issues
       Then we receive a list of dictionaries

  Scenario: get an issue from database
      Given we have root directory and configuration
       When we load an issue
       Then we receive a dictionary

  Scenario: delete an issue from database
      Given we have root directory and configuration
       When we delete an issue
       Then we receive True if issue was deleted

