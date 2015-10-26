# ansible-zabbix
[Ansible][src_ansible] wrapper for py-zabbix

This module uses the Zabbix API to make requests to zabbix server.

# Requirements
Python module ``py-zabbix``, install with ``pip install py-zabbix``
[src_ansible]: https://github.com/ansible/ansible

# Notes
* The module has been tested with Zabbix Server 2.4.
* All requests set ansible fact called 'response' which contains zabbix api answer
* Zabbix 2.4 API reference: https://www.zabbix.com/documentation/2.4/manual/api

# Examples

Get groupid by name
```yaml
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
```
Create new host in group 'My favorite host group'
```yaml
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
```
Get all hosts in group 'My favorite host group'
```yaml
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
```
Delete all hosts in group 'My favorite host group'
```yaml
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
```
