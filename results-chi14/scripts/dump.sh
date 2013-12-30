#!/bin/bash
set -e
set -u

if [ $# -lt 1 ]; then
    echo "Usage $0 <indir>"
    exit 1
fi

IN_DIR=$1
MIN=4

sqlite3 $IN_DIR/database.db <<!
.mode csv
.output $IN_DIR/state.csv
select * from sstate where (num_eval >= $MIN);
!

sqlite3 $IN_DIR/database.db <<!
.mode csv
.output $IN_DIR/eval.csv
select * from eval where session_id in \
    (select session_id from sstate where (num_eval >= $MIN));
!

sqlite3 $IN_DIR/database.db <<!
.mode csv
.output $IN_DIR/survey.csv
select * from userdetails where session_id in \
    (select session_id from sstate where (num_eval >= $MIN));
!
