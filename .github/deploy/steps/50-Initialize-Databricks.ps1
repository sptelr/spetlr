###############################################################################################
# Initialize Databricks
###############################################################################################
Write-Host "Initialize Databricks Configuration" -ForegroundColor Green

Write-Host "  Collect resourceId and workspace URL" -ForegroundColor DarkYellow
$resourceId = az resource show `
  --resource-group $resourceGroupName `
  --name $databricksName `
  --resource-type "Microsoft.Databricks/workspaces" `
  --query id `
  --out tsv

Throw-WhenError -output $resourceId

Write-Host "Get Databricks workspace URL" -ForegroundColor DarkYellow
$workspaceUrl = az resource show `
  --resource-group $resourceGroupName `
  --name $databricksName `
  --resource-type "Microsoft.Databricks/workspaces" `
  --query properties.workspaceUrl `
  --out tsv

$workspaceUrl = "https://$workspaceUrl"
Throw-WhenError -output $workspaceUrl
Write-Host "Workspace URL is: $workspaceUrl" -ForegroundColor DarkYellow

Write-Host "Get Bearer token for dbSpn" -ForegroundColor DarkYellow
$bearerToken = Get-OAuthToken `
  -tenantId $tenantId `
  -clientId $dbSpn.clientId `
  -clientSecret $dbSpn.secretText

Write-Host "Set SPN as the workspace admin" -ForegroundColor DarkYellow
Set-DatabricksSpnAdminUser `
  -tenantId $tenantId `
  -clientId $dbSpn.clientId `
  -clientSecret $dbSpn.secretText `
  -resourceId $resourceId `
  -workspaceUrl $workspaceUrl `
  -bearerToken $bearerToken

Write-Host "Convert Bearer token to Databricks personal access token" -ForegroundColor DarkYellow
$databricksAccessToken = ConvertTo-DatabricksPersonalAccessToken `
  -workspaceUrl $workspaceUrl `
  -bearerToken $bearerToken

Write-Host "Generate .databrickscfg" -ForegroundColor DarkYellow
Set-Content ~/.databrickscfg "[DEFAULT]"
Add-Content ~/.databrickscfg "host = $workspaceUrl"
Add-Content ~/.databrickscfg "token = $databricksAccessToken"
Add-Content ~/.databrickscfg ""

# [Environment]::SetEnvironmentVariable('DATABRICKS_AAD_TOKEN', $databricksAccessToken)

# Write-Host "  Connect to Databricks" -ForegroundColor DarkYellow
# $output = databricks configure --host $workspaceUrl --aad-token
# Throw-WhenError -output $output
