# Trigger the Azure Machine Learning pipeline with GitHub Actions

The benefit of using the CLI v2 to run an Azure Machine Learning pipeline, is that you can submit the pipeline job from anywhere. To trigger the pipeline to run, you can use GitHub Actions.

## Prerequisites

If you haven't, complete the [set-up](00-set-up.md) before you continue.

You'll also need the Azure Machine Learning pipeline created in Challenge 1. 

## Learning objectives

By completing this challenge, you'll learn how to:

- Run the Azure Machine Learning pipeline with GitHub Actions.
- Trigger the pipeline with a change to the repo.

## Tasks

In the **.github/workflows** folder, you'll find two GitHub Actions that were used in set-up to create and manage the Azure Machine Learning workspace.

- Create a new workflow in the **.github/workflows** that triggers the Azure Machine Learning pipeline.
- You should be able to trigger the workflow manually.
- The Azure Machine Learning pipeline should use a **compute cluster**. 

> **Tip:**
> GitHub is authenticated to use your Azure Machine Learning workspace with a service principal. The service principal is only allowed to submit jobs that use a compute cluster, not a compute instance.

## Success criteria

To complete this challenge successfully, you should be able to show:

- A successfully completed Action in your GitHub repo, triggered manually in GitHub.
- A step in the Action should have submitted a pipeline job to the Azure Machine Learning workspace.
- A successfully completed Azure Machine Learning pipeline that used a compute cluster.

## Useful resources

- [Learning path covering an introduction of DevOps principles for machine learning.](https://docs.microsoft.com/learn/paths/introduction-machine-learn-operations/)
- [GitHub Actions.](https://docs.github.com/en/actions/guides)
