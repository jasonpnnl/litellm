targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string
@secure()
param authSecret string
param authClientId string

param resourceGroupName string = ''
param dockerImageName string = 'litellmdevapp'
param openAILocation string = 'eastus2'
param openAISku string = 'S0'
param gpt4oDeploymentCapacity int = 200
param gpt4oDeploymentName string = 'gpt-4o'
param gpt4oModelName string = 'gpt-4o'
param gpt4oModelVersion string = '2024-05-13'
param gpt35DeploymentCapacity int = (environmentName == 'aiendpointprod') ? 200 : 50
param gpt35DeploymentName string = 'gpt-35-turbo'
param gpt35ModelName string = 'gpt-35-turbo'
param gpt35ModelVersion string = '0125'
param openAI2ResourceGroupLocation string = 'northcentralus'
param embeddingDeploymentName string = 'embedding'
param embeddingDeploymentCapacity int = 100
param embeddingModelName string = 'text-embedding-ada-002'

@secure()
param liteLLMMasterKey string
@secure()
param postgresDbPassword string

param appGWSubscriptionId string = '9e44d5e3-fcdd-4192-98fe-feb9e7748478'
param appGWVNetName string = 'aiexploration2-westus_VNET'
param appGWRGName string = 'aiexploration2_Restricted'

// Tags that should be applied to all resources.
// 
// Note that 'azd-service-name' tags should be applied separately to service host resources.
// Example usage:
//   tags: union(tags, { 'azd-service-name': <service name in azure.yaml> })
var tags = {
  'azd-env-name': environmentName
}

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : 'rg-${environmentName}'
  location: location
  tags: tags
}

module registry './shared/registry.bicep' = {
  name: 'registry'
  params: {
    location: location
    tags: tags
    name: '${abbrs.containerRegistryRegistries}${resourceToken}'
  }
  scope: rg
}

module resources 'resources.bicep' = {
  name: 'all-resources'
  scope: rg
  params: {
    name: environmentName
    resourceToken: resourceToken
    tags: tags
    openAiResourceGroupLocation: openAILocation
    openAiSkuName: openAISku
    gpt4oDeploymentCapacity: gpt4oDeploymentCapacity
    gpt4oDeploymentName: gpt4oDeploymentName
    gpt4oModelName: gpt4oModelName
    gpt4oModelVersion: gpt4oModelVersion
    gpt35DeploymentCapacity: gpt35DeploymentCapacity
    gpt35DeploymentName: gpt35DeploymentName
    gpt35ModelName: gpt35ModelName
    gpt35ModelVersion: gpt35ModelVersion
    openAI2ResourceGroupLocation: openAI2ResourceGroupLocation
    embeddingDeploymentName: embeddingDeploymentName
    embeddingDeploymentCapacity: embeddingDeploymentCapacity
    embeddingModelName: embeddingModelName
    location: location
    authSecret: authSecret
    authClientId: authClientId
    containerRegistryEndpoint: registry.outputs.loginServer
    containerRegistryName: registry.outputs.name
    dockerImageName: dockerImageName
    appGWSubscriptionId: appGWSubscriptionId
    appGWVNetName: appGWVNetName
    appGWRGName: appGWRGName
    liteLLMMasterKey: liteLLMMasterKey
    postgresDbPassword: postgresDbPassword
  }
}


output AZURE_CONTAINER_REGISTRY_ENDPOINT string = registry.outputs.loginServer
