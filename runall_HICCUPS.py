import sys
import re
from optparse import OptionParser
import subprocess
import os
import time


# /lustre2/home/tangqianzi/software/mirnylab-hiclib-8c146707b6f6/examples/pipeline_2017/

class generate:

    def __init__(self, path='/Lustre02/lixingyu/yy_hic/'):

        self.path = path
        self.jobfolder = 'runallHICCUPSjobs'
        self.maxnum = '22'

    def generate(self):

        # os.system('python '+self.path+'/combine_results.py '+self.mychr+' '+self.path)

        os.system('mkdir -p ' + self.path + '/' + self.jobfolder)
        # os.system('mkdir -p '+self.outpath)

        myoutput = open(self.path + '/' + self.jobfolder + '/runthis_pipeline.sh', 'w')

        # os.system('python '+self.scriptpath+'/get_loop_union.new.py '+self.mychr)

        # ======= get simiHICCUPS ===============================

        myoutput1 = open(self.path + '/' + self.jobfolder + '/runthis_test.sh', 'w')
        myoutput2 = open(self.path + '/' + self.jobfolder + '/alljobs_test.sh', 'w')

        # results={}

        # for i in range(1,19):
        # results[str(i)]=[]

        # for c in mykeeploops:
        # results[self.mychr].append(c[0])

        # allnames=['ULB_CC2_H3K4me3.rmdup.bam','ULB_CC4_H3K4me3.rmdup.bam','ULB_CC2_INPUT.rmdup.bam','ULB_CC4_INPUT.rmdup.bam']

        mychroms = []
        mychroms.append('22')

        for i in range(1, int(self.maxnum) + 1):
            if i != 22:
                # if 1:
                mychroms.append(str(i))
        # mychroms.append(str(i)+'\(mat\)')

        for i in range(0, len(mychroms)):
            # os.system('mkdir -p '+self.outpath+'/aroundloopquantilenew/'+mytissue+'/'+self.mychr)
            # for mychr in mychroms:
            # for j in range(0,len(mychroms)):
            if 1:
                if 1:
                    mychr1 = mychroms[i]
                    if 1:
                        print >> myoutput2, '''cd /Lustre02/lixingyu/yy_hic/HICCUPSresults/
export PATH=/usr/local/cuda-8.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
java -Xms512m -Xmx20048m -Djava.library.path=/Lustre01/tangqianzi/software/JCuda-All-0.8.0-bin-linux-x86_64/ -jar /Lustre01/tangqianzi/software/juicer_tools.1.8.9_jcuda.0.8.jar hiccups -m 500 -r 5000,10000 /Lustre02/lixingyu/yy_hic/4DNFICSTCJQZ.hic -c ''' + mychr1 + ''' all_hiccups_loopsfinal''' + mychr1

        # print>>myoutput1,'/usr/bin/perl /Lustre01/tangqianzi/software/scripts/qsub-sgenew.pl --lines 4 --jobprefix pre --convert no --resource nodes=1:ppn=1,mem=240g '+self.path+'/'+self.jobfolder+'/alljobs_pre.sh'
        print >> myoutput1, '/usr/bin/perl /Lustre01/tangqianzi/software/scripts/qsub-sgenew.pl --queue genomics --maxjob 200 --lines 4 --jobprefix convert --convert no --resource nodes=gpunode11.hpc:ppn=1,mem=20g ' + self.path + '/' + self.jobfolder + '/alljobs_test.sh'

        myoutput1.close()
        myoutput2.close()
        # self.input2.close()

        print >> myoutput, 'sh ' + self.path + '/' + self.jobfolder + '/runthis_test.sh'

        myoutput.close()


# self.input.close()

def main():
    usage = "usage: %prog [options] <pathandfiles>"
    description = "Generate jobs."

    optparser = OptionParser(version="%prog 0.1", description=description, usage=usage, add_help_option=False)
    optparser.add_option("-h", "--help", action="help", help="Show this help message and exit.")

    (options, pathandfiles) = optparser.parse_args()

    generate().generate()


# generate(mychr=pathandfiles[0]).generate()


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)

