#!/usr/bin/python
from Bio import AlignIO
from Bio.Nexus import Nexus
import os
from Bio.Alphabet import IUPAC, Gapped
import glob
#Convert all alignments to nexus format.
for fn in os.listdir('./uscos/aligns/'):
    input_handle = open(os.path.join('./uscos/aligns/',fn), "rU")
    fn2 = fn + ".nex"
    output_handle = open(os.path.join('./uscos/aligns/', fn2), "w")
    alignments = AlignIO.parse(input_handle, "fasta",alphabet=Gapped(IUPAC.IUPACAmbiguousDNA()))
    AlignIO.write(alignments, output_handle, "nexus")
    output_handle.close()
    input_handle.close()

#Grab all nexus files.
file_list = glob.glob(os.path.join('./uscos/aligns/','*.nex'))
nexi =  [(fname, Nexus.Nexus(fname)) for fname in file_list]
combined = Nexus.combine(nexi)
combined.export_phylip(filename='COMBINED.phy')
combined.write_nexus_data(filename=open('COMBINED.nex', 'w'))