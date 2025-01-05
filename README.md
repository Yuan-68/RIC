# RIC
01.runall_pipeline.new.py: This script is used to process raw ATAC-seq data (typically in fastq format). It probably includes steps for quality control, alignment, peak calling, and ultimately outputs peaks related to genomic features.

HiCAN.py: This script appears to be designed specifically for processing Hi-C data, defining chromatin speckles and nucleolus regions based on interaction data.

runall_HICCUPS.py: This script is used to extend the loops in Hi-C data files. It probably utilizes the HICCUPS algorithm to identify and expand chromatin loops based on Hi-C interaction data.

test_overlap.py: This script is used to calculate the overlapping regions between different datasets.
