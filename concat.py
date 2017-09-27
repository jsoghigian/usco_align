#!/usr/bin/python

#concat.py must be run from the parent directory of the USCO sequences and .tsv files, 
#that is, in the same directory in which cpdirs.sh was run!  Specify a presence threshold
#for USCOs by passing a proportion (0-1) to the script, e.g. concat.py 1 would only return
#USCOs in ALL genomes, while concat.py 0.75 would return USCOs in 75% of genomes.

import pandas as pd
import os
import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

to_merge = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".tsv"):
            files=os.path.join(root, file)
            print(files)
            to_merge.append(files)

dfs = []
#define the ortholog names
on = pd.read_csv(to_merge[1],sep='\t', header=None, skiprows=5)
on = on.drop_duplicates(subset=on.loc[:,0:1])
on = on.ix[:,0]
on = on.reset_index(drop=True)
dfs.append(on)

#now loop over merged files
for filename in to_merge:
    # read the csv
    df = pd.read_csv(filename,sep='\t', header=None,skiprows=5)
    df = df.drop_duplicates(subset=df.loc[:,0:1])
    df = df.reset_index(drop=True)
    # keep only the second column (which contains the records)
    df = df.ix[:,1:1]
    # change the column names so they won't collide during concatenation
    df.columns = [filename + str(cname) for cname in df.columns]
    dfs.append(df)
threshold = float(sys.argv[1])
# concatenate them horizontally
merged = pd.concat(dfs,axis=1)
# the merged csv - will be large!
merged.to_csv("merged.csv", header=None, index=None)
#set the USCO to be thei ndex
merged2=merged.set_index([0])
#transpose so index is column
merged3=merged2.T
#melt for grouping
merged4 = pd.melt(merged3)
#discard anything that isn't complete
merged5 = merged4[merged4['value'].str.contains("Complete")]
#each usco with number of genomes in which it is present
merged6 = merged5.groupby(by=[0])['value'].count()
#make the number a proportion
tots=len(to_merge)
merged7 = merged6[:]/tots
#Plot a histogram of USCO presence; save it as a png, then
#write a CSV with the same information. 
plt.hist(merged7, bins=10)
plt.xlabel('Proportion of Genomes with an Ortholog')
plt.ylabel('Number of orthologs')
plt.title(r'Ortholog presence in genomes')
plt.savefig('usco_presence.png')
merged7.to_csv("uscos_presence.csv", header=None, index=None)
#select uscos that exceed THRESHOLD
thresh=(merged7 >= threshold )
thresh_scos=thresh[thresh].index.values.tolist()
#write uscos that pass THRESHOLD to a list
f = open("threshold_uscos.txt", "w")
f.write("\n".join(str(x) for x in thresh_scos))
f.close()