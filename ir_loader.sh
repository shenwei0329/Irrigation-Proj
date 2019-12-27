#!/bin/sh


DATE=`date -Idate`
mDATE=`date`
echo $DATE

sh << EOF

cd /home/shenwei/project/data-collector/

echo "$mDATE ... ing" >> p_loader.log
python p_loader.py >> p_loader.log
echo "$mDATE ... ed" >> p_loader.log

EOF

#
