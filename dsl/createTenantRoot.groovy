import groovy.transform.Field

Map mergeMaps(Map lhs, Map rhs) {
    // Shallow copy so we dont modify the data of the arguments
    Map result = lhs.getClass().newInstance(lhs)
    rhs.each { k, v ->
        result[k] = (lhs[k] in Map ? mergeMaps(result[k], v) : v)
    }
    return result
}

def buildPermissionMatrix(Map jenkinsRoleMap, Map ldapRoleMap) {
    def result = []

    // Build a list in the format jenkins expects for a permission matrix plugin. Ex: GROUP:<Jenkins Permission>:<Ldap Group>
    ldapRoleMap.each { curRoleName, curLdapGroup ->
        def jenkinsPermissionList = jenkinsRoleMap.get(curRoleName)
        if (jenkinsPermissionList != null) {
            jenkinsPermissionList.each { curJenkinsPerm ->
                result.add("GROUP:${curJenkinsPerm}:${curLdapGroup}")
            }
        }
    }
    return result
}

def createTenantFolder(String tenantKey, Map tenantConfig) {
    def tenantVars = tenantConfig.get('vars')
    def folderPath = "${pathPrefix}/${tenantKey}"
    def tenantDisplayName = tenantVars.get('display_name')

    def permissionMatrix = []
    folder(folderPath) {
        displayName(tenantDisplayName)

        properties {
            authorizationMatrix {
                inheritanceStrategy { nonInheriting() }
                permissions(permissionMatrix)
            }
            folderProperties {
                properties {
                    stringProperty {
                        key('TENANT')
                        value('tenantKey')
                    }
                }
            }
        }
    }

}


boolean main()
{
    try {
        def tenants = configYaml.get('tenants')
        if (tenants != null) {
            def commonConfig = tenants.get('common')

            tenants.each { tenantKey, tenantConfig ->
                if (tenantKey != 'common') {
                    Map mergedConfig = mergeMaps(commonConfig, tenantConfig)
                    println("Merged Config: ${mergedConfig}")
                    createTenantFolder(tenantKey, mergedConfig)
                }
            }
        }
    } catch (Exception ex) {
        println("Exception: ${ex.toString()}")
        return false
    }
    return true
}

boolean result = main()
if (result == false)
{
    throw new Exception("createTenantRoot.groovy - Execution FAILURE")
}




