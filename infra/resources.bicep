param name string = 'aiendpointdev'
param dockerImageName string = 'litellmdevapp'
param resourceToken string
@secure()
param authSecret string
param authClientId string = '60b7aa7b-7582-48c9-b071-e99f2ec0bf79'

param openAiResourceGroupLocation string
param openAiSkuName string = 'S0'
param gpt4oDeploymentCapacity int = 200
param gpt4oDeploymentName string = 'gpt-4o'
param gpt4oModelName string = 'gpt-4o'
param gpt4oModelVersion string = '2024-05-13'
param gpt35DeploymentCapacity int = 200
param gpt35DeploymentName string = 'gpt-35-turbo'
param gpt35ModelName string = 'gpt-35-turbo'
param gpt35ModelVersion string = '0125'
param openAI2ResourceGroupLocation string = 'northcentralus'
param embeddingDeploymentName string = 'embedding'
param embeddingDeploymentCapacity int = 120
param embeddingModelName string = 'text-embedding-ada-002'

param containerRegistryEndpoint string
param containerRegistryName string
@secure()
param liteLLMMasterKey string
@secure()
param postgresDbPassword string
param appGWSubscriptionId string = '9e44d5e3-fcdd-4192-98fe-feb9e7748478'
param appGWVNetName string = 'aiexploration2-westus_VNET'
param appGWRGName string = 'aiexploration2-westus_RG'

param location string = resourceGroup().location

param tags object = {}

var abbrs = loadJsonContent('./abbreviations.json')

var subscriptionName = subscription().displayName
var pnnlVnetName = '${subscriptionName}-${location}_VNET'
var pnnlSubnetName = 'private-2'
var pnnlVnetRGName = '${subscriptionName}_Restricted'

var openai_name = toLower('${name}ai${resourceToken}')
var webapp_name = toLower('${name}-webapp-${resourceToken}')
var appservice_name = toLower('${name}-app-${resourceToken}')
var stripped_name = replace(name, '-', '')
var short_prefix = take(stripped_name, 7)
var keyVaultName = toLower('${short_prefix}-kv-${resourceToken}')
var webhookName = toLower('webapp${name}webapp${resourceToken}')
var openai_name_2 = toLower('${short_prefix}ai2${resourceToken}')

var dockerImageNameAndTag = '${dockerImageName}/${dockerImageName}:latest'
var latestImage = '${containerRegistryEndpoint}/${dockerImageNameAndTag}' ?? 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
var linux_fx_version = 'DOCKER|${latestImage}'

var allowed_audience = 'api://${authClientId}'

var keyVaultSecretsUserRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
var containerRegistryAcrPullRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
var proxyBaseUrl = (name == 'aiendpointdev' ? 'https://ai-incubator-dev-api.pnnl.gov/' : name == 'aiendpointprod' ? 'https://ai-incubator-api.pnnl.gov/' : 'https://${webapp_name}.azurewebsites.net/')


resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appservice_name
  location: location
  tags: tags
  properties: {
    reserved: true
  }
  sku: {
    name: 'B1'
    tier: 'Basic'
    size: 'B1'
    family: 'B'
    capacity: 1
  }
  kind: 'linux'
}

// Reference the existing virtual network in another subscription and resource group
resource existingAppGWVnet 'Microsoft.Network/virtualNetworks@2021-02-01' existing = {
  name: appGWVNetName
  scope: resourceGroup(appGWSubscriptionId, appGWRGName)
}
// Reference the existing subnet
resource existingAppGWSubnet 'Microsoft.Network/virtualNetworks/subnets@2021-02-01' existing = {
  parent: existingAppGWVnet
  name: 'default'
}

resource existingPNNLVnet 'Microsoft.Network/virtualNetworks@2021-02-01' existing = {
  name: pnnlVnetName
  scope: resourceGroup(pnnlVnetRGName)
}

resource existingPNNLSubnet 'Microsoft.Network/virtualNetworks/subnets@2021-02-01' existing = {
  parent: existingPNNLVnet
  name: pnnlSubnetName
}

// // Create a virtual network for the web app
// resource webAppVnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
//   name: '${abbrs.networkVirtualNetworks}${resourceToken}'
//   location: location
//   properties: {
//     addressSpace: {
//       addressPrefixes: [
//         '10.0.0.0/16'
//       ]
//     }
//     subnets: [
//       {
//         name: '${abbrs.networkVirtualNetworksSubnets}${resourceToken}'
//         properties: {
//           addressPrefix: '10.0.0.0/24'
//           // privateEndpointNetworkPolicies: 'Disabled'
//           // privateLinkServiceNetworkPolicies: 'Enabled'
//           delegations: [
//             {
//               name: 'Microsoft.Web.hostingEnvironments'
//               properties: {
//                 serviceName: 'Microsoft.Web/serverFarms'
//               }
//             }
//           ]
//           serviceEndpoints: [
//             {
//               service: 'Microsoft.SQL'
//             }
//           ]
//         }
//       }
//     ]
//   }
// }



resource postgresDB 'Microsoft.DBforPostgreSQL/flexibleServers@2023-12-01-preview' = {
  location: location
  tags: {}
  name: '${abbrs.dBforPostgreSQLServers}${resourceToken}'
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    replica: {
      role: 'Primary'
    }
    storage: {
      type: ''
      iops: 120
      tier: 'P4'
      storageSizeGB: 32
      autoGrow: 'Disabled'
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
    dataEncryption: {
      type: 'SystemManaged'
    }
    authConfig: {
      activeDirectoryAuth: 'Disabled'
      passwordAuth: 'Enabled'
    }
    version: '16'
    administratorLogin: 'pgadmin'
    administratorLoginPassword: postgresDbPassword
    availabilityZone: '1'
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    maintenanceWindow: {
      customWindow: 'Disabled'
      dayOfWeek: 0
      startHour: 0
      startMinute: 0
    }
    replicationRole: 'Primary'
  }
}

resource firewall 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-12-01-preview' = {
  parent: postgresDB
  name: 'Jason'
  properties: {
    startIpAddress: '35.135.110.15'
    endIpAddress: '35.135.110.15'
  }
}

resource allowAllWindowsAzureIps 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-12-01-preview' = {
  name: 'AllowAllWindowsAzureIps' // don't change the name
  parent: postgresDB
  properties: {
    endIpAddress: '0.0.0.0'
    startIpAddress: '0.0.0.0'
  }
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webapp_name
  kind: 'app,linux,container'
  location: location
  tags: union(tags, { 'azd-service-name': 'ai-endpoint-api' })
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    // virtualNetworkSubnetId: existingPNNLSubnet.id // This is being blocked by C&DO's new policies so must be done manually by one of their engineers
    siteConfig: {
      httpLoggingEnabled: true
      linuxFxVersion: linux_fx_version
      alwaysOn: true
      appCommandLine: null
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      acrUseManagedIdentityCreds: true
      appSettings: [
        {
          name: 'DATABASE_URL'
          value:'@Microsoft.KeyVault(VaultName=${kv.name};SecretName=${kv::POSTGRES_DB_URL.name})'
        }
        {
          name: 'STORE_MODEL_IN_DB'
          value: 'True'
        }
        {
          name: 'LITELLM_MASTER_KEY'
          value: '@Microsoft.KeyVault(VaultName=${kv.name};SecretName=${kv::LITELLM_MASTER_KEY.name})'
        }
        {
          name: 'MICROSOFT_TENANT'
          value: 'd6faa5f9-0ae2-4033-8c01-30048a38deeb'
        }
        {
          name: 'MICROSOFT_CLIENT_ID'
          value: authClientId
        }
        {
          name: 'MICROSOFT_CLIENT_SECRET'
          value: authSecret
        }
        {
          name: 'DOCKER_ENABLE_CI'
          value: 'true'
        }
        {
          name: 'WEBSITE_HTTPLOGGING_RETENTION_DAYS'
          value: '30'
        }
        {
          name: 'PROXY_BASE_URL'
          value: proxyBaseUrl
        }
        {
          name: 'PROXY_ADMIN_ID'
          value: '355ca704-e3ca-4478-a9b8-2221253b4af1'
        }
        {
          name: 'DISABLE_FALLBACK_LOGIN'
          value: 'true'
        }
      ]
      ipSecurityRestrictionsDefaultAction: 'Deny'
      ipSecurityRestrictions: [
        {
          vnetSubnetResourceId: existingAppGWSubnet.id
          action: 'Allow'
          priority: 300
          name: 'AppGW Subnet'
        }
      ]
      scmIpSecurityRestrictionsDefaultAction: 'Deny'
      scmIpSecurityRestrictions: [
        {
          ipAddress: '130.20.0.0/16'
          action: 'Allow'
          priority: 300
          name: 'PNNL'
        }
        {
          ipAddress: '44.228.229.0/32'
          action: 'Allow'
          priority: 301
          name: 'AWS1'
        }
        {
          ipAddress: '44.241.229.120/32'
          action: 'Allow'
          priority: 302
          name: 'AWS2'
        }
        {
          ipAddress: '35.135.110.15/32'
          action: 'Allow'
          priority: 400
          name: 'Jason'
        }
        {
          ipAddress: 'AzureContainerRegistry'
          tag: 'ServiceTag'
          action: 'Allow'
          priority: 303
          name: 'ACR'
        }
      ]
    }
  }
  identity: { type: 'SystemAssigned'}
}


// resource authSettings 'Microsoft.Web/sites/config@2022-09-01' = {
//   name: 'authsettingsV2'
//   parent: webApp
//   properties: {
//     globalValidation: {
//       redirectToProvider: 'azureactivedirectory'
//       requireAuthentication: true
//       unauthenticatedClientAction: 'RedirectToLoginPage'
//     }
//     httpSettings: {
//       routes: {
//         apiPrefix: '/.auth'
//       }
//     }
//     identityProviders: {
//       azureActiveDirectory: {
//         enabled: true
//         isAutoProvisioned: true
//         registration: {
//           clientId: authClientId
//           clientSecretCertificateIssuer: 'https://sts.windows.net/d6faa5f9-0ae2-4033-8c01-30048a38deeb/v2.0'
//           clientSecretSettingName: 'MICROSOFT_PROVIDER_AUTHENTICATION_SECRET'
//           openIdIssuer: 'https://sts.windows.net/d6faa5f9-0ae2-4033-8c01-30048a38deeb/v2.0'
//         }
//         validation: {
//           allowedAudiences: [
//             allowed_audience
//           ]
//           defaultAuthorizationPolicy:{
//             allowedApplications: [
//               authClientId
//             ]
//           }
//           jwtClaimChecks: {
//             allowedClientApplications: [
//               authClientId
//             ]
//           }
//         }
//       }
//     }
//     login: {
//       tokenStore: {
//         enabled: true
//         tokenRefreshExtensionHours: 72
//       }
//     }
//   }
  
// }


resource kvAppPermissions 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(kv.id, webApp.name, keyVaultSecretsUserRole)
  scope: kv
  properties: {
    principalId: webApp.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: keyVaultSecretsUserRole
  }
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-06-01-preview' existing = {
  name: containerRegistryName
}

// This should work but doesn't for some reason so instead we use the code below
// resource publishingcreds 'Microsoft.Web/sites/config@2023-12-01' existing = {
//   name: publishingcredentials
//   parent: webApp
// }
// var webhookUri = publishingcreds.list().properties.scmUri


var webhookUri = '${list(resourceId('Microsoft.Web/sites/config', webapp_name, 'publishingcredentials'), '2023-12-01').properties.scmUri}/api/registry/webhook'

resource webhook 'Microsoft.ContainerRegistry/registries/webhooks@2023-11-01-preview' = {
  name: webhookName
  parent: containerRegistry
  location: location
  properties: {
    status: 'enabled'
    scope: dockerImageNameAndTag
    actions: [
      'push'
    ]
    serviceUri: webhookUri
  }
}

resource registryAppPermissions 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(containerRegistry.id, webApp.name, 'AcrPull')
  scope: containerRegistry
  properties: {
    principalId: webApp.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: containerRegistryAcrPullRole
  }
}

var postgresDbUrl = 'postgresql://pgadmin:${postgresDbPassword}@${postgresDB.properties.fullyQualifiedDomainName}:5432/postgres'

resource kv 'Microsoft.KeyVault/vaults@2021-06-01-preview' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enabledForDeployment: false
    enabledForDiskEncryption: true
    enabledForTemplateDeployment: false
  }

  resource POSTGRES_DB_URL 'secrets' = {
    name: 'POSTGRES-DB-URL'
    properties: {
      contentType: 'text/plain'
      value: postgresDbUrl
    }
  }

  resource LITELLM_MASTER_KEY 'secrets' = {
    name: 'LITELLM-MASTER-KEY'
    properties: {
      contentType: 'text/plain'
      value: liteLLMMasterKey
    }
  }

}

resource azureopenai 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: openai_name
  location: openAiResourceGroupLocation
  tags: tags
  kind: 'OpenAI'
  properties: {
    customSubDomainName: openai_name
    publicNetworkAccess: 'Enabled'
  }
  sku: {
    name: openAiSkuName
  }
}

resource gpt4odeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: azureopenai
  name: gpt4oDeploymentName
  properties: {
    model: {
      format: 'OpenAI'
      name: gpt4oModelName
      version: gpt4oModelVersion
    }
    raiPolicyName: null
    dynamicThrottlingEnabled: true
  }
  sku: {
    name: 'Standard'
    capacity: gpt4oDeploymentCapacity
  }
}

resource embeddingdeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  dependsOn: [
    gpt4odeployment
  ]
  parent: azureopenai
  name: embeddingDeploymentName
  properties: {
    model: {
      format: 'OpenAI'
      name: embeddingModelName
      version: '2'
    }
    raiPolicyName: null
    dynamicThrottlingEnabled: true
  }
  sku: {
    name: 'Standard'
    capacity: embeddingDeploymentCapacity
  }
}

resource azureopenai2 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: openai_name_2
  location: openAI2ResourceGroupLocation
  tags: tags
  kind: 'OpenAI'
  properties: {
    customSubDomainName: openai_name_2
    publicNetworkAccess: 'Enabled'
  }
  sku: {
    name: openAiSkuName
  }
}

resource gpt35deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: azureopenai2
  name: gpt35DeploymentName
  properties: {
    model: {
      format: 'OpenAI'
      name: gpt35ModelName
      version: gpt35ModelVersion
    }
    raiPolicyName: null
    dynamicThrottlingEnabled: true
  }
  sku: {
    name: 'Standard'
    capacity: gpt35DeploymentCapacity
  }
}

output url string = 'https://${webApp.properties.defaultHostName}'
