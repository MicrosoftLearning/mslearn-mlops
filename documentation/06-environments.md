---
challenge:
    module: 'Work with environments in GitHub Actions'
    challenge: '6: Work with environments'
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

# Challenge 6: Work with environments

<button class="button" onclick="window.location.href='https://microsoftlearning.github.io/mslearn-mlops/';">Back to overview</button>

## Challenge scenario

There are many advantages to using environments in machine learning projects. When you have separate environments for development, staging, and production, you can more easily control access to resources. 

Use environments to isolate workloads and control the deployment of the model.

## Prerequisites

If you haven't, complete the [previous challenge](05-unit-test-linting.md) before you continue.

**Your repo should be set to public**. If you're using a private repo without GitHub Enterprise Cloud, you'll not be able to create environments. [Change the visibility of your repo to public](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility) if your repo is set to private.

You'll re-use the workflow you created for [challenge 3: trigger the Azure Machine Learning job with GitHub Actions](03-github-actions.md). 

## Objectives

By completing this challenge, you'll learn how to:

- Set up a development and production environment.
- Add a required reviewer.
- Add environments to a GitHub Actions workflow.

## Challenge Duration

- **Estimated Time**: 60 minutes

## Instructions

> **Note:**
> Though it's a best practice to associate a separate Azure Machine Learning workspace to each separate environment, you can use one workspace for both the development and production environment for this challenge (to avoid extra costs). 

- Within your GitHub repo, create a development and production environment.
- For each environment, add the **AZURE_CREDENTIALS** secret that contains the service principal output. 

> **Note:**
> If you don't have the service principal output anymore from [challenge 3](03-github-actions.md), go back to the Azure portal and create it again. You can only get the necessary output at the time of creation.

- Remove the global repo **AZURE_CREDENTIALS** secret, so that each environment can only use its own secret.
- Add an approval check for the production environment.
- Create a new data asset in the workspace with the following configuration:
  - **Name**: *diabetes-prod-folder*
  - **Path**: The **data** folder in the **production** folder which contains a larger CSV file to train the model. The path should point to the folder, not to the specific file.  
- Create one GitHub Actions workflow with two jobs:
  - The **experiment** job that trains the model using the registered dataset in the **development environment**. 
  - The **production** job that trains the model in the **production environment**, using the production data (the *diabetes-prod-folder* data asset as input).
- Add a condition that the **production** job is only allowed to run when the **experiment** job ran *successfully*. Success means that the Azure Machine Learning job ran successfully too.

<details>
<summary>Hint</summary>
<br/>
You'll need to do two things to ensure the production job only runs when the experiment job is successful: add <code>needs</code> to the workflow and add <code>--stream</code> to the CLI command to trigger the Azure Machine Learning job. 
</details>

## Success criteria

To complete this challenge successfully, you should be able to show:

- Show the environment secrets in the settings.
- A successfully completed Actions workflow that contains two jobs. The production job needs the experimentation job to be successful to run.
- Show that the workflow required an approval before running the production workload.
- Show two successful Azure Machine Learning jobs, one trained with the *diabetes-dev-folder* as input and the other with the *diabetes-prod-folder* as input.

## Useful resources

- Learn more about [continuous deployment for machine learning.](https://docs.microsoft.com/learn/modules/continuous-deployment-for-machine-learning/)
- [Workflow syntax for GitHub Actions.](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Using environments for deployment in GitHub.](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [How to create a secret in a GitHub repo.](https://docs.github.com/actions/security-guides/encrypted-secrets)
- [CLI reference for jobs.](https://docs.microsoft.com/cli/azure/ml/job?view=azure-cli-latest)

<button class="button" onclick="window.location.href='07-deploy-model';">Continue with challenge 7</button>