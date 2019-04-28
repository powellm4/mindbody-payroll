#!/bin/bash

fileName=$(basename -s .xls Payroll_Report_4-1-2019_4-14-2019.xls)
fileName=$(basename -s .xls $1)

cp -a ./raw/$fileName.xls ./tmp/$fileName.xls
sed -i 's/\xC3\xB1/n/g' ./tmp/$fileName.xls
sed -i 's/\&#241;/n/g' ./tmp/$fileName.xls

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/$fileName.xls <<EOS
so ./bin/clean.so
w! ./tmp/${fileName}-1.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/${fileName}-1.txt <<EOS
g/"staffName"/+1s/^/?<stafName>?/
g/Private Lessons--/s/^/?<startPrivate>?/
g/Total for /s/^/?<totalFor>?/
g/^<tr/s/^/?<startRecord>?&/
g/\/tr>$/s/^/?<endRecord>?&/
g/^<td/s/^/?<startData>?&/
g/\/td>$/s/^/?<endData>?&/
w! ./tmp/${fileName}-2.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/${fileName}-2.txt <<EOS
g/^?<totalFor>?/-2s/^?<startRecord>?/?<del>?&/
g/^?<totalFor>?/-1s/^?<startData>?/?<del>?&/
g/^?<totalFor>?/+1;/^?<endRecord>?/s/^/?<del>?/
g/^?<del>?/d
g/^Vitalidad Movement Arts Center/-2;/^?<endRecord>?/s/^/?<del>?/
g/^# Services$/-1;/^?<endRecord>?/s/^/?<del>?/
g/^?<del>?/d
g/^Grand total/-2s/^?<startRecord>?/?<del>?&/
g/^Grand total/-1s/^?<startData>?/?<del>?&/
g/^Grand total/+1;/^?<endRecord>?/s/^/?<del>?/
g/^?<del>?/d
w! ./tmp/${fileName}-3.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/${fileName}-3.txt <<EOS
g/^?<startData>?/+1s/^?<endData>?/?<del>?&/
g/^?<del>??<endData>?/-1s/^?<startData>?/?<del>?&/
g/^?<del>?/d
g/^?<startData>?/+1;/^?<endData>?/-1s/^/?<data>?&/
v/^?<.*>?/d
g/^?<startData>?/d
g/^?<endData>?/d
v/^?<.*>?/d
w! ./tmp/${fileName}-4.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/${fileName}-4.txt <<EOS
g/&nbsp;/s// /g
g/^?<startRecord>?<tr class="subtotal">/;/^?<endRecord>?/s/^/?<del>?/
g/^?<del>?/d
g/^?<totalFor>?/-1s/^?<startRecord>?/?<del>?&/
g/^?<del>?/d
w! ./tmp/${fileName}-5.txt
q!
EOS

#######################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/${fileName}-5.txt <<EOS
g/^?<startPrivate>?/;/^?<totalFor>?/-1s/^/?<del>?/
g/^?<del>?/d
g/^?<totalFor>?/-1s/^?<stafName>?/?<del>?&/
g/^?<del>?/+1s/^?<totalFor>?/?<del>?&/
g/^?<del>?/d
w! ./tmp/01-Class-1.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/01-Class-1.txt <<EOS
so ./bin/data.so
w! ./tmp/01-Class-2.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/01-Class-2.txt <<EOS
so ./bin/names.so
w! ./tmp/01-Class-3.so
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/01-Class-2.txt <<EOS
so ./tmp/01-Class-3.so
w! ./tmp/01-Class-4.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/01-Class-4.txt <<'EOS'
3;$g/^"Instructors",/d
g/^?<stafName>?/d
g/^?<totalFor>?/d
g/?<and>?/s//\&/g
w! ./dat/00-01-Class-All.csv
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/01-Class-4.txt <<EOS
v/^?<stafName>?/d
g/^?<stafName>?/s/^/\/^/
g/?<stafName>?/s/$/\/+1;\/^?<totalFor>?\/-1w! /
w! ./tmp/01-Class-1p.1
q!
EOS

ex ./tmp/01-Class-4.txt <<EOS
v/^?<stafName>?/d
g/^?<stafName>?/s///
g/&/s//and/g
g/, */s//-/g
g/  */s//-/g
%!nl
g/\t/s/^ *//
g/^.\t/s/^/0/
g/^..\t/s/^/0/
g/\t/s//-/g
g/^./s/^/01-Class-/
w! ./tmp/01-Class-2p.2
"
g/^./s/^/.\/dat\//
g/^./s/$/.csv/
w! ./tmp/01-Class-2p.2
q!
EOS

paste ./tmp/01-Class-1p.1 ./tmp/01-Class-2p.2 \
    > ./tmp/01-Class-3each.so

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/01-Class-4.txt <<EOS
g/?<and>?/s//\&/g
so ./tmp/01-Class-3each.so
q!
EOS

#######################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/${fileName}-5.txt <<EOS
g/^?<stafName>?/s/^/?<m>?/
g/^?<startPrivate>?/;/^?<totalFor>?/s/^/?<m>?/
v/^?<m>?/d
g/?<m>??<stafName>?/s/^?<m>?/?<del>?/
g/^?<m>??<startPrivate>?/-1s/?<del>?//
g/^?<del>?/d
g/^?<m>?/s///
g/^?<startPrivate>?/d
w! ./tmp/02-Private-1.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/02-Private-1.txt <<EOS
so ./bin/data.so
w! ./tmp/02-Private-2.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/02-Private-2.txt <<EOS
so ./bin/names.so
w! ./tmp/02-Private-3.so
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/02-Private-2.txt <<EOS
so ./tmp/02-Private-3.so
w! ./tmp/02-Private-4.txt
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/02-Private-4.txt <<'EOS'
3;$g/^"Instructors",/d
g/^?<stafName>?/d
g/^?<totalFor>?/d
g/?<and>?/s//\&/g
w! ./dat/00-02-Private-All.csv
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/02-Private-4.txt <<EOS
v/^?<stafName>?/d
g/^?<stafName>?/s/^/\/^/
g/?<stafName>?/s/$/\/+1;\/^?<totalFor>?\/-1w! /
w! ./tmp/02-Private-1p.1
q!
EOS

ex ./tmp/02-Private-4.txt <<EOS
v/^?<stafName>?/d
g/^?<stafName>?/s///
g/&/s//and/g
g/, */s//-/g
g/  */s//-/g
%!nl
g/\t/s/^ *//
g/^.\t/s/^/0/
g/^..\t/s/^/0/
g/\t/s//-/g
g/^./s/^/02-Private-/
w! ./tmp/02-Private-2p.2
"
g/^./s/^/.\/dat\//
g/^./s/$/.csv/
w! ./tmp/02-Private-2p.2
q!
EOS

paste ./tmp/02-Private-1p.1 ./tmp/02-Private-2p.2 \
    > ./tmp/02-Private-3each.so

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ex ./tmp/02-Private-4.txt <<EOS
g/?<and>?/s//\&/g
so ./tmp/02-Private-3each.so
q!
EOS

