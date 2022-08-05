---
challenge:
    module: Use an Azure Machine Learning job for automation
    challenge: '0: Convert a notebook to production code'
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

# Challenge 0: Convert a notebook to production code

<button class="button" onclick="window.location.href='https://microsoftlearning.github.io/mslearn-mlops/';">Back to overview</button>

## Challenge scenario

The first step to automate machine learning workflows is to convert a Jupyter notebook to production-ready code. When you store your code as scripts, it's easier to automate the code execution. You can parameterize scripts to easily reuse the code for retraining.

## Prerequisites

To complete this challenge, you'll need:

- Access to an Azure subscription.
- A GitHub account.

## Objectives

By completing this challenge, you'll learn how to:

- Clean nonessential code.
- Convert your code to Python scripts.
- Use functions in your scripts.
- Use parameters in your scripts.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If for example, the instructions ask you to create an Azure Machine Learning workspace, it's up to you to explore and decide how you want to create it. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 30 minutes

## Instructions

To work through the challenges, you need **your own public repo** which includes the challenge files. Create a new public repo by navigating to [https://github.com/MicrosoftLearning/mslearn-mlops](https://github.com/MicrosoftLearning/mslearn-mlops) and selecting the **Use this template** button to create your own repo.

In the **experimentation** folder, you'll find a Jupyter notebook that trains a classification model. The data used by the notebook is in the **experimentation/data** folder and contains a CSV file. 

In the **src/model** folder you'll find a `train.py` script which already includes code converted from part of the notebook. It's up to you to complete it. 

- Go through the notebook to understand what the code does. 
- Convert the code under the **Split data** header and include it in the `train.py` script as a `split_data` function. Remember to:
    - Remove nonessential code.
    - Include the necessary code as a function.
    - Include any necessary libraries at the top of the script.

<details>
<summary>Hint</summary>
<br/>
The <code>split_data</code> function is already included in the main function. You only need to add the function itself with the required inputs and outputs underneath the comment <code>TO DO: add function to split data</code>. 
</details>

- Add logging so that every time you run the script, all parameters and metrics are tracked. Use the autologging feature of MLflow to also ensure the necessary model files are stored with the job run to easily deploy the model in the future.

<details>
<summary>Hint</summary>
<br/>
MLflow is an open source library for tracking and managing machine learning models. You can use it to track custom metrics. However, since the current model is trained with the common Scikit-learn library, you can also use autologging. By enabling autologging with <code>mlflow.autolog()</code>, all parameters, metrics, and model files will automatically be stored with your job run. Enable autologging in the main function under <code>TO DO: enable autologging</code>.
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

<button class="button" onclick="window.location.href='01-aml-job';">Continue with challenge 1</button>