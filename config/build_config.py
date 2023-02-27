#!/usr/bin/env python3
import yaml
import sys
import re

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

KEY_TENANTS='tenants'
KEY_COMMON='common'

KEY_JOBS='jobs'
KEY_VARS='vars'
KEY_BUILDS='builds'
KEY_ROLES='roles'
KEY_ROLE_LDAP_GROUP='role-ldap-map'

REGEX_MATCH_ALL=".*"
#REGEX_EXCLUDE_ALL="^(?!.*).*$"
REGEX_EXCLUDE_ALL="!.*$"
REGEX_ONLY_MAIN="^(.*main).*$"
REGEX_EXCLUDE_MAIN="^(?!.*main).*$"
# Regex notes
# ^(?:.*develop|.*master|.*release/\d+\.\d+\.\d+(?!.))$



TENANT_CRED_BITBUCKET_RW='tenant-bitbucket-rw-cred'
TENANT_CRED_BITBUCKET_RO='tenant-bitbucket-ro-cred'
TENANT_CRED_ARTIFACTORY_RW='tenant-artifactory-rw-cred'
TENANT_CRED_ARTIFACTORY_RO='tenant-artifactory-ro-cred'

TENANT_PIPELINE='Pipeline'
TENANT_GROUP_A="Group A"
TENANT_GROUP_B="Group B"
TENANT_GROUP_C="Group C"

JENKINS_PERM_READ = 'hudson.model.Item.Read'
JENKINS_PERM_BUILD = 'hudson.model.Item.Build'
JENKINS_PERM_CANCEL = 'hudson.model.Item.Cancel'

ROLE_READONLY = 'read-only'
ROLE_READONLY_PERMS = [ JENKINS_PERM_READ ]

ROLE_DEVELOPER = 'developer'
ROLE_DEVELOPER_PERMS = [ JENKINS_PERM_READ, JENKINS_PERM_BUILD, JENKINS_PERM_CANCEL ]

def slugify(value):
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def dump_config(config):
    for cur_key in config:
        print(f'\t{cur_key}={config[cur_key]}')

def setConfig(config, tenant_name, config_category, var_key, var_value):
    tenant_name_slug = slugify(tenant_name)
    if KEY_TENANTS not in config:
        config[KEY_TENANTS] = {}
    if tenant_name_slug not in config[KEY_TENANTS]:
        config[KEY_TENANTS][tenant_name_slug] = {}
    if config_category not in config[KEY_TENANTS][tenant_name_slug]:
        config[KEY_TENANTS][tenant_name_slug][config_category] = {}
    config[KEY_TENANTS][tenant_name_slug][config_category][var_key] = var_value

def setTenantVar(config, tenant_name, var_key, var_value):
    setConfig(config, tenant_name, KEY_VARS, var_key, var_value)


def templateBuildConfig(project_list, repo_filter='.*'):
    return { 'display_name' : 'Builds',
             'project_list' : project_list,
             'repo_filter' : repo_filter
            }

def setBuilds(config, tenant_name, project_list):
    tenant_name_slug = slugify(tenant_name)
    setConfig(config, tenant_name, KEY_BUILDS, 'display_name', "Builds")
    setConfig(config, tenant_name, KEY_BUILDS, 'project_list', project_list)
    setConfig(config, tenant_name, KEY_ROLE_LDAP_GROUP, ROLE_READONLY, f'jenkins-ro-{tenant_name_slug}')
    setConfig(config, tenant_name, KEY_ROLE_LDAP_GROUP, ROLE_DEVELOPER, f'jenkins-dev-{tenant_name_slug}')


def addTenant(config, tenant_name, project_list):
    setConfig(config, tenant_name, KEY_VARS, 'display_name', tenant_name)
    setBuilds(config, tenant_name, project_list)

def setCommon(config):
    setTenantVar(config, KEY_COMMON, 'bitbucket_url', 'http://10.0.0.35')
    setConfig(config, KEY_COMMON, KEY_ROLES, ROLE_READONLY, ROLE_READONLY_PERMS)
    setConfig(config, KEY_COMMON, KEY_ROLES, ROLE_DEVELOPER, ROLE_DEVELOPER_PERMS)

def createTenants(config):
    addTenant(config, TENANT_PIPELINE, ['PIP', 'PIPAPP'])
    addTenant(config, TENANT_GROUP_A, ['prjA'])
    addTenant(config, TENANT_GROUP_B, ['prjB'])
    addTenant(config, TENANT_GROUP_C, ['prjA','prjB','prjC'])


def main():
    #try:
        output_path = 'config/config.yaml'
        output_config = {}

        setCommon(output_config)
        createTenants(output_config)

        with open('config/config.yaml', 'w') as f:
            yaml.dump(output_config, f, Dumper=NoAliasDumper,sort_keys=False)
    #except Exception as ex:
    ##    print('Exception: %s' % ex)
    #    sys.exit(1)


if __name__ == '__main__':
    main()
    sys.exit(0)