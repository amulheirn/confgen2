# Overview
This project is a way of creating lots of config files from a Jinja2 template.

Once a template is created, variables are gathered for the devices in an Excel spreadsheet. This is turned into  YAML by a python script.  Once that is complete, the Ansible playbook reads the variables and the template, and produces config files.

Currently it creates three (abbreviated) Juniper Network router config files, but given a different template could create anything.

# Usage

## Device Template
Before doing anything else, you need to create a Jinja2-formatted device template.  This is a just a configuration file from whatever you are working on, but with all the variables replaced by `{{ item.VARIABLENAME }}`.  There is an example supplied in the `roles/confgen2/templates/router-template.j2` that should work for you and serve as a basis for your own template.  It is a Junos config.

## Variable gathering
Once the template is defined, you need to gather the variables for each device, such as hostname, IP addresses and so on.  You may need to ask for this information from a customer, so it is easiest to do this in an Excel spreadsheet.

**NOTE: make sure all your variable names are in lowercase, and use only underscores as a separator.  Using hyphens is not supported by Ansible.**

- Open the source-variables.xlsx
- Create headings in row 1 for each of your variables specified in the template
- Fill in device 1's variable values in line 2
- Fill in device 2's variable values in line 3 and carry on
- When complete, save the file as source-variables.csv

## Conversion to YAML
The Ansible playbook needs the variables in YAML, so a Python script is included to convert the CSV file you just generated into that format.

Run it using `python csv2yaml.py` - the result is output to the screen, and also put in `roles/confgen2/vars/main.yml` for the next stage.

## Generating Config Files

We are now about to generate config files:

- First, delete the supplied config files in the `configs` directory - these will be re-created when you run the playbook.
- Type 'ansible-playbook confgen2.yml' to run the playbook.
- See the files re-appear.

## Other info
This playbook operates locally on the script host - it does not push a config out to a device.
The confgen.yml playbook simply calls a role called `confgen2` and runs it against all hosts in the `hosts` file.

The tasks for the confgen2 role are in `roles/confgen2/tasks/main.yml`.  This reads in the source template, and writes a `hostname.cfg` config file for each line in under `srx_configs` in the variables file.

The template is a Jinja2 formatted file:  `roles/confgen2/templates/router-template.j2`

The variables are in `roles/confgen2/vars/main.yml`

Hopefully the python script will be sufficient for your needs, but to manually modify this for your own purposes, do this:

Edit the template:  `roles/confgen2/templates/router-teplate.j2`
Put your variables in curly brackets in the format `{{ item.VARIABLENAME }}`

Edit the variables file:  `roles/confgen2/vars/main.yml`
For each config to be generated, there needs to be a line starting with a hyphen under `config_parameters`
The curly brackets enclose a 'dictionary' of variables, referenced by variable name.
Variable name and value are separated by a colon.
Variable name/value pairs are separated by commas.
Make sure the variable names agree with what your template has in it.
