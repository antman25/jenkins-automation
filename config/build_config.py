#!/usr/bin/env python3
import yaml
import sys
import re

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

KEY_TENANTS='tenants'
KEY_COMMON='common'
KEY_UTILITIES='utilities'
KEY_SANDBOX='sandbox'
KEY_JOBS='jobs'
KEY_VARS='vars'

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

def createCommon(config):
    setTenantVar(config, 'common', 'bitbucket_url', 'http://10.0.0.35')

def main():
    try:
        output_path = 'config/config.yaml'
        output_config = {}

        createCommon(output_config)

        with open('config/config.yaml', 'w') as f:
            yaml.dump(output_config, f, Dumper=NoAliasDumper,sort_keys=False)
    except:
        print('Error building config')
        sys.exit(1)


if __name__ == '__main__':
    main()
    sys.exit(0)