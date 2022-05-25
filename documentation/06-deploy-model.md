# Deploy and test the model

To get value from a model, you'll want to deploy it. You can deploy a model to a managed online or batch endpoint.

## Prerequisites

If you haven't, complete the [set-up](00-set-up.md) before you continue.

You'll also need the GitHub Action that triggers the Azure Machine Learning pipeline created in Challenge 3. 

## Learning objectives

By completing this challenge, you'll learn how to:

- Set up a development and production environment.
- Add environments to GitHub Action.
- Add a required reviewer to the staging job environment.

## Tasks

When you work with environments, you can isolate projects and tasks within a project. Though it's a best practice to associate a separate Azure Machine Learning workspace to each environment, you can use one workspace for both the development and production environment for this challenge. 

- Within your GitHub repo, create a development and production environment. 
- Create one GitHub Action that trains the model in the development environment.
- Create a second GitHub Action that creates and deploys the model in the production environment.
- Add a approval check for the production environment. 

## Success criteria

To complete this challenge successfully, you should be able to show:

- A successfully completed Action in your GitHub repo that trains the model.
- A GitHub Action that creates the model in the production environment. Show that the workflow requires an approval before running.
- A model registered in the Azure Machine Learning workspace.

## Useful resources

- [Learning path covering an introduction of DevOps principles for machine learning.](https://docs.microsoft.com/learn/paths/introduction-machine-learn-operations/)
- [GitHub Actions.](https://docs.github.com/actions/guides)
- [Using environments for deployment in GitHub.](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)
