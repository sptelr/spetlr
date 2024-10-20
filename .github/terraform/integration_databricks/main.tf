terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.7.0"
    }
    databricks = {
      source = "databricks/databricks"
    }
  }
  backend "local" {
    path = "integration_databricks.tfstate"
  }
}

variable "subscription_id" {}
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
provider "databricks" {
  alias      = "account"
  host       = "https://accounts.azuredatabricks.net"
  account_id = var.db_account_id
}

provider "databricks" {
  alias = "workspace"
  host  = data.azurerm_databricks_workspace.db_workspace.workspace_url
}


variable "uniqueRunId" {}

module "config" {
  source      = "../modules/config"
  uniqueRunId = var.uniqueRunId
}
