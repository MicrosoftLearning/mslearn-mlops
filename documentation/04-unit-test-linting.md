---
challenge:
    module: 'Work with linting and unit testing in GitHub Actions'
    challenge: '4: Work with linting and unit testing'
---

<style>
.button  {
  border: none;
  color: white;
  padding: 12px 28px;
  background-color: #008CBA;
  float: right;
}
</style>

# Challenge 4: Work with linting and unit testing

<button class="button" onclick="window.location.href='https://microsoftlearning.github.io/mslearn-mlops/';">Back to overview</button>

## Challenge scenario

Code quality can be assessed in two ways: linting and unit testing. Use linting to check for any stylistic errors and unit testing to verify your functions.

## Prerequisites

If you haven't, complete the [previous challenge](03-trigger-workflow.md) before you continue.

You'll complete the workflow created in the previous challenge.

## Objectives

By completing this challenge, you'll learn how to:

- Run linters and unit tests with GitHub Actions.
- Troubleshoot errors to improve your code.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If for example, the instructions ask you to create an Azure Machine Learning workspace, it's up to you to explore and decide how you want to create it. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 45 minutes

## Instructions

In the **tests** folder, you'll find files that will perform linting and unit testing on your code. The `flake8` lints your code to check for stylistic errors. The `test_train.py` performs unit tests on your code to check whether the functions behave as expected.

- Go to the **Actions** tab in your GitHub repo and trigger the **Code checks** workflow manually. Inspect the output and fix your code where necessary.

<details>
<summary>Hint</summary>
<br/>
Whenever the linter finds an error, the GitHub Actions step will fail with exit code 1. Inspect the output of the workflow to see the specific error codes for the linter. Next to the error code, the output will also list the source file with the line number and column number to help you find the cause of the error.
</details>

- Add linting and unit tests jobs to the workflow you created in the previous challenge. The workflow should be triggered by the creation of a new pull request. The workflow should run the Flake8 linter *and* run the Pytest unit tests.

<details>
<summary>Hint</summary>
<br/>
To include unit testing in your workflow, install Pytest (using the <code>requirements.txt</code>), and run the tests with <code>pytest tests/</code>. By default, Pytest uses test files that are prefixed with <code>test</code>.
</details>

- Create (or edit) a **branch protection rule** to require the two code checks to be successful before merging a pull request to the **main** branch.

<details>
<summary>Hint</summary>
<br/>
To configure checks to be required to pass before merging, you can enable <b>status checks</b> in a branch protection rule. To find the checks, your jobs need to have a name. To ensure the checks run whenever a pull request is created, your checks should be part of a GitHub Actions workflow triggered by a <code>pull_request</code> event.
</details>

To trigger the workflow, do the following:

- Make a change and push it. For example, change the hyperparameter value. 
- Create a pull request, showing the integrated code checks.

## Success criteria

To complete this challenge successfully, you should be able to show:

- Both the **Linting** and **Unit tests** checks are completed successfully without any errors. The successful checks should be shown in a newly created pull request.

## Useful resources

- [Flake8 documentation](https://flake8.pycqa.org/latest/user/index.html), including [error codes and their descriptions.](https://flake8.pycqa.org/en/latest/user/error-codes.html)
- [A beginner's guide to Python testing.](https://miguelgfierro.com/blog/2018/a-beginners-guide-to-python-testing)
- Learn more about [test infrastructure using Azure ML and how to create tests.](https://github.com/microsoft/recommenders/tree/main/tests)
- Learn more about [testing with Pytest.](https://docs.microsoft.com/learn/modules/test-python-with-pytest/)

In this challenge, all testing is executed with GitHub Actions. Optionally, you can learn how to [verify your code locally with Visual Studio Code](https://docs.microsoft.com/learn/modules/source-control-for-machine-learning-projects/5-verify-your-code-locally). Running linters and unit tests locally is not required for this challenge.

<button class="button" onclick="window.location.href='05-environments';">Continue with challenge 5</button>