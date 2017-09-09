#!/bin/bash
#Input file should be specified as a list of directories... PATHS SHOULD NOT HAVE A TRAILING / ... e.g. :
#
#/my/path/to/busco/run_results1
#/my/path/to/busco/run_results2
#This scrpt file must have execute permissions, of course!

sed -n '/sets/,/charpartition/{/sets/b;/charpartition/b;p}' $1 | sed 's/charset/LG,/g' | sed 's/;//' > raxml_partition.txt