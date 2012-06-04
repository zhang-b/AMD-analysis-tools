import os

TEMP ="""
#PBS -S /bin/bash
#PBS -l nodes=1,walltime=5000:00:00
#PBS -M chengtao@sjtu.edu.cn

cd %MF%
echo $HOSTNAME > host.log
dname=%TF%
echo $dname >> host.log
if [ ! -d $dname ]; then
    mkdir -p %TF%
else
    echo "folder exists"
fi
cp geo %TF%
cp ffield %TF%
cp control %TF%
cd %TF%

/home/chengtao/reaxMD/water/src2/SerialReax geo ffield control
tar -cvzf run.tar.gz water*

"""

for i in os.listdir('.'):
    if os.path.isdir(i):
        os.chdir(i)
        JN = 'amd_1898_%s'%i
        MF = os.getcwd()
        TF = '/state/partition1/jobs/chengtao/%s'%JN
        lines = TEMP
        lines = lines.replace('%MF%', MF)
        lines = lines.replace('%TF%', TF)
        lines = lines.replace('%JN%', JN)
        o = open('reax.sh', 'w')
        o.write(lines)
        o.close()
        os.chdir('..')
