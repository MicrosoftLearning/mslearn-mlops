---
challenge:
    module: Use an Azure Machine Learning job for automation
    challenge: '1: Convert a notebook to production code'
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

# Challenge 1: Convert a notebook to production code

<button class="button" onclick="window.location.href='https://microsoftlearning.github.io/mslearn-mlops/';">Back to overview</button>

## Challenge scenario

The first step to automate machine learning workflows is to convert a Jupyter notebook to production-ready code. When you store your code as scripts, it's easier to automate the code execution. You can parameterize scripts to easily reuse the code for retraining.

## Prerequisites

To complete this challenge, you'll need:

- Access to an Azure subscription.
- A GitHub account.
- A GitHub repo with all necessary files. Create a new public repo by navigating to [https://github.com/MicrosoftLearning/mslearn-mlops](https://github.com/MicrosoftLearning/mslearn-mlops) and selecting the **Use this template** button. 

## Objectives

By completing this challenge, you'll learn how to:

- Clean nonessential code.
- Convert your code to Python scripts.
- Use functions in your scripts.
- Use parameters in your scripts.

## Challenge Duration

- **Estimated Time**: 30 minutes

## Instructions

In the **experimentation** folder, you'll find a Jupyter notebook that trains a classification model. The data used by the notebook is in the **experimentation/data** folder and contains a CSV file. 

In the **src/model** folder you'll find a **train.py** script which already has converted most of the code from the notebook. It's up to you to complete it. 

- Go through the notebook to understand what the code does. 
- Convert the code under the **Split data** header and include it in the **train.py** script as a **split_data** function. Remember to:
    - Remove nonessential code.
    - Include the necessary code as a function.

<details>
<summary>Hint</summary>
<br/>
The split_data function is already included in the main function. You only need to add the function itself with the required inputs and outputs underneath the comment <b>TO DO: add function to split data</b>. 
</details>

- Add logging so that every time you run the script, all parameters and metrics are tracked. Use the autologging feature of MLflow to also ensure the necessary model files are stored with the job run to easily deploy the model in the future.

<details>
<summary>Hint</summary>
<br/>
MLflow is an open source library for tracking and managing machine learning models. You can use it to track custom metrics. However, since the current model is trained with the common Scikit-learn library, you can also use autologging. By enabling autologging, using `mlflow.autolog()` all parameters, metrics, and model files will automatically be stored with your job run. Enable autologging in the main function under <b>TO DO: enable autologging</b>.
</details>

## Success criteria

To complete this challenge successfully, you should be able to show:

- A training script which includes a function to split the data and autologging using MLflow.

> **Note:**
> If you've used a compute instance for experimentation, remember to stop the compute instance when you're done. 

## Useful resources

- [Tutorial: Convert ML experiments to production Python code](https://docs.microsoft.com/azure/machine-learning/tutorial-convert-ml-experiment-to-production)
- [Logging MLflow models in Azure Machine Learning](https://docs.microsoft.com/azure/machine-learning/how-to-log-mlflow-models)
- [MLflow documentation](https://www.mlflow.org/docs/latest/python_api/mlflow.html)

<button class="button" onclick="window.location.href='02-aml-job';">Continue with challenge 2</button>