#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import *

try:
    from zabbix.api import ZabbixAPI
    HAS_ZABBIX_API = True
except ImportError:
    HAS_ZABBIX_API = False
DOCUMENTATION = '''
---
module: zabbix
short_description: ansible wrapper for py-zabbix
description:
    - This module uses the Zabbix API to make requests to zabbix server.
version_added: "1.9"
requirements: [ 'py-zabbix' ]
options:
    object:
        description:
            - The object to which the action applies. E.g item, host etc.
        required: false
        required: true
        default: null
    action:
        description:
            - Api methods: get, create, update, delete.
        required: true
        default: null
    params:
        description:
            - Request parameters.
        required: true
        default: null
    server:
        description:
            - Url of Zabbix server, with protocol (http or https) e.g.
              https://monitoring.example.com/zabbix.
        required: true
        default: null
    login:
        description:
            - Zabbix user name.
        required: true
        default: null
    password:
        description:
            - Zabbix user password.
        required: true
notes:
    - The module has been tested with Zabbix Server 2.4.
    - all requests set ansible fact called 'response' which contains zabbix api answer
    - Zabbix 2.4 Api reference: https://www.zabbix.com/documentation/2.4/manual/api
author: Flashick <flashick@gmail.com>
'''

EXAMPLES = '''
# get groupid by name

- name: hostgroup name to groupid
  zabbix:
    server: 'https://zabbix-server.example.com'
    login: 'api_user'
    password: 'api_user_password'
    action: 'get'
    object: 'hostgroup'
    params:
      filter:
        name:
         - "My favorite host group"
- set_fact:
    groupid: "{{ response.result[0].groupid }}"

# create new host in group 'My favorite host group'

- name: add new hosts
  zabbix:
    server: 'https://zabbix-server.example.com'
    login: 'api_user'
    password: 'api_user_password'
    action: 'create'
    object: 'host'
    params:
       host: 'Sample host'
       groups:
         - groupid:  "{{ groupid }}"
       templates:
         - templateid: 5
       interfaces:
        - type: 1
          main: 1
          useip: 1
          ip: "127.0.0.1"
          port: 10050
          dns: ""

# get all hosts in group 'My favorite host group'

- name: get existing hosts
  zabbix:
    server: 'https://zabbix-server.example.com'
    login: 'api_user'
    password: 'api_user_password'
    action: 'get'
    object: 'host'
    params:
      groupids: "{{ groupid }}"
- set_fact:
    host_list: "{{ response.result }}"

# delete all hosts in group 'My favorite host group'
- name: delete hosts
  zabbix:
    server: 'https://zabbix-server.example.com'
    login: 'api_user'
    password: 'api_user_password'
    action: 'delete'
    object: 'host'
    params:
      - "{{ item.hostid }}"
   with_items: "{{ host_list }}"
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            server=dict(default=None),
            login=dict(default=None),
            password=dict(default=None),
            action=dict(default=None, required=True),
            object=dict(default=None, required=True),
            params=dict(default=None),
        )
    )

    if not HAS_ZABBIX_API:
        module.fail_json(msg='Missing requried py-zabbix module (check docs or install with: pip install py-zabbix)')

    try:
        action = module.params['action']
    except KeyError, e:
        module.fail_json(msg='Missing actions data: %s is not set.' % e.message)

    try:
        login = module.params['login']
        password = module.params['password']
        server = module.params['server']
    except KeyError, e:
        module.fail_json(msg='Missing login data: %s is not set.' % e.message)

    try:
        zabbix_object = module.params['object']
        params = module.params['params']
    except KeyError, e:
        module.fail_json(msg='Missing actions data: %s is not set.' % e.message)

    try:
        zapi = ZabbixAPI(url=server, user=login, password=password)
    except BaseException as e:
        module.fail_json(msg='Authentication error: %s' % e)

    try:
        request = zapi.do_request(zabbix_object + '.' + action, params)
    except BaseException as e:
        module.fail_json(msg='Request error: %s ' % e)

    module.exit_json(changed=1, ansible_facts={'response': request})

main()

