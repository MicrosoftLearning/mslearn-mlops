---
challenge:
    module: 'Deploy a model with GitHub Actions'
    challenge: '7: Deploy and test the model'
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

# Challenge 7: Deploy and test the model

<button class="button" onclick="window.location.href='https://microsoftlearning.github.io/mslearn-mlops/';">Back to overview</button>

## Challenge scenario

To get value from a model, you'll want to deploy it. You can deploy a model to a managed online or batch endpoint.

## Prerequisites

If you haven't, complete the [previous challenge](06-environments.md) before you continue.

## Objectives

By completing this challenge, you'll learn how to:

- Register the model with GitHub Actions.
- Deploy the model to an online endpoint with GitHub Actions.
- Test the deployed model.

## Challenge Duration

- **Estimated Time**: 60 minutes

## Instructions

When a model is trained and logged by using MLflow, you can easily register and deploy the model with Azure Machine Learning. After training the model, you want to deploy the model to a real-time endpoint so that it can be consumed by a web app.

- Create a GitHub Actions workflow which deploys the model trained in the production environment.
- The workflow should register the model, create an endpoint and deploy your model to the endpoint using the CLI (v2).

- Test whether the deployed model returns predictions as expected.

## Success criteria

To complete this challenge successfully, you should be able to show:

- A model registered in the Azure Machine Learning workspace.
- A successfully completed Action in your GitHub repo that deploys the model to an online endpoint.

## Useful resources

- [Learning path covering an introduction of DevOps principles for machine learning.](https://docs.microsoft.com/learn/paths/introduction-machine-learn-operations/)
- [GitHub Actions.](https://docs.github.com/actions/guides)

