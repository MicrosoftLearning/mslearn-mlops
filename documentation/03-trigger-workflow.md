# Trigger GitHub Actions with trunk-based development

Triggering a workflow by pushing directly to the repo is **not** considered a best practice. Preferably, you'll want to review any changes before you build them with GitHub Actions.

## Prerequisites

If you haven't, complete the [set-up](00-set-up.md) before you continue.

You'll also need the GitHub Action that triggers the Azure Machine Learning pipeline created in Challenge 2. 

## Learning objectives

By completing this challenge, you'll learn how to:

- Work with trunk-based development.
- Trigger the Azure Machine Learning pipeline with a pull request event.

## Tasks

Use trunk-based development to better govern changes made to the repo and the triggering of GitHub Actions.

- Create a branch in the repo.
- Make a change and push it. For example, change the hyperparameter value. 
- Create a pull request. 
- Trigger the GitHub Action that submits the Azure Machine Learning pipeline by merging the pull request.

## Success criteria

To complete this challenge successfully, you should be able to show:

- A successfully completed Action in your GitHub repo. 
- An event in the GitHub Action that ensures the workflow is triggered by a merged pull request with the tag “Release”.

## Useful resources

- [Learning path covering an introduction of DevOps principles for machine learning.](https://docs.microsoft.com/learn/paths/introduction-machine-learn-operations/)
- [GitHub Actions.](https://docs.github.com/actions/guides)
- [Triggering a GitHub Actions workflow.](https://docs.github.com/actions/using-workflows/triggering-a-workflow)