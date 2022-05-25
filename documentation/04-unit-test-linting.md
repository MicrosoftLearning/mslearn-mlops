# Work with linting and unit testing

Code quality can be assessed in two ways: linting and unit testing. Use linting to check for any stylistic errors and unit testing to verify your functions.

## Prerequisites

If you haven't, complete the [set-up](00-set-up.md) before you continue.

You'll also need the GitHub Action that triggers the Azure Machine Learning pipeline created in Challenge 3. 

## Learning objectives

By completing this challenge, you'll learn how to:

- Run linters and unit tests with GitHub Actions.
- Troubleshoot errors to improve your code.

## Tasks

In the **tests** folder, you'll find files that will perform linting and unit testing on your code. The `flake8` lints your code to check for stylistic errors. The `test_train.py` performs unit tests on your code to check whether the functions work.

- Go to the **Actions** tab in your GitHub repo and trigger the **Linting** workflow manually. Inspect the output and fix your code where necessary.
- Go to the **Actions** tab in your GitHub repo and trigger the **Unit testing** workflow manually. Inspect the output and fix your code where necessary.

## Success criteria

To complete this challenge successfully, you should be able to show:

- Both the **Linting** and **Unit testing** workflows are completed successfully without any errors.

## Useful resources

- [Learning path covering an introduction of DevOps principles for machine learning.](https://docs.microsoft.com/learn/paths/introduction-machine-learn-operations/)