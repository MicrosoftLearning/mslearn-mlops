---
lab:
    title: 'Deploy and monitor a model in Azure Machine Learning'
    description: 'Use GitHub Actions pull requests, environments, and comment triggers to train models in dev and prod, deploy to a managed online endpoint, and configure Azure Machine Learning model monitoring.'
    level: 300
    duration: 60 minutes
---

# Deploy and monitor a model in Azure Machine Learning

Training a model is only the beginning of the machine learning lifecycle. To generate value, you need a repeatable way to move models from development into production, monitor how they behave, and respond quickly when data or performance changes.

In this exercise, you:

- Use GitHub Actions **environments** to run training in a development context.
- Register models in a **shared Azure Machine Learning registry**.
- Deploy the registry model to a **production** online endpoint.
- Monitor drift, retrain in dev, and promote a new model version to production.
- Optionally roll back to a previous deployment and archive a bad model version.

## Before you start

You need:

- An [Azure subscription](https://azure.microsoft.com/free?azure-portal=true) in which you have administrative-level access.
- A [GitHub](https://github.com/) account with permission to create repositories and configure GitHub Actions.

## Provision the workspace and data assets

First, you create or reuse an Azure Machine Learning workspace and the data assets you need for development and production. You build on the same pattern that you used in the previous lab: provision the workspace and data from the original lab repo, and then connect a separate GitHub repository for automation.

1. In a browser, open the Azure portal at `https://portal.azure.com/` and sign in with your Microsoft account.
1. Select the **[>_]** (**Cloud Shell**) button at the top of the page to open Cloud Shell, and choose **Bash** if prompted.
1. Make sure the correct subscription is selected and that **No storage account required** is selected. Then select **Apply**.
1. In the terminal, clone this repo and navigate to the infrastructure folder:

	```azurecli
	rm -r mslearn-mlops -f
	git clone https://github.com/MicrosoftLearning/mslearn-mlops.git mslearn-mlops
	cd mslearn-mlops/infra
	```

1. Before you run the setup script, update it so that it also creates separate dev and prod folder data assets:
	1. In Cloud Shell, open the `setup.sh` file in the editor (for example, run `code setup.sh`).
	1. In the file, locate the **Create data assets** section:

		```bash
		# Create data assets
		echo "Create training data asset:"
		az ml data create --type mltable --name "diabetes-training" --path ../data/diabetes-data
		az ml data create --type uri_file --name "diabetes-data" --path ../data/diabetes-data/diabetes.csv
		```

	1. Directly after these commands, add the following lines to create folder data assets that point to the dev and prod data folders in this repo:

		```bash
		az ml data create --type uri_folder --name "diabetes-dev-folder" --path ../experimentation/data
		az ml data create --type uri_folder --name "diabetes-prod-folder" --path ../production/data
		```

	1. Save the file and return to the terminal pane.

1. Run the setup script:

	```azurecli
	./setup.sh
	```

	> Ignore any messages that say that extensions couldn't be installed.

1. Wait for the script to finish. It creates a resource group, an Azure Machine Learning workspace, compute resources, and the data assets you need for this lab.
1. In the Azure portal, go to **Resource groups** and open the `rg-ai300-...` resource group that was created.
1. Select the Azure Machine Learning workspace (for example, `mlw-ai300-...`) and then select **Launch studio** to open Azure Machine Learning studio.
1. In the studio, select **Data** and verify that you have the following data assets:
	- An **MLTable** or file-based asset named `diabetes-training` for the core training data.
	- A **File (uri_folder)** data asset named `diabetes-dev-folder` that points to the `experimentation/data` folder in your workspace files.
	- A **File (uri_folder)** data asset named `diabetes-prod-folder` that points to the `production/data` folder.

	If any of these assets are missing, create them manually with the types and paths shown.

For this lab, you can use a single workspace and separate data assets to represent development and production data.

## Create your GitHub repository from the template

Next, you create your own GitHub repository from the original lab repo so you can use GitHub Actions. This follows the same template-based approach you used in the previous lab.

1. In a browser, go to `https://github.com/MicrosoftLearning/mslearn-mlops`.
1. In the upper-right corner, select **Use this template** and then choose **Create a new repository**.
1. In the **Owner** field, select your GitHub account. In the **Repository name** field, enter a name such as `mslearn-mlops`.
1. Select **Create repository from template**.
1. In your new repository that was created from the template, go to the **Actions** tab and enable GitHub Actions if prompted.
1. Note the clone URL for your new repository (for example, `https://github.com/<your-alias>/mslearn-mlops.git`). You use this URL when you work with the repository locally or from a development environment.
 
With your template-based repository in place and your workspace already provisioned, you can now connect GitHub securely to Azure.

## Prepare your GitHub repo, environments, and secrets

Next, you set up GitHub so that you can run training in a dev environment and later deploy from a prod environment.

1. In a browser, go to the repository you created from the `MicrosoftLearning/mslearn-mlops` template.
1. In your repo, go to the **Actions** tab and enable GitHub Actions if prompted.
1. In the repo, go to **Settings** > **Environments**.
1. Create two environments:
	- `dev`
	- `prod`
1. In the Azure portal Cloud Shell, create a service principal that has **Contributor** access to your resource group. Replace `<service-principal-name>`, `<subscription-id>`, and `<your-resource-group-name>` before running the command:

	```azurecli
	az ad sp create-for-rbac --name "<service-principal-name>" --role contributor \
	    --scopes /subscriptions/<subscription-id>/resourceGroups/<your-resource-group-name> \
	    --sdk-auth
	```

1. Copy the full JSON output and save it temporarily. You'll add it as a secret in both environments.
1. In your GitHub repository, go to **Settings** > **Environments** and select the `dev` environment.
1. Add a new environment secret named `AZURE_CREDENTIALS` and paste the JSON output from the service principal as the value. Save the secret.
1. Repeat the previous two steps for the `prod` environment so that both environments have an `AZURE_CREDENTIALS` secret.
1. (Optional) In the `prod` environment, add an **environment protection rule** that requires manual approval before a job can run in this environment.

GitHub can now authenticate to Azure for both dev and prod via environment-specific secrets and protection rules.

## Train and validate a model in dev from a pull request

Now you use a GitHub Actions workflow in your template-based repository that trains your model against dev data whenever someone proposes a change to the training configuration.

1. Clone your `mslearn-mlops` repository that you created from the template to a development machine where you can edit files and push changes.
1. In your local clone, open `src/train-model-parameters.py` and review how it:
	- Reads training data from a file or folder path.
	- Trains a logistic regression model and logs metrics such as **Accuracy** and **AUC**.
1. Open `src/job.yml` and replace the placeholder values for the `training_data` input so the command job uses the dev folder data asset by default:

	```yml
	inputs:
	  training_data:
	    type: uri_folder
	    path: azureml:diabetes-dev-folder@latest
	```
1. Open `src/job.yml` and review how the Azure Machine Learning command job:
	- Runs `train-model-parameters.py` on the `aml-cluster` compute.
	- Uses a `training_data` input that points to the `diabetes-dev-folder` data asset by default.
	- Accepts a configurable `reg_rate` hyperparameter.
1. Review the workflow at `.github/workflows/train-dev.yml` to see how it:
	- Signs in to Azure by using the `AZURE_CREDENTIALS` secret in the `dev` environment.
	- Detects the resource group and workspace that the `infra/setup.sh` script created.
	- Submits the Azure Machine Learning job defined in `src/job.yml`, overriding the `training_data` input to use the `diabetes-dev-folder` data asset.
	- Streams the job logs, parses the **Accuracy** and **AUC** values from the output, and posts them as a comment on the pull request.
1. In your local clone, open `.github/workflows/train-dev.yml` and add a `pull_request` trigger so the workflow only runs automatically when a pull request changes the training code:

	```yml
	on:
	  workflow_dispatch:
	  pull_request:
	    branches:
	      - main
	    paths:
	      - 'src/train-model-parameters.py'
	      - 'src/job.yml'
	```
1. In your local clone, create a new feature branch and make a small, safe hyperparameter change. For example, adjust the default value of `--reg_rate` in `src/train-model-parameters.py`.
1. Commit your change and push the new branch to GitHub.
1. In GitHub, create a pull request from your feature branch into `main`.
1. On the pull request page, observe that the **Train model in dev** workflow runs automatically because of the `pull_request` trigger you added, and wait for it to complete.
1. When the workflow run has finished, review the comments on the pull request. You should see a comment from the workflow that includes the dev **Accuracy** and **AUC** values from the training job.

The dev workflow stays manual by default and only starts running automatically for pull requests after you add the trigger. That keeps unnecessary runs out of the live repo while still letting you enable PR validation when you're ready.

## Retrain the model on prod data from a pull request comment

After you're satisfied that the dev training results look reasonable, you can request a prod training run that uses the prod data asset and the `prod` environment in GitHub Actions.

1. In your GitHub repository, open **Settings** > **Environments** and verify that you have a `prod` environment with an `AZURE_CREDENTIALS` secret configured (just as you did earlier for `dev`).
1. On the same pull request where you validated the dev run, add a new comment that contains the command `/train-prod` on its own line.
1. In the **Actions** tab, observe that the **Train model in prod (PR comment)** workflow (defined in `.github/workflows/train-prod.yml`) starts in response to your comment.
1. Wait for the workflow to complete. The workflow:
	- Signs in to Azure by using the `AZURE_CREDENTIALS` secret in the `prod` environment.
	- Detects the same Azure Machine Learning workspace you used for dev.
	- Submits the `src/job.yml` command job again, this time overriding the `training_data` input to use the `diabetes-prod-folder` data asset.
	- Streams the logs, parses **Accuracy** and **AUC** from the output, and posts them back to the pull request as a separate comment.
1. Review the new comment on the pull request that includes the **prod** evaluation metrics. Compare these values to the dev metrics to understand how your model behaves on production-like data.

By using a comment command to trigger prod training, you keep control over when prod workloads run while still capturing the results as part of the pull request discussion.

## Deploy the model to a real-time endpoint from a pull request comment

With dev and prod training complete and reviewed, you're ready to deploy the model to a managed online endpoint by using a Python script and another comment-triggered workflow.

1. In your local clone, open `src/deploy_to_online_endpoint.py` and review how it:
	- Connects to your Azure Machine Learning workspace by using `DefaultAzureCredential` and `MLClient`.
	- Ensures that an online endpoint (for example, `diabetes-endpoint`) exists or creates it if needed.
	- Creates or updates a deployment (for example, `blue`) that uses the MLflow model in the local `model` folder.
	- Directs 100% of endpoint traffic to the specified deployment and prints the scoring URI.
1. Review the workflow at `.github/workflows/deploy-prod.yml` to see how it:
	- Listens for a `/deploy-prod` comment on a pull request.
	- Uses the `prod` environment and `AZURE_CREDENTIALS` secret to authenticate to Azure.
	- Detects the subscription, resource group, and workspace created by `infra/setup.sh`.
	- Runs `deploy_to_online_endpoint.py` with the detected values to deploy the MLflow model to a managed online endpoint.
1. On your pull request, add a comment that contains `/deploy-prod` on its own line.
1. In the **Actions** tab, watch the **Deploy model to online endpoint (PR comment)** workflow run and wait for it to complete successfully.
1. When the workflow has finished, review the new comment on the pull request that confirms the deployment. Then, in Azure Machine Learning studio, go to **Endpoints** > **Real-time endpoints**, select the `diabetes-endpoint`, and use the **Test** tab to send a sample request.

Your production endpoint now serves a model that was trained and reviewed through a PR-based workflow, with dev and prod metrics visible in the pull request and a scripted deployment you can repeat and extend.

## Enable data collection and configure model monitoring

To monitor for drift and quality issues, Azure Machine Learning needs access to production inference data from your endpoint.

1. In Azure Machine Learning studio, on your real-time endpoint, open the **Settings** or **Data collection** section.
1. Enable **Model data collection** for the endpoint so that inputs and outputs are stored in a workspace datastore.
1. Save the changes.
1. In the left navigation, go to **Monitoring** (or **Model monitoring**, depending on your workspace view).
1. Create a new monitor and associate it with your online endpoint.
1. Configure the monitor with settings such as:
	- **Monitoring signals**: enable **Data drift**.
	- **Reference data**: use the training data asset (for example, `diabetes-dev-folder`).
	- **Production data**: use the data collected from the online endpoint.
	- **Frequency**: set a reasonable schedule (for example, daily).
1. Save and enable the monitor.

Once the first monitoring run completes, you can review metrics like drift scores and see whether the production data distribution is diverging from the training data.

## Simulate drift and retrain through the PR workflow

In a real system, drift or performance degradation would trigger retraining. In this lab, you simulate this by changing a training parameter and then repeating the same PR-based dev → prod → deploy flow you used earlier.

1. Wait until your monitor has run at least once and review the drift metrics in Azure Machine Learning studio.
1. In your local clone of the repo, create a new feature branch to represent your retraining work. For example:

		```bash
		git checkout -b feature/drift-retrain
		```

1. Open `src/train-model-parameters.py` and change the default regularization rate or another safe parameter (for example, adjust the default value of `--reg_rate`) to represent how you want to respond to drift.
1. Commit the change and push the branch to GitHub:

		```bash
		git add src/train-model-parameters.py
		git commit -m "Retrain in response to drift"
		git push --set-upstream origin feature/drift-retrain
		```

1. In GitHub, create a new pull request from your `feature/drift-retrain` branch into `main`.
1. Observe that the **Train model in dev** workflow runs automatically for the new pull request because you added the `pull_request` trigger earlier. When it completes, review the comment that shows the updated **dev** Accuracy and AUC.
1. If the dev metrics look acceptable, add a comment `/train-prod` on the pull request to trigger the **Train model in prod (PR comment)** workflow. When it completes, review the comment that shows the updated **prod** Accuracy and AUC.
1. If the prod metrics also meet your expectations, add a comment `/deploy-prod` on the pull request to trigger the **Deploy model to online endpoint (PR comment)** workflow. Wait for it to complete.
1. Finally, in Azure Machine Learning studio, go to **Endpoints** > **Real-time endpoints**, select the `diabetes-endpoint`, and use the **Test** tab to confirm that the endpoint still returns predictions after your retraining and deployment.

By repeating the same PR-based dev → prod → deploy workflow in response to simulated drift, you see how monitoring, retraining, and controlled promotion can work together in an end-to-end MLOps process.

## (Optional) Roll back to a previous model version

If the newly deployed model introduces a regression or causes unexpected behavior in production, you can roll back to a previous version directly in Azure Machine Learning studio without rerunning any workflows.

1. In Azure Machine Learning studio, go to **Endpoints** > **Real-time endpoints** and select `diabetes-endpoint`.
1. On the **Deployments** tab, review the list of deployments. You should see the current `blue` deployment associated with the model version you most recently deployed.
1. To create a rollback deployment from a previous model version:
	1. In the left navigation, go to **Models** and open the model (for example, `train` or the name used in your `model/MLmodel` file).
	1. In the model's **Versions** list, identify the version you want to roll back to (for example, the version before the most recent deployment).
	1. Select that version, then select **Deploy** > **Real-time endpoint**.
	1. In the deployment wizard, select **Existing endpoint** and choose `diabetes-endpoint`.
	1. Give the new deployment a distinct name, such as `rollback`.
	1. Accept the remaining defaults and select **Deploy**.
	1. Wait for the deployment to reach a **Succeeded** state.
1. Once the `rollback` deployment is ready, return to **Endpoints** > **Real-time endpoints** > `diabetes-endpoint`.
1. On the **Deployments** tab, select **Update traffic**.
1. Set the traffic allocation so that `rollback` receives **100%** of traffic and `blue` receives **0%**. Select **Update** to apply the change.
1. On the **Test** tab, send a sample request to confirm that the endpoint now returns predictions from the rollback model version.
1. (Optional) To flag the problematic model version so it is excluded from future deployments, go back to **Models**, open the affected version, and set its **Stage** to **Archived**.

> **Tip:** Because traffic routing is updated immediately, rolling back in the UI takes effect without any downtime for the endpoint. When you're confident the rollback is stable, you can delete the original `blue` deployment from the **Deployments** tab to reduce hosting costs.

## Clean up Azure resources

When you finish exploring Azure Machine Learning, you should delete the resources you've created to avoid unnecessary Azure costs.

1. Close the Azure Machine Learning studio tab and return to the Azure portal.
1. In the Azure portal, on the **Home** page, select **Resource groups**.
1. Select the **rg-ai300-...** resource group that contains your Azure Machine Learning workspace and any associated resources.
1. At the top of the **Overview** page for your resource group, select **Delete resource group**.
1. Enter the resource group name to confirm you want to delete it, and select **Delete**.

