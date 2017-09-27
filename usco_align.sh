#!/bin/bash
#Input var1 should be the set of directories (used for cpdirs.sh earlier).

mkdir uscos
mkdir uscos/aligns
mkdir uscos/aligns/aligns_raw
mkdir uscos/aligns/aligns_trim
mkdir uscos/aligns/reports
for usco in `cat threshold_uscos.txt`
    do
    usco_name=$(basename $usco ".fna")
    mkdir uscos/${usco}
    for sample in `cat $1`
        do
        base=$(printf $sample | sed 's/.*\(run\)/\1/g')
        cp ${sample}/single_copy_busco_sequences/${usco}.fna uscos/${usco}/${base}_${usco}
        cd uscos/${usco}
        sed -i "1s/.*/>${base}/" ${base}_${usco}
        cd ../..
        done
            cd uscos/${usco}
    cat * > ${usco}.fa
    /ycga-gpfs/home/js3633/mafft-7.310/scripts/mafft --auto ${usco}.fa > ../aligns/aligns_raw/${usco}.fna
    /ycga-gpfs/home/js3633/trimAl/source/trimal -in ../aligns/aligns_raw/${usco}.fna -out ../aligns/aligns_trim/${usco}_trim.fna -htmlout ../aligns/reports/${usco}.html -automated1
    cd ../..
done
