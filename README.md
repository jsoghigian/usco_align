# Universal Single Copy Ortholog Aligner
This is a series of scripts that will accept BUSCO results directories and output a multisequence alignment (MSA) representing all orthologs present in some threshold of genomes.  The script leverages the OrthoDB catalogs and BUSCO analyses.

Future iterations will optionally trim MSAs.

Dependencies:   
BUSCO (or the results directories from BUSCO)    
MAFFT  
Python 2.7
    Biopython
    Matplotlib  
## Description of each script  
In order of use, I provide a short description of each script.  

### cpdirs.sh
Copies universal single copy orthologs from each BUSCO results directory provided in input.txt
Basic usage: cpdirs.sh input.txt  
  
### concat.py  
Determines single copy orthologs present in a genome beyond some user specified threshold.  
Basic usage: python concat.py 0.90  
  
### usco_align.sh  
Aligns single copy orthologs passing the threshold specified in concat.py with MAFFT.  Must include the original input.txt file from cpdirs.sh.  MAFFT installation location must be specified (or inherited from environment)
Basic usage: usco_align.sh  
  
### nex_fna.py 
Utilized Biopython modules to concetnate ortholog alignments into a multisequence alignment, outputting both nexus and phylip files.
Basic usage: python nex_fa.py  
  
### part_converter.sh 
A script that extracts partition information from a nexus file charset with sed.
Basic usage: part_converter.sh COMBINED.nex  
  
## An Example USCO ALIGN Run
An example run of the scripts is below:  

#these scripts require Biopython and matplotlib, along with a *NIX operating system.  Of course  
#they also rely on BUSCO results directories!  
#cpdirs copies single copy orthologs and the tsv of ortholog presence/absence from the results   
#directories defined in sets_r.txt .  These results directories should be presented as below,   
#without a trailing slash:  

#/my/path/to/busco/run_results1  
#/my/path/to/busco/run_results2  
  
./cpdirs.sh sets_r.txt  
  
#Outputs written: One directory for each genome, containing single copy orthologs and the tsv  
#that defines presence or absence of orthologs in the BUSCO catalog.  
  
#next we use concat.py to choose a set of orthologs that pass some threshold for inclusion in the msa.  
#concat.py must be run from the parent directory of the USCO sequences and .tsv files, that is, in the   
#same directory in which cpdirs.sh was run!  
  
#concat.py takes a single argument: the proportion of genomes in which a USCO must be present to be #returned.  
  
python concat.py 0.90  
  
#Outputs written:  
#merged.csv , A csv containing the concatenated BUSCO catalogs 
#usco_presence.png , a histogram of usco presence in the selected genomes. 
#threshold_uscos.txt , the list of uscos passing the specified threshold. 
  
#usco_align then aligns the set of uscos defined by concat.py with mafft. usco_align.sh will take the same input as cpdirs.  
#ADJUST MAFFT DIRECTORY IN THE SCRIPT!  
 
./usco_align.sh sets_r.txt  
  
#Outputs written: Alignments for each usco in fasta format (but with .phy extension)  

#Run a Python script to create the MSA, which is written both as a nexus file, and as a phylip file.  
  
python nex_fna.py  
  
#Outputs written:  
#Alignments for each USCO as .nex  
#COMBINED.nex , containing the concatenated MSA in nexus format with charset partitions  
#COMINBED.phy , containing the concatenated MSA in phylip format  
  
#run the final script to convert the nexus charset into a RAxML partition format, providing the input as the nexus file to convert:  
  
./part_converter.sh COMBINED.nex  
  
#Outputs written: raxml_partition.txt , containing partition information in RAxML format.  
