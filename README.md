## Overview
This is an ansible playbook for creating config files from templates.  

Currently this playbook creates four (abbreviated) Juniper Network SRX config files, but given a different template, could create anything.

## Usage
First, delete the four config files in roles/confgen2/configs - these will be re-created when you run the playbook.
Type 'ansible-playbook confgen2.yml' to run the playbook
See the four files re-appear

## Other info
The template is a Jinja2 formatted file:
`confgen/roles/confgen2/templates/srx-template.j2`

The variables are in confgen/roles/confgen2/vars/main.yml

To modify this for your own purposes, do this:

Edit the template:  ansible/roles/confgen2/templates/srx-teplate.j2
Put your variables in curly brackets in the format {{ item.VARIABLENAME }}

Edit the variables file:  ansible/roles/confgen2/vars/main.yml
For each config to be generated, there needs to be a line starting with a hyphen under srx_configs
The curly brackets enclose a 'dictionary' of variables, referenced by variable name. 
Variable name and value are separated by a colon
Variable name/value pairs are separated by commas
Make sure the variable names agree with what your template has in it
