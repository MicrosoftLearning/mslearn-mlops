# Create an Azure Machine Learning pipeline

The first step to automate machine learning workflows is to create a workflow of the machine learning workloads. A workflow grouping machine learning tasks in Azure Machine Learning is referred to as a pipeline.

## Prerequisites

If you haven't, complete the [set-up](00-set-up.md) before you continue.

## Learning objectives

By completing this challenge, you'll learn how to:

- Convert a notebook into multiple scripts.
- Define an Azure Machine Learning pipeline job in YAML.
- Run an Azure Machine Learning pipeline job with the CLI v2.

## Tasks

In the **experimentation** folder, you'll find a Jupyter notebook which reads a local data file and uses it to train a classification model. 

- Convert the Jupyter notebook to three scripts. 
- Run the scripts as a **pipeline** in Azure Machine Learning.
- Trigger the pipeline using the CLI v2 using the Cloud Shell or a local terminal.
- Use the registered **dataset** in the Azure Machine Learning workspace as input to the pipeline.
- Run the pipeline using an Azure Machine Learning **compute instance** (don't forget to stop it when done).

> **Tip:**
> Run each script as an individual job to test the script and its inputs and outputs.

## Success criteria

To complete this challenge successfully, you should be able to show:

- A successfully completed pipeline in the Azure Machine Learning workspace. 

## Useful resources

- Learning path on how to use the CLI v2 with Azure Machine Learning.
- Documentation on refactoring notebooks into scripts.
- YAML reference for pipelines. 
- Example pipeline. 
- CLI reference for pipeline jobs.
