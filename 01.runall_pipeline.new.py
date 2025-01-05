
#--gsize=2456479391:pig
#--gsize=1005118510:goose
#--gsize=2922212712:human or --gsize=hs:human

import sys
import re
from optparse import OptionParser
import subprocess
import os
import time

class generate_bwamapjobs:

	def __init__ (self,path='ATAC'):

		self.path = path
		self.pathin = 'ATAC'
		self.input = open(self.path+'/filelist.txt','r')

	def generate_bwamapjobs (self):

	        os.system('mkdir '+self.path+'/runall_mapandpeakjobs/')

		allinfo=[]
		for line in self.input:
		      line=line.rstrip()
		      parts=line.split(' ')
		      allinfo.append(parts)

		self.input.close()

	        i=1
	        for parts in allinfo:
                       name=parts[2]

                       #myname1=parts[0].split('/')[-1].split('.fq.gz')[0]+'_val_1.fq.gz'
                       #myname2=parts[1].split('/')[-1].split('.fq.gz')[0]+'_val_2.fq.gz'

                       myname1=parts[0]
                       myname2=parts[1]

	               os.system('mkdir '+self.path+'/sorted_'+name)
	               os.system('mkdir '+self.path+'/sorted_'+name+'/'+name+'_macs2output1')

	               handle=open(str(self.path)+'/runall_mapandpeakjobs/'+str(name)+'_'+'macs2job','w')

                       print>>handle,'''#!/bin/bash
#PBS -q tangqianzi'''

                       print>>handle,'''echo start at time `date +%F'  '%H:%M`'''
                       print>>handle,'''cd '''+self.path+'/sorted_'+name+'/'

                       #print>>handle,'''bwa aln -l 32 -t 6 /lustre/tangqianzi/forShangdownload/analysis/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa '''+self.path+'''/Sample_ChIP'''+name+'''_R1_CAGATC.fastq.gz > '''+name+'''_R1alnhuman.sai'''
                       #print>>handle,'''bwa aln -l 32 -t 6 /lustre/tangqianzi/forShangdownload/analysis/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa '''+self.path+'''/Sample_ChIP'''+name+'''_R2_CAGATC.fastq.gz > '''+name+'''_R2alnhuman.sai'''

                       print>>handle,'export PATH=/Lustre01/zhangJM/02.soft/bowtie2-2.3.5.1-linux-x86_64:$PATH'
                       print>>handle,'bowtie2 -p 8 -t -q -N 1 -L 25 -X 2000 --no-mixed --no-discordant -x /Lustre02/Yangyuan/219_ATAC/hg38 -1 '+myname1+' -2 '+myname2+' -S '+name+'.sam'
                       print>>handle,'samtools view -hS '+name+'.sam | grep -v MT > '+name+'.rmMT.sam'
                       #print>>handle,'samtools view -hS '+name+'.sam | grep -v chrM > '+name+'.rmMT.sam'
                       print>>handle,'samtools view -bSh -q 10 '+name+'.rmMT.sam -o '+name+'.rmMT.rmq30.bam'
                       print>>handle,'''/Lustre01/tangqianzi/software/samtools-0.1.19/samtools sort -@ 4 -m 1000000000 '''+name+'.rmMT.rmq30.bam '+name+'''.bam.sort'''

                       print>>handle,'''/Lustre01/tangqianzi/software/samtools-0.1.19/samtools flagstat '''+name+'''.bam.sort.bam > '''+name+'''.bam.sort.bam.stat'''
                       print>>handle,'''/Lustre01/tangqianzi/software/samtools-0.1.19/samtools rmdup '''+name+'.bam.sort.bam '+name+'''.rmdup.bam'''

                       print>>handle,'''/Lustre01/tangqianzi/software/samtools-0.1.19/samtools flagstat '''+name+'''.rmdup.bam > '''+name+'''.rmdup.bam.stat'''

                       print>>handle,'''export PYTHON_EGG_CACHE=/Lustre02/data/hic/ChIPSeq20181128/pigoutput/01.BWA/bam/jobs/
export PATH=/Lustre01/tangqianzi/software/anaconda2new/bin/:$PATH'''

                       print>>handle,'''/Lustre01/tangqianzi/software/samtools-0.1.19/samtools sort -@ 4 -m 1000000000 -n '''+name+'''.rmdup.bam '''+name+'''.rmdup.bam.sort'''
                       ##print>>handle,'''/Lustre01/tangqianzi/software/samtools-0.1.19/samtools index '''+name+'''.rmdup.bam.sort.bam'''
                       print>>handle,'''export PATH=/Lustre01/tangqianzi/software/bedtools2/bin/:$PATH'''
                       ##print>>handle,'''bedtools bamtobed -i '''+name+'''.rmdup.bam.sort.bam > '''+name+'''.bed'''

                       ## print>>handle,'''cd '''+self.path+'/sorted_'+name+'/'
                       print>>handle,'''macs2 callpeak --tempdir='''+self.path+'/sorted_'+name+'/'+name+'_macs2output1 --verbose=2 --treatment='''+self.path+'/sorted_'+name+'/'+name+'''.rmdup.bam.sort.bam --shift -100 --extsize 200 --nomodel -B --SPMR --format=BAMPE --gsize=3088269832 --outdir='''+self.path+'/sorted_'+name+'/'+name+'_macs2output1 --name='''+name+''' --keep-dup=1 --qvalue=0.05'''
                       #print>>handle,'''macs2 callpeak --broad --broad-cutoff=0.1 --tempdir='''+self.path+'/'+name+'_macs2output2 --SPMR --bdg --verbose=2 --treatment='''+self.path+'/'+name+'''.rmdup.bam.sort.bam --format=BAMPE --gsize=2456479391 --outdir='''+self.path+'/'+name+'_macs2output2 --name='''+name+'''  --control='''+self.path+'/'+control+'''.rmdup.bam.sort.bam --keep-dup=all --qvalue=0.05'''

	               print>>handle,'''echo finish at time `date +%F'  '%H:%M`'''

                       handle.close()
                       i+=1

	        #for name in names:
	        myreturn=[]
	        for parts in allinfo:
	              name=parts[2]
	              #for i in range(1,11):
	              if 1:
                           p=subprocess.Popen('qsub -q tangqianzi -l nodes=1:ppn=8 -l mem=40gb '+str(self.path)+'/runall_mapandpeakjobs/'+str(name)+'_macs2job',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	                   out, err = p.communicate()
	                   eachr='.'.join(out.rstrip().split('.')[0:2])
	                   myreturn.append(eachr)

	        time.sleep(20)

	        while 1:
	              #for i in range(1,11):
                      sig=0
	              proc=subprocess.Popen('qstat',stdout=subprocess.PIPE).communicate()
	              procparts=list(proc)
                      p=procparts[0].split('\n')
                      for line in p:
	                   if line:
	                           parts=line.split()
	                           if str(parts[0]) in myreturn:
	                                   if str(parts[4])=='R' or str(parts[4])=='Q':
	                                           sig=1

	              if sig==0:
	                   break

                      time.sleep(300)


def main():

	generate_bwamapjobs().generate_bwamapjobs()


if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("User interrupt me! ;-) See you!\n")
		sys.exit(0)
