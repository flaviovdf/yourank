#!/bin/bash
# Script to start the web server. Just calls the python code which
# will take care of the rest. Logs are redirected to the log 
# folder (folder where app is / log)

function findself() {
    echo `dirname $0`
}

OK=0
ERROR=1
SELFDIR=`findself`
LOGSDIR=$SELFDIR/logs

echo "Attempting to start server with params: $*"

if [ -e $LOGSDIR ]; then
    if [ -d $LOGSDIR ]; then
        echo "Log folder exists, appending"
    else
        echo "Log folder is apparently a file. Exiting"
        exit $ERROR
    fi
else
    echo "Creating log folder"
    mkdir $LOGSDIR
fi

PYTHONPATH=$PYTHONPATH/:$SELFDIR/ python $SELFDIR/code.py $* \
    2>> $LOGSDIR/yourank.log

if [ $? -eq $OK ]; then
    echo "Exiting!"
else
    echo "Some error occurred, see the error log"
fi
