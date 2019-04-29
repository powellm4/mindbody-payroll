#!/bin/bash

fileName=$(basename -s .xls Payroll_Report_4-1-2019_4-14-2019.xls)
fileName=$(basename -s .xls $1)

cp -a ./raw/$fileName.xls ./tmp/$fileName.xls
sed -i 's/\xC3\xB1/n/g' ./tmp/$fileName.xls
sed -i 's/\&#241;/n/g' ./tmp/$fileName.xls

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/$fileName.xls <<EOS
so ./bin/clean01.so
so ./bin/mark01Basics.so
so ./bin/mark02Data.so
so ./bin/clean02.so
so ./bin/joinData.so
w! ./tmp/${fileName}-1.txt
so ./bin/prepare4Class.so
w! ./tmp/01Class0All.txt
so ./bin/names.so
w! ./tmp/01Class.so
e! ./tmp/${fileName}-1.txt
so ./bin/prepare4Private.so
w! ./tmp/02Private0All.txt
so ./bin/names.so
w! ./tmp/02Private.so
e! ./tmp/01Class0All.txt
so ./tmp/01Class.so
so ./bin/clean03.so
w! ./dat/00-01-Class-All.csv
e! ./tmp/02Private0All.txt
so ./tmp/02Private.so
so ./bin/clean03.so
w! ./dat/00-02-Private-All.csv
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/01Class0All.txt <<EOS
so ./bin/paste1.so
w! ./tmp/01ClassPaste.1
e! ./tmp/01Class0All.txt
so ./bin/paste2.so
g/^./s/^/01-Class-/
g/^./s/^/.\/dat\//
w! ./tmp/01ClassPaste.2
!paste ./tmp/01ClassPaste.1 ./tmp/01ClassPaste.2 \
       > ./tmp/01ClassEach.so
e! ./tmp/01Class0All.txt
so ./tmp/01Class.so
g/?<and>?/s//\&/g
g/&nbsp;/s// /g
so ./tmp/01ClassEach.so
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/02Private0All.txt <<EOS
so ./bin/paste1.so
w! ./tmp/02PrivatePaste.1
e! ./tmp/02Private0All.txt
so ./bin/paste2.so
g/^./s/^/02-Private-/
g/^./s/^/.\/dat\//
w! ./tmp/02PrivatePaste.2
!paste ./tmp/02PrivatePaste.1 ./tmp/02PrivatePaste.2 \
       > ./tmp/02PrivateEach.so
e! ./tmp/02Private0All.txt
so ./tmp/02Private.so
g/?<and>?/s//\&/g
g/&nbsp;/s// /g
so ./tmp/02PrivateEach.so
q!
EOS

