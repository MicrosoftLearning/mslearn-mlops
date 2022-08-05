---
challenge:
    module: Use an Azure Machine Learning job for automation
    challenge: '1: Create an Azure Machine Learning job'
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

# Challenge 1: Create an Azure Machine Learning job

<button class="button" onclick="window.location.href='https://microsoftlearning.github.io/mslearn-mlops/';">Back to overview</button>

## Challenge scenario

To automate machine learning workflows, you can define machine learning tasks in scripts. To execute any workflow consisting of Python scripts, use Azure Machine Learning jobs. Azure Machine Learning jobs store all metadata of a workflow, including input parameters and output metrics. By running scripts as jobs, it's easier to track and manage your machine learning models.

## Prerequisites

If you haven't, complete the [previous challenge](00-script.md) before you continue.

## Objectives

By completing this challenge, you'll learn how to:

- Define an Azure Machine Learning job in YAML.
- Run an Azure Machine Learning job with the CLI v2.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If for example, the instructions ask you to create an Azure Machine Learning workspace, it's up to you to explore and decide how you want to create it. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 30 minutes

## Instructions

In the **src/model** folder, you'll find a Python script which reads CSV files from a folder and uses the data to train a classification model. In the **src** folder, you'll find a YAML file to define a job. There are values missing in the YAML file. It's up to you to complete it. 

- Create an Azure Machine Learning workspace and a compute instance.
- Use the CLI (v2) to create a registered data asset with the following configuration:
    - **Name**: *diabetes-dev-folder*
    - **Path**: The **data** folder in the **experimentation** folder which contains the CSV file to train the model. The path should point to the folder, not to the specific file.

<details>
<summary>Hint</summary>
<br/>
Using the CLI (v2) you can create a data asset by defining the <a href="https://docs.microsoft.com/azure/machine-learning/reference-yaml-data">configuration in a YAML file</a> <b>or</b> by specifying the configuration in the <a href="https://docs.microsoft.com/cli/azure/ml/data?view=azure-cli-latest">CLI command</a>.
</details>
 
- Complete the `job.yml` file to define the Azure Machine Learning job to run the `train.py` script, with the registered data asset as input. 
- Use the CLI (v2) to run the job. 

> **Tip:**
> Whether you're working from the Cloud Shell, compute instance or a local terminal, make sure to update the Azure Machine Learning extension for the CLI to the latest version.

## Success criteria

To complete this challenge successfully, you should be able to show:

- A successfully completed job in the Azure Machine Learning workspace. The job should contain all input parameters and output metrics for the model you trained.

> **Note:**
> If you've used a compute instance for experimentation, remember to stop the compute instance when you're done. 

## Useful resources

- [Learning path on how to use the CLI v2 with Azure Machine Learning.](https://docs.microsoft.com/learn/paths/train-models-azure-machine-learning-cli-v2/)
- [CLI reference for managing Azure Machine Learning workspaces](https://docs.microsoft.com/cli/azure/ml/workspace?view=azure-cli-latest)
- [CLI reference for managing Azure ML compute resources](https://docs.microsoft.com/cli/azure/ml/compute?view=azure-cli-latest)
- [CLI reference for managing Azure ML data assets](https://docs.microsoft.com/cli/azure/ml/data?view=azure-cli-latest)
- [CLI reference for jobs.](https://docs.microsoft.com/cli/azure/ml/job?view=azure-cli-latest)
- [YAML reference for command jobs.](https://docs.microsoft.com/azure/machine-learning/reference-yaml-job-command) 
- [Example job YAML files.](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/basics) 

<button class="button" onclick="window.location.href='02-github-actions';">Continue with challenge 2</button>
