This is an ansible playbook for creating config files from templates.

Type 'ansible-playbook confgen2.yml' to run the playbook


The template is a Jinja2 formatted file under confgen/roles/confgen2/templates
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
