param pnnlVnetName string
param pnnlSubnetName string

resource existingPNNLVnet 'Microsoft.Network/virtualNetworks@2021-02-01' existing = {
  name: pnnlVnetName
}

resource existingPNNLSubnet 'Microsoft.Network/virtualNetworks/subnets@2021-02-01' existing = {
  parent: existingPNNLVnet
  name: pnnlSubnetName
}

resource addDelegationToPNNLSubnet 'Microsoft.Network/virtualNetworks/subnets@2021-02-01' = {
  parent: existingPNNLVnet
  name: existingPNNLSubnet.name
  properties: {
    delegations: [
      {
        name: 'Microsoft.Web.hostingEnvironments'
        properties: {
          serviceName: 'Microsoft.Web/serverFarms'
        }
      }
    ]
  }
}

output subnetId string = existingPNNLSubnet.id
