---
lab:
    title: 'Plan and prepare an MLOps solution with Azure Machine Learning'
    description: 'Design dev and prod environments and plan Azure CLI automation to provision workspaces, registries, and data assets.'
    level: 300
    duration: 45 minutes
---

# Plan and prepare an MLOps solution with Azure Machine Learning

As your machine learning solution matures, you move from one-off experiments to a repeatable process for training, evaluating, and deploying models. To support this process, you need an environment strategy and automation that can reliably provision the Azure resources you depend on.

In this exercise, you'll focus on planning and preparing an MLOps-ready environment in three phases:

- Review the existing Azure CLI script that provisions a development Azure Machine Learning workspace and related resources.
- Design a production environment that uses a shared Azure Machine Learning registry for models, but isolates production data from development data.
- Plan how you would extend the existing `infra/setup.sh` script to support dev and prod environments with Azure CLI commands.

You won't run all of the commands you design in this lab. Instead, you focus on understanding the architecture, naming, and scripting patterns you would use to automate a real-world MLOps setup.

## Before you start

You'll need an [Azure subscription](https://azure.microsoft.com/free?azure-portal=true) in which you have administrative-level access.

## Review the existing development environment script

You can manually create necessary resources and assets to work with Azure Machine Learning through the portal. However, when you want to easily track and automate your work, working with CLI commands is easier. You can combine CLI commands in a shell script. In this section, you review a shell script and identify what it provisions.

1. In a browser, open the Azure portal at `https://portal.azure.com/`, signing in with your Microsoft account.
1. Select the \[>_] (*Cloud Shell*) button at the top of the page to the right of the search box. This opens a Cloud Shell pane at the bottom of the portal.
1. Select **Bash** if asked. The first time you open the Cloud Shell, you're asked to choose the type of shell you want to use (*Bash* or *PowerShell*).
1. Check that the correct subscription is specified and that **No storage account required** is selected. Select **Apply**.
1. In the terminal, enter the following commands to clone this repo:

		```azurecli
		rm -r mslearn-mlops -f
		git clone https://github.com/MicrosoftLearning/mslearn-mlops.git mslearn-mlops
		```

		> Use `SHIFT + INSERT` to paste your copied code into the Cloud Shell.

1. After the repo has been cloned, enter the following commands to change to the `infra` folder and open the setup script:

		```azurecli
		cd mslearn-mlops/infra
		code setup.sh
		```

		> [!NOTE]
		> If the `code` command is not available, you are in the new Cloud Shell experience. Switch to Classic Cloud Shell by selecting **Switch to Classic Cloud Shell** in the toolbar and selecting **Confirm**. Then run the commands again.

1. Review the script and identify the resources that are created for your current **development** environment:
		- A resource group with a randomized suffix, for example `rg-ai300-l...`.
		- An Azure Machine Learning workspace, for example `mlw-ai300-l...`.
		- A compute instance for interactive work.
		- A compute cluster for training jobs.
		- Data assets for the diabetes training data in the `data/diabetes-data` folder.

1. Note how the script:
		- Generates a random suffix to avoid name collisions.
		- Registers the **Microsoft.MachineLearningServices** resource provider.
		- Sets default values for the resource group and workspace so subsequent `az ml` commands use them automatically.

By understanding what this script does for development, you're ready to think about what you would change or add for production.

## Design dev and prod environments for MLOps

Before you add more commands, you need a clear picture of how you want your environments to look. A common MLOps pattern is to:

- Use **separate workspaces** for development and production to isolate experiments from production workloads.
- Use a **shared Azure Machine Learning registry** to store and promote reusable assets such as models and environments across workspaces.
- Use **separate data assets** so that production data never appears in the development environment.

For this lab, imagine the following target architecture:

- **Dev workspace** for experimentation:
	- Resource group: `rg-ai300-dev-<suffix>`
	- Workspace: `mlw-ai300-dev-<suffix>`
	- Data asset: `diabetes-dev-folder` that points to the sample data in the `data/diabetes-data` folder.
- **Prod workspace** for production training and deployment:
	- Resource group: `rg-ai300-prod-<suffix>`
	- Workspace: `mlw-ai300-prod-<suffix>`
	- Data asset: `diabetes-prod-folder` that points to the larger dataset in the `production/data` folder.
- **Shared registry** for reusable assets:
	- Registry: `mlr-ai300-shared-<suffix>` in a central resource group.
	- Both workspaces can push and pull models and environments from this registry.

> [!NOTE]
> In production, you typically create separate workspaces (and sometimes separate subscriptions) for dev, test, and prod. For this lab you focus on the **design** and **scripts**. You don't need to actually create multiple workspaces if you want to avoid extra Azure costs.

With this design in mind, you're ready to plan the Azure CLI commands you would add to your automation.

## Plan Azure CLI commands for a production workspace and shared registry

Next, you map your target architecture to Azure CLI commands. Instead of running them immediately, you use this section to reason about the resources and naming conventions you would use.

1. In the Cloud Shell editor, create a new file based on the existing script so you can experiment safely:

		```bash
		cp setup.sh setup-prod-design.sh
		code setup-prod-design.sh
		```

1. At the top of the new file, add variables for both environments and the shared registry. For example:

		```bash
		# Existing random suffix
		guid=$(cat /proc/sys/kernel/random/uuid)
		suffix=${guid//[-]/}
		suffix=${suffix:0:18}

		# Dev environment
		DEV_RESOURCE_GROUP="rg-ai300-dev-${suffix}"
		DEV_WORKSPACE_NAME="mlw-ai300-dev-${suffix}"

		# Prod environment
		PROD_RESOURCE_GROUP="rg-ai300-prod-${suffix}"
		PROD_WORKSPACE_NAME="mlw-ai300-prod-${suffix}"

		# Shared registry (one per subscription/region)
		REGISTRY_RESOURCE_GROUP="rg-ai300-reg-${suffix}"
		REGISTRY_NAME="mlr-ai300-shared-${suffix}"
		```

1. Plan the commands that would create the **shared registry** in its own resource group. For example:

		```azurecli
		# Create a resource group for the shared registry
		az group create --name $REGISTRY_RESOURCE_GROUP --location $RANDOM_REGION

		# Create an Azure Machine Learning registry
		az ml registry create \
			--name $REGISTRY_NAME \
			--resource-group $REGISTRY_RESOURCE_GROUP \
			--location $RANDOM_REGION
		```

1. Plan the commands that would create the **production** resource group and workspace. They follow the same pattern as the existing dev workspace, but use the prod names:

		```azurecli
		# Create the production resource group
		az group create --name $PROD_RESOURCE_GROUP --location $RANDOM_REGION

		# Create the production Azure Machine Learning workspace
		az ml workspace create \
			--name $PROD_WORKSPACE_NAME \
			--resource-group $PROD_RESOURCE_GROUP \
			--location $RANDOM_REGION
		```

1. Finally, plan the data assets that keep dev and prod data separated. Use the **dev** folder for experimentation and the **production** folder for production training:

		```azurecli
		# In the dev workspace: data asset that points to experimentation data
		az configure --defaults group=$DEV_RESOURCE_GROUP workspace=$DEV_WORKSPACE_NAME
		az ml data create \
			--type uri_folder \
			--name diabetes-dev-folder \
			--path ../data/diabetes-data

		# In the prod workspace: data asset that points to production data
		az configure --defaults group=$PROD_RESOURCE_GROUP workspace=$PROD_WORKSPACE_NAME
		az ml data create \
			--type uri_folder \
			--name diabetes-prod-folder \
			--path ../production/data
		```

> [!IMPORTANT]
> For this lab, you **don't need** to run the new commands that create extra resource groups and workspaces. Focus on understanding how you would structure the script so that dev and prod resources are clearly separated and production data stays out of the development environment. If you do want to run the script, follow the optional steps in the next section.

By planning these commands, you've translated your architecture into concrete Azure CLI operations that you can automate in a shell script.

## Optional: run your design script

If you want to see your design in action, you can validate your script against a reference solution and then run it. This step is optional and will incur Azure costs while the resources exist.

1. In the Cloud Shell terminal, make sure you're in the `infra` folder:

		```bash
		cd mslearn-mlops/infra
		```

1. The repo includes a reference script `infra/setup-mlops-envs.sh` that shows what the complete script should look like. Compare it with your own `setup-prod-design.sh` to check your work:

		```bash
		diff setup-prod-design.sh setup-mlops-envs.sh
		```

		Review any differences and update your script if needed.

1. Once you're satisfied with your script, make it executable and run it:

		```bash
		chmod +x setup-prod-design.sh
		./setup-prod-design.sh
		```

1. When the script completes, verify the resources in the Azure portal:
		- New resource groups for dev, prod, and the shared registry.
		- Separate workspaces for dev and prod.
		- Data assets `diabetes-dev-folder` and `diabetes-prod-folder` in the respective workspaces.

1. When you're done exploring, be sure to delete any extra resource groups you created so you don't continue to incur charges.

## Plan how to extend the setup script for multiple environments

In a real MLOps project, you want a single automation entry point that can provision the right environment on demand. In this section, you think about how you would evolve the existing script to support this goal.

1. Decide how you would pass the **target environment** into the script. For example, you could accept a parameter such as `dev` or `prod`:

		```bash
		ENVIRONMENT=${1:-dev}
		```

1. Based on the environment, plan how you would set the resource group and workspace variables. For example:

		```bash
		if [ "$ENVIRONMENT" = "prod" ]; then
			RESOURCE_GROUP=$PROD_RESOURCE_GROUP
			WORKSPACE_NAME=$PROD_WORKSPACE_NAME
		else
			RESOURCE_GROUP=$DEV_RESOURCE_GROUP
			WORKSPACE_NAME=$DEV_WORKSPACE_NAME
		fi
		```

1. Think through which resources should be **shared** and which should be **isolated**:
		- The registry is shared between dev and prod, so you'd create it once and reuse it.
		- Workspaces, compute, and data assets are environment-specific so that you can apply different security and access controls.

1. Consider how this script would fit into your broader MLOps workflows:
		- In **GitHub Actions**, you could call the script with `dev` when validating pull requests and `prod` when deploying approved models.
		- In **local development**, data scientists could call the script with `dev` to recreate the experimentation environment from scratch.

You now have a clear plan for how to evolve the existing script into a more flexible provisioning tool without changing how earlier labs work.

## Clean up Azure resources

When you finish exploring Azure Machine Learning, you should delete the resources you've created to avoid unnecessary Azure costs.

1. Close the Azure Machine Learning studio tab and return to the Azure portal.
1. In the Azure portal, on the **Home** page, select **Resource groups**.
1. If you created any additional resource groups while experimenting with this lab (for example, `rg-ai300-dev-...`, `rg-ai300-prod-...`, or `rg-ai300-reg-...`), delete those resource groups as well.
1. Select the **rg-ai300-...** resource group that was created by the original `setup.sh` script.
1. At the top of the **Overview** page for your resource group, select **Delete resource group**.
1. Enter the resource group name to confirm you want to delete it, and select **Delete**.
