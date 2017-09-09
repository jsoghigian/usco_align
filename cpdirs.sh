#!/bin/bash
#Input file should be specified as a list of directories... PATHS SHOULD NOT HAVE A TRAILING / ... e.g. :
#
#/my/path/to/busco/run_results1
#/my/path/to/busco/run_results2
#This scrpt file must have execute permissions, of course!
for sample in `cat $1`
    do
    #create directory to store single copy orthologs:
    base=$(printf $sample | sed 's/.*\(run\)/\1/g')
    mkdir ${base}
    cp ${sample}/single_copy_busco_sequences/*.fna ${base}
    cp ${sample}/full_table_*.tsv ${base}
done