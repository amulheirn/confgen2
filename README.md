# Overview
This project is a way of creating lots of config files from a Jinja2 template
using a python script and an Ansible playbook.  The process is:


1. Write template with variables in place of IP addresses (for example)
2. Gather variable values for the devices in an Excel spreadsheet
3. Turn this into YAML using a python script
4. Run the Ansible playbook to read the variables and the template, and produce
config files.
5. Add more csv files and templates and repeat.

Currently it creates seven (abbreviated) Juniper Network config files
(three "routers" and four "srx") but given a different template could create
anything.

# Usage

## Device Template
Before doing anything else, you need to create at least one Jinja2-formatted
device template.  This is a just a configuration file from whatever you are
working on, but with all the variables replaced by `{{ item.VARIABLENAME }}`.
There is a couple of examples supplied in the
`roles/confgen2/templates/` directory
that should work for you and serve as a basis for your own template.  Both are
for Junos config.

## Variable gathering
Once the template(s) are defined, you need to gather the variables for each
device, such as hostname, IP addresses and so on.  You may need to ask for this
information from a customer, so it is easiest to do this in an Excel
spreadsheet.

**NOTE: make sure all your variable names are in lowercase, and use only
underscores as a separator.  Using hyphens is not supported by Ansible.**

- Open the file `roles/confgen2/data/variables.xlsx`
- Create headings in row 1 for each of your variables specified in the template
- Fill in device 1's variable values in line 2
- Fill in device 2's variable values in line 3 and carry on
- If you have multiple Jinja2 templates, repeat the process across multiple
tabs. Each tab can have different headings to match the template.
- When complete, save each tab as a `-variables.csv` file.

## Conversion to YAML
The Ansible playbook needs the variables in YAML, so a Python script is included
to convert the CSV file you just generated into that format.

Run it using csv2yaml.py as follows to create roles/confgen/vars/main.yml
required for the next stage.
    `python csv2yaml.py -i roles/confgen2/data/*.csv  -o roles/confgen2/vars/main.yml`

## Generating Config Files

We are now about to generate config files:

- First, delete the supplied config files in the `roles/confgen2/configs/*`
directories - these will be re-created when you run the playbook.
- Type 'ansible-playbook confgen2.yml' to run the playbook.
- See the files re-appear.

## Other info
This playbook operates locally on the script host - it does not push a config
out to a device.
The confgen.yml playbook simply calls a role called `confgen2` and runs it against all hosts in the `hosts` file.

The tasks for the confgen2 role are in `roles/confgen2/tasks/main.yml`.  This
reads in the source template, and writes a `hostname.cfg` config file for each
line in under `srx_configs` in the variables file.  If you add new CSV files and
Jinja2  templates it'll be necessary to edit this file to add new tasks.

The templates are Jinja2 formatted files in `roles/confgen2/templates/`:
- `router-template.j2`
- `srx-template.j2`

The variables are in `roles/confgen2/vars/main.yml`

Hopefully the python script will be sufficient for your needs, run with the
"-h" argument for help:

    `$ python csv2yaml.py -h
    usage: csv2yaml.py [-h] [-o [outFile]] [-i [inFile [inFile ...]]] [-debug]

    Takes one or more CSV files, each containing device parameters, and turns them
    into YAML for use by Ansible/Jinja2 config generation process.

    optional arguments:
      -h, --help            show this help message and exit
      -o [outFile]          YAML file to write to
      -i [inFile [inFile ...]]
                            CSV file(s) to read from
      -debug                Enable Debug Mode

    This software is provided with no warranty. Based on work by Andrew Mulheirn.
    https://github.com/amulheirn/confgen2`

This file will convert each csv file provided as input to a YAML dictionary,
with each dictionary getting its name from the originating csv filename.
Any hyphens in the csv filename are converted to underscores in the dictionary
name.  The `outFile` and `inFile` variables default to stdin and stdout
respectively, however reading from stdin is problematic.

