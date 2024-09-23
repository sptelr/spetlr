data "databricks_service_principal" "cicd_spn" {
  display_name = module.config.permanent.cicd_spn_name
}

variable "db_account_id" {
  type        = string
  description = "The databricks Account Id for Spetlr subscription."
}