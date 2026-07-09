#!/usr/bin/env bash

set -u

# Change the values of these variables as needed.
# You can also pass a suffix as the first argument when starting the script.

DEFAULT_LOCATION=""
RESOURCE_PROVIDER="Microsoft.MachineLearningServices"
REGIONS=("eastus" "westus" "centralus" "northeurope" "westeurope")
COMPUTE_CLUSTER="aml-cluster"
COMPUTE_SIZE="STANDARD_DS11_V2"
MAX_RETRIES=3
RETRY_DELAY=5

# ============================================================================
# DON'T CHANGE ANYTHING BELOW THIS LINE.
# ============================================================================

generate_suffix() {
  if command -v uuidgen >/dev/null 2>&1; then
    uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-' | cut -c1-18
  else
    printf '%(%s)T\n' -1 | tr -d '\n' | cut -c1-18
  fi
}

if [[ -n "${1:-}" ]]; then
  suffix=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9' | cut -c1-18)
else
  suffix=$(generate_suffix)
fi

if [[ -z "$suffix" ]]; then
  echo "Error: A valid suffix could not be determined."
  exit 1
fi

if [[ -n "$DEFAULT_LOCATION" ]]; then
  RANDOM_REGION="$DEFAULT_LOCATION"
else
  RANDOM_REGION=${REGIONS[$RANDOM % ${#REGIONS[@]}]}
fi

RESOURCE_GROUP="rg-ai300-l${suffix}"
WORKSPACE_NAME="mlw-ai300-l${suffix}"
COMPUTE_INSTANCE="ci${suffix}"

run_az_command() {
  local description="$1"
  shift

  local attempt=1
  local exit_code=0

  while (( attempt <= MAX_RETRIES )); do
    echo "$description"
    "$@"
    exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
      return 0
    fi

    echo "Warning: command failed (attempt ${attempt}/${MAX_RETRIES})."

    if (( attempt == MAX_RETRIES )); then
      echo "Error: unable to complete operation after ${MAX_RETRIES} attempts."
      return $exit_code
    fi

    echo "Retrying in ${RETRY_DELAY} seconds..."
    sleep "$RETRY_DELAY"
    attempt=$((attempt + 1))
  done

  return $exit_code
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: Required command '$1' is not installed or not in PATH."
    return 1
  fi
}

check_prerequisites() {
  echo "Checking prerequisites..."

  require_command az || return 1

  if ! az account show >/dev/null 2>&1; then
    echo "Error: Not authenticated with Azure. Please run: az login"
    return 1
  fi

  echo "✓ Azure CLI is available and authenticated"
}

register_resource_provider() {
  run_az_command \
    "Register the Machine Learning resource provider:" \
    az provider register --namespace "$RESOURCE_PROVIDER"
}

create_resource_group() {
  run_az_command \
    "Create a resource group and set as default:" \
    az group create --name "$RESOURCE_GROUP" --location "$RANDOM_REGION" || return 1

  run_az_command \
    "Set the default resource group:" \
    az configure --defaults group="$RESOURCE_GROUP"
}

create_workspace() {
  run_az_command \
    "Create an Azure Machine Learning workspace:" \
    az ml workspace create --name "$WORKSPACE_NAME" || return 1

  run_az_command \
    "Set the default Azure Machine Learning workspace:" \
    az configure --defaults workspace="$WORKSPACE_NAME"
}

create_compute_instance() {
  run_az_command \
    "Creating a compute instance with name: $COMPUTE_INSTANCE" \
    az ml compute create --name "$COMPUTE_INSTANCE" --size "$COMPUTE_SIZE" --type ComputeInstance
}

create_compute_cluster() {
  run_az_command \
    "Creating a compute cluster with name: $COMPUTE_CLUSTER" \
    az ml compute create --name "$COMPUTE_CLUSTER" --size "$COMPUTE_SIZE" --max-instances 2 --type AmlCompute
}

create_data_assets() {
  run_az_command \
    "Create training data asset (MLTable):" \
    az ml data create --type mltable --name "diabetes-training" --path ../data/diabetes-data || return 1

  run_az_command \
    "Create training data asset (CSV):" \
    az ml data create --type uri_file --name "diabetes-data" --path ../data/diabetes-data/diabetes.csv
}

run_full_setup() {
  check_prerequisites || return 1
  register_resource_provider || return 1
  create_resource_group || return 1
  create_workspace || return 1
  create_compute_instance || return 1
  create_compute_cluster || return 1
  create_data_assets || return 1

  echo ""
  echo "Setup complete."
}

show_status() {
  echo "Current configuration"
  echo "====================================================================="
  echo "Suffix: $suffix"
  echo "Resource Group: $RESOURCE_GROUP"
  echo "Location: $RANDOM_REGION"
  echo "Workspace: $WORKSPACE_NAME"
  echo "Compute Instance: $COMPUTE_INSTANCE"
  echo "Compute Cluster: $COMPUTE_CLUSTER"
  echo "====================================================================="
  echo "Suggested order: 1 -> 2 -> 3 -> 4 -> 5, or use option 6."
}

show_menu() {
  clear
  echo "====================================================================="
  echo "    Azure Machine Learning Lab Setup Menu"
  echo "====================================================================="
  echo "Suffix: $suffix"
  echo "Resource Group: $RESOURCE_GROUP"
  echo "Location: $RANDOM_REGION"
  echo "Workspace: $WORKSPACE_NAME"
  echo "====================================================================="
  echo "1. Register Machine Learning resource provider"
  echo "2. Create resource group and set defaults"
  echo "3. Create Azure Machine Learning workspace"
  echo "4. Create compute resources"
  echo "5. Create data assets"
  echo "6. Run full setup"
  echo "7. Show configuration"
  echo "8. Exit"
  echo "====================================================================="
}

while true; do
  show_menu
  read -r -p "Please select an option (1-8): " choice

  case "$choice" in
    1)
      echo ""
      check_prerequisites && register_resource_provider
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
    2)
      echo ""
      check_prerequisites && create_resource_group
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
    3)
      echo ""
      check_prerequisites && create_workspace
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
    4)
      echo ""
      check_prerequisites && create_compute_instance && create_compute_cluster
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
    5)
      echo ""
      check_prerequisites && create_data_assets
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
    6)
      echo ""
      run_full_setup
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
    7)
      echo ""
      show_status
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
    8)
      echo "Exiting..."
      clear
      exit 0
      ;;
    *)
      echo ""
      echo "Invalid option. Please select 1-8."
      echo ""
      read -r -p "Press Enter to continue..."
      ;;
  esac

  echo ""
done
