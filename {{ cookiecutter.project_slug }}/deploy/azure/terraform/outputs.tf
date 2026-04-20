output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "container_registry_login_server" {
  value = azurerm_container_registry.app.login_server
}

output "storage_account_name" {
  value = azurerm_storage_account.media.name
}
