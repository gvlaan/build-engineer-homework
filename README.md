# Build Engineer Homework

Imagine a case where developers would like to have info on potential causes of failures without having to navigate to read github action logs. Your task is to write a [custom GitHub Action](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions) capable of parsing Unity Editor log files for errors and warnings. The parsed results should be presented in [GitHub Workflow Summary Annotations](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#example-creating-an-annotation-for-an-error) and errors set as action outputs.


## Deliverables

Use this template repository to implement the following:

1. Create a custom github action
   1. Accepts a log file path as input
   2. Parse and log errors and warnings as annotations
   3. Errors should be set to action output
2. Reference this action from ./github/workflows/parse-log.yml

## Log files
Inside `logs` directory you will find standard editor log when building for macos standalone.
