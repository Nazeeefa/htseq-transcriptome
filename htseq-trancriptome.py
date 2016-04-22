# coding: utf-8
import HTSeq as hs
import os
samfile = 'Cplan_Q2_16Aligned.out.sam'
gtffile = '/home/antqueen/genomics/experiments/analyses/PRO20160405_camponotus/trinity_denovo_normalized_camponotus/Transdecoder_ss/merge_genesets/Cpla_td_gff.Apr21_11.15.families.gtf'
gtf = hs.GFF_Reader(gtffile)
import itertools
exons = hs.GenomicArrayOfSets( "auto", stranded=True)
import collections
sam_file = hs.SAM_Reader(samfile)
counts = collections.Counter( )
for almnt in itertools.islice( sam_file, 100):
    if not almnt.aligned:
        count[ "_unmapped" ] += 1
        continue
    gene_ids = set()
    for iv, val in exons[ almnt.iv ].steps():
        gene_ids |= val
    if len(gene_ids) == 1:
        gene_id = list(gene_ids)[0]
        counts[ gene_id ] += 1
    elif len(gene_ids) == 0:
        counts[ "_no_feature" ] += 1
    else:
        counts[ "_ambiguous" ] += 1
        
print counts
for g, c in counts.items():
    print "%-10s %d" % (g, c)
    
def assess_bundle(bundle, features):
    counts = collections.Counter()
    for almnt in bundle:
        if not almnt.aligned:
            count[ "_unmapped" ] += 1
            continue
        gene_ids = set()
        for iv, val in features[ almnt.iv ].steps():
            gene_ids |= val
        if len(gene_ids) == 1:
            counts[ list(gene_ids)[0] ] += 1
        elif len(gene_ids) == 0:
            counts[ "_no_feature" ] += 1
        else:
            counts[ "_ambiguous" ] += 1
    return counts
multi_iterator = hs.pair_SAM_alignments( sam_file , bundle=True)