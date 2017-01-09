# Takes a CSV file of device variables and turns it into YAML for use
# by Ansible/Jinja2 config generation process
#
# Andrew Mulheirn - Axians 2017
#
# This software is provided with no warranty

#!/usr/bin/python

__author__ = "Andrew Mulheirn"
__copyright__ = "Copyright 2016, Axians Networks Limited"
__version__ = "0.1"
__maintainer__ = "Andrew Mulheirn"
__email__ = "andrew.mulheirn@axians.co.uk"
__status__ = "Test"


import csv

# Open the file and read the contents in as dictionary

with open('source-variables.csv') as f:
    reader = csv.DictReader(f, dialect='excel')

    # Write the YAML version
    varfile = open('./roles/confgen2/vars/main.yml', 'w')
    print "---"
    varfile.write("---\n")
    print "config_parameters:"
    varfile.write("config_parameters:\n")
    try:
        for row in reader:
            varfile.write("  - { ",)
            print "  - { ",
            for item, value in row.iteritems():
                varfile.write("%s: %s, " % (item, value))
                print item, ": ", value, ",",
            varfile.write("}\n")
            print "}"
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (f, reader.line_num, e))
