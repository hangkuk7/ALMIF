#!/bin/sh

export LC_ALL=en_US.utf8
source $IV_HOME/flexconf_venv/bin/activate

cd $IV_HOME/bin/scripts/ALMIF/
python3 ./almif_main.py ALMIF 

