---
lab:
    title: 'Automate model training with GitHub Actions'
    description: 'Securely integrate GitHub with Azure Machine Learning and automate model training with GitHub Actions workflows.'
    level: 300
    duration: 45 minutes
---

# Automate model training with GitHub Actions

As your machine learning solution matures, you move from running ad-hoc experiments in Azure Machine Learning to automating repeatable training workflows. GitHub Actions lets you run Azure Machine Learning jobs whenever you need them, using secure, traceable workflows that fit into your existing source control practices.

In this exercise, you automate model training with GitHub Actions in three phases:

- Configure secure access from GitHub to your Azure Machine Learning workspace by using a service principal and GitHub secrets.
- Run an Azure Machine Learning command job from a manually triggered GitHub Actions workflow.
- Use feature-based development and branch protection so that model training runs as part of a pull request workflow.

Along the way, you review how workspace networking and source control settings influence how you design secure automation for model training.

## Before you start

You need:

- An [Azure subscription](https://azure.microsoft.com/free?azure-portal=true) in which you have administrative-level access.
- A [GitHub](https://github.com/) account with permission to create repositories and configure GitHub Actions.

## Provision an Azure Machine Learning workspace

First, you create the Azure Machine Learning workspace and compute resources you'll use from your GitHub workflows.

1. In a browser, open the Azure portal at `https://portal.azure.com/` and sign in with your Microsoft account.
1. Select the **[>_]** (**Cloud Shell**) button at the top of the page to open Cloud Shell, and choose **Bash** if you're prompted.
1. Make sure the correct subscription is selected and that **No storage account required** is selected. Then select **Apply**.
1. In the Cloud Shell terminal, clone the original lab repo and run the setup script:

	```azurecli
	rm -r mslearn-mlops -f
	git clone https://github.com/MicrosoftLearning/mslearn-mlops.git mslearn-mlops
	cd mslearn-mlops/infra
	./setup.sh
	```

	> Ignore any messages that say that extensions couldn't be installed.

1. Wait for the script to finish. It creates a resource group, an Azure Machine Learning workspace, and compute resources.
1. In the Azure portal, go to **Resource groups** and open the `rg-ai300-...` resource group that was created.
1. Select the Azure Machine Learning workspace (for example, `mlw-ai300-...`) and then select **Launch studio** to open Azure Machine Learning studio.

With a workspace in place, you can now create your own GitHub repository and configure secure access.

## Create your GitHub repository from the template

Next, you create your own GitHub repository from the original lab repo so you can use GitHub Actions.

1. In a browser, go to `https://github.com/MicrosoftLearning/mslearn-mlops`.
1. In the upper-right corner, select **Use this template** and then choose **Create a new repository**.
1. In the **Owner** field, select your GitHub account. In the **Repository name** field, enter a name such as `mslearn-mlops`.
1. Select **Create repository from template**.
1. In your new repository that was created from the template, go to the **Actions** tab and enable GitHub Actions if prompted.
1. Note the clone URL for your new repository (for example, `https://github.com/<your-alias>/mslearn-mlops.git`). You use this URL when you work with the repository locally or from a development environment.

With your template-based repository in place, you can now connect GitHub securely to Azure.

## Configure GitHub integration with Azure Machine Learning

To let GitHub Actions authenticate to Azure Machine Learning, you use a service principal. The credentials for this service principal are stored as an encrypted secret in your GitHub repository.

1. In the Azure portal, select the **[>_]** (**Cloud Shell**) button at the top of the page to open Cloud Shell.
1. Select **Bash** if you are prompted to choose a shell type.
1. Make sure the correct subscription is selected for your Azure Machine Learning workspace.
1. In Cloud Shell, create a service principal that has **Contributor** access to the resource group that contains your Azure Machine Learning workspace. Replace `<service-principal-name>`, `<subscription-id>`, and `<your-resource-group-name>` with your own values before you run the command. Use a descriptive name such as `sp-mslearn-mlops-github`:

	```azurecli
	az ad sp create-for-rbac --name "<service-principal-name>" --role contributor \
			--scopes /subscriptions/<subscription-id>/resourceGroups/<your-resource-group-name> \
			--sdk-auth
	```

1. Copy the full JSON output of the command to a safe location. You use the values in the next steps and in later challenges.
1. In the GitHub repository you created from the template, navigate to **Settings** > **Secrets and variables** > **Actions**.
1. Select **New repository secret**.
1. Enter `AZURE_CREDENTIALS` as the **Name** of the secret.
1. Paste the JSON output from the `az ad sp create-for-rbac` command into the **Value** field and select **Add secret**.
1. Select the **Variables** tab and then select **New repository variable**.
1. Enter `AZURE_RESOURCE_GROUP` as the **Name** and your resource group name (for example, `rg-ai300-l<suffix>`) as the **Value**. Select **Add variable**.
1. Select **New repository variable** again. Enter `AZURE_WORKSPACE_NAME` as the **Name** and your Azure Machine Learning workspace name (for example, `mlw-ai300-l<suffix>`) as the **Value**. Select **Add variable**.

Your GitHub repository now has an encrypted secret that GitHub-hosted runners can use to sign in to Azure and submit jobs to your Azure Machine Learning workspace.

> [!NOTE]
> The service principal is scoped to your Azure Machine Learning resource group. In a production scenario, you would further restrict its permissions and combine it with network controls, such as private endpoints and self-hosted runners, to limit how and where jobs can be submitted.

## Review workspace network access options

Before you automate training from GitHub, review how your Azure Machine Learning workspace controls network access.

1. In **Azure Portal** on your Azure Machine Learning workspace, select **Settings** in the left navigation and then select **Networking**.
1. Review the **Public access** and the **Private endpoints** settings. Note how you can:
		- Allow public network access from all networks.
		- Restrict access to specific IP ranges.
		- Disable public network access and rely on private endpoints.
1. For this lab, keep the default public access settings so that GitHub-hosted runners can reach your workspace. In a production environment, you would typically:
		- Use private endpoints and virtual networks.
		- Run GitHub Actions on self-hosted runners that can reach those private networks.
		- Combine role-based access control (RBAC) with network rules to tightly control who can submit jobs.

Now that you understand the network options, you are ready to automate a training job from GitHub.

## Automate model training with a manually triggered workflow

In this section, you connect your GitHub workflow to Azure Machine Learning and run a command job to train a model. The workflow uses the `AZURE_CREDENTIALS` secret you created earlier.

1. Clone your `mslearn-mlops` repository that you created from the template to a development environment where you can edit files and push changes back to GitHub.
1. In the cloned repository, open `src/job.yml` and replace the placeholder values for the `training_data` input so the command job uses the single file data asset created by the setup script:

	```yml
	inputs:
	  training_data:
	    type: uri_file
	    path: azureml:diabetes-data@latest
	```
1. In the cloned repository, locate the `.github/workflows/manual-trigger-job.yml` workflow file.
1. Open `manual-trigger-job.yml` and review the existing steps. The workflow should:
		- Check out the repository code.
		- Install the Azure Machine Learning CLI extension.
		- Use the `AZURE_CREDENTIALS` secret to sign in to Azure via `azure/login@v2`.
1. At the end of the workflow, add a new step that submits the Azure Machine Learning job defined in `src/job.yml`. The command requires explicit `--resource-group` and `--workspace-name` flags, supplied from the GitHub Actions variables you created:

	```yml
	- name: Run Azure Machine Learning training job
		run: az ml job create -f src/job.yml --stream --resource-group ${{vars.AZURE_RESOURCE_GROUP}} --workspace-name ${{vars.AZURE_WORKSPACE_NAME}}
	```

1. Save your changes, commit them to your local repository, and push the changes to the **main** branch of your fork.
1. In GitHub, go to the **Actions** tab for your repository.
1. Select the workflow defined in `manual-trigger-job.yml` and use **Run workflow** to start it manually.
1. Wait for the workflow run to complete. Verify that the **Run Azure Machine Learning training job** step completes successfully.
1. In Azure Machine Learning studio, select **Jobs** and confirm that a new job based on `src/job.yml` has run successfully. Review the job inputs, metrics, and logs.

You have now automated the training job by using a GitHub Actions workflow that you can run on demand.

## Use feature-based development to trigger workflows

Running workflows manually is useful for initial testing, but in a team environment you usually want training workflows to run automatically when someone proposes a change. Next, you update the existing workflow so it runs for pull requests, and then you use feature branches and branch protection rules to control when the workflow runs.

1. In your GitHub repository, open the `.github/workflows/manual-trigger-job.yml` workflow file.
1. Update the `on` section so that the workflow can run both manually and when a pull request targets the **main** branch. For example:

	```yml
	on:
		workflow_dispatch:
		pull_request:
			branches:
				- main
	```

1. Commit the updated workflow file and push it to the **main** branch of your repository.
1. In GitHub, go to **Settings** > **Branches** and select **Add branch protection rule**.
1. Configure a rule for the **main** branch that prevents direct pushes. At a minimum, select:
		- **Branch name pattern**: `main`.
		- **Protect matching branches**.
1. Save the branch protection rule.
1. In your local clone of the repository, create a new branch for a feature change. For example:

	```bash
	git checkout -b feature/update-parameters
	```

1. Make a small, safe change to the training configuration. For example, adjust a hyperparameter value in `src/train-model-parameters.py` or in `src/job.yml`.
1. Commit your change to the feature branch and push the branch to GitHub:

	```bash
	git add .
	git commit -m "Adjust training parameters"
	git push --set-upstream origin feature/update-parameters
	```

1. In GitHub, create a pull request from your feature branch into **main**.
1. On the pull request page, observe that the workflow defined in `manual-trigger-job.yml` runs automatically because of the `pull_request` trigger you added.
1. After the workflow completes successfully, review the results and then complete the pull request to merge your changes into **main**.

By using feature branches, branch protection rules, and pull request–triggered workflows with the same training workflow definition, you ensure that model training automation is tied to controlled changes in source control.

## Clean up Azure resources

When you finish exploring Azure Machine Learning and GitHub Actions, you should delete the resources you created to avoid unnecessary Azure costs.

1. Close the Azure Machine Learning studio tab and return to the Azure portal.
1. In the Azure portal, on the **Home** page, select **Resource groups**.
1. Select the **rg-ai300-...** resource group that contains your Azure Machine Learning workspace.
1. At the top of the **Overview** page for your resource group, select **Delete resource group**.
1. Enter the resource group name to confirm you want to delete it, and select **Delete**.
1. In GitHub, you can also delete the repository you created from the `mslearn-mlops` template if you no longer need the workflows or sample code.

