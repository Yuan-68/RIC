
# -*- coding: utf-8 -*-

import sys
import os
import re
import numpy as np
from optparse import OptionParser
import subprocess
import time
#from scipy import stats
#import numpy as np
import math
import random

class autoremove_bam:

	def __init__ (self):

	        self.input1 = open('/data/Yangyuan/Ric_seq/chip-seq/overlap/ARID3A_45806_peaks_sorted.txt','r')
	        self.input2 = open('/data/Yangyuan/Ric_seq/chip-seq/overlap/ARID4B_100639_peaks_sorted.txt','r')
	        self.input3 = open('/data/Yangyuan/Ric_seq/chip-seq/test/all/interaction3.txt','r')
	        #self.output = open('/Lustre03/data/tangqianzi/Gut_unroll/outputs/'+sample+'/pos2spotID.absolutedistance_finalgroupsforpseudobulk.new.xls','w')
	        self.output = open('./overlap_test.txt','w')
	        #self.count = '40'

	def autoremove_bam (self):

	        chroms=[]
	        for i in range(1,23):
	               chroms.append('chr'+str(i))

	        chroms.append('chrX')

	        chrom_pairs={}
	        for i in range(0,len(chroms)):
	               for j in range(0,len(chroms)):
	                    chrom_pairs[chroms[i]+'_'+chroms[j]]={}

	        for line in self.input3:
	               line=line.rstrip()
	               parts=line.split('\t')
	               chrinfo=[]

	               if ('chr'+str(parts[0]) not in chroms) or ('chr'+str(parts[6]) not in chroms):
	                       continue

	               chrinfo.append([str(parts[0]),int(parts[1]),int(parts[2])])
	               chrinfo.append([str(parts[6]),int(parts[7]),int(parts[8])])

	               chrinfo.sort()

	               chr1='chr'+str(chrinfo[0][0])
	               chr1_start=chrinfo[0][1]
	               chr1_end=chrinfo[0][2]

	               chr2='chr'+str(chrinfo[1][0])
	               chr2_start=chrinfo[1][1]
	               chr2_end=chrinfo[1][2]

	               chrom_pairs[chr1+'_'+chr2][str(chr1_start)+'_'+str(chr1_end)+';'+str(chr2_start)+'_'+str(chr2_end)]=0



	        myinput1={}
	        myinput2={}

	        for mychr in chroms:
                        myinput1[mychr]={}
                        myinput2[mychr]={}

	        for line in self.input1:
	                line=line.rstrip()
	                parts=line.split('\t')
	                if parts[0] not in chroms:
	                       continue

	                myinput1[parts[0]][parts[1]+'_'+parts[2]]=0

	        for line in self.input2:
	                line=line.rstrip()
	                parts=line.split('\t')
	                if parts[0] not in chroms:
	                       continue

	                myinput2[parts[0]][parts[1]+'_'+parts[2]]=0


	        countlap=0
	        for mychr_pair in chrom_pairs:
	               chr1=mychr_pair.split('_')[0]
	               chr2=mychr_pair.split('_')[1]

	               if chr1==chr2:
	                       for each in chrom_pairs[mychr_pair]:

	                               start1=int(each.split(';')[0].split('_')[0])
	                               end1=int(each.split(';')[0].split('_')[1])

	                               start2=int(each.split(';')[1].split('_')[0])
	                               end2=int(each.split(';')[1].split('_')[1])

	                               if chr1 in myinput1:
	                                       for each1 in myinput1[chr1]:
	                                               start1_1=int(each1.split('_')[0])
	                                               end1_1=int(each1.split('_')[1])

	                                               if start1_1<=end1 and start1<=end1_1:
	                                                       if chr2 in myinput2:
	                                                               for each2 in myinput2[chr2]:
	                                                                       start2_1=int(each2.split('_')[0])
	                                                                       end2_1=int(each2.split('_')[1])
	                                                                       if start2_1<=end2 and start2<=end2_1:
	                                                                               countlap+=1


	                               if chr1 in myinput2:
	                                       for each1 in myinput2[chr1]:
	                                               start1_1=int(each1.split('_')[0])
	                                               end1_1=int(each1.split('_')[1])

	                                               if start1_1<=end1 and start1<=end1_1:
	                                                       if chr2 in myinput1:
	                                                               for each2 in myinput1[chr2]:
	                                                                       start2_1=int(each2.split('_')[0])
	                                                                       end2_1=int(each2.split('_')[1])
	                                                                       if start2_1<=end2 and start2<=end2_1:
	                                                                               countlap+=1


	               elif chr1!=chr2:
	                       ##chr1_1=chr2
	                       ##chr2_1=chr1

                               for each in chrom_pairs[mychr_pair]:

	                               start1=int(each.split(';')[0].split('_')[0])
	                               end1=int(each.split(';')[0].split('_')[1])

	                               start2=int(each.split(';')[1].split('_')[0])
	                               end2=int(each.split(';')[1].split('_')[1])

	                               if chr1 in myinput1:
	                                       for each1 in myinput1[chr1]:
	                                               start1_1=int(each1.split('_')[0])
	                                               end1_1=int(each1.split('_')[1])

	                                               if start1_1<=end1 and start1<=end1_1:
	                                                       if chr2 in myinput2:
	                                                               for each2 in myinput2[chr2]:
	                                                                       start2_1=int(each2.split('_')[0])
	                                                                       end2_1=int(each2.split('_')[1])
	                                                                       if start2_1<=end2 and start2<=end2_1:
	                                                                               countlap+=1


	                               if chr1 in myinput2:
	                                       for each1 in myinput2[chr1]:
	                                               start1_1=int(each1.split('_')[0])
	                                               end1_1=int(each1.split('_')[1])

	                                               if start1_1<=end1 and start1<=end1_1:
	                                                       if chr2 in myinput1:
	                                                               for each2 in myinput1[chr2]:
	                                                                       start2_1=int(each2.split('_')[0])
	                                                                       end2_1=int(each2.split('_')[1])
	                                                                       if start2_1<=end2 and start2<=end2_1:
	                                                                               countlap+=1


	        print (countlap)

	        self.output.write(str(countlap)+'\n')

	        self.input1.close()
	        self.input2.close()
	        self.input3.close()
	        self.output.close()


def main():

	usage = "usage: %prog [options] <pathandfiles>"
	description = "Generate jobs."

	optparser = OptionParser(version="%prog 0.1",description=description,usage=usage,add_help_option=False)
	optparser.add_option("-h","--help",action="help",help="Show this help message and exit.")

	(options,pathandfiles) = optparser.parse_args()

	autoremove_bam().autoremove_bam()


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
