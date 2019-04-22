ex ./00-RawData.csv <<EOS
"
g/^Class Date,Class Time,/-2s/^.*Edit Class Pay Rates/?#S?&/
g/ *Edit Class Pay Rates.*$/s///
g/^?#S?"/s/"//
g/^\$.*\...,,,,,,,,$/s/^/?#E?/
g/^".*\....,,,,,,,,$/s/^/?#E?/
g/^Class Date,Class Time,/.;/^?#E?/-1s/^/?data?/
v/^?.*?/d
g/^?#E?/+1s/^?#E?/?del?&/
g/^?del?/d
g/^?data?Class Date,Class Time,/-1s/^?#E?/?del?&/
g/^?del?/d
"
"Eliminate the duplicate rows that contain the extra column names 
g/^?data?Class Date,Class Time,/-1s/^/?m?/
g/^?m??#S?/s/^?m?//
g/^?m?/+1s/^?data?Class Date,Class Time,/?del?&/
g/^?m?/s///
g/^?del?/d
"
w! ./tmp/01-Revenue-All.txt
q!
EOS

cp ./tmp/01-Revenue-All.txt ./tmp/all.so
ex ./tmp/all.so <<EOS
"
v/^?#S?/d
g/ *$/s///
g/&/s//?and?/
g/^.*$/s//&?m?&/
g/?m??#S?/s//?m?/
g/^?#S?/s//\//
g/?m?/s//$\/+1;\/^?#E?\/-1s&/
g/?m?/s//\/^?data?\/&/
g/?m?/s/$/",\//
g/?m?/s//"/
g/?and?/s//\&/
"
w! ./tmp/all.so
"
q!
EOS

ex ./tmp/01-Revenue-All.txt <<EOS
"
2mo0
1s/^?data?/Instructors,/
g/^?data?Class Date,Class Time,/d
"
so ./tmp/all.so
"
g/?and?/s//\&/
g/^?#S?/d
g/^?#E?/d
"
w! ./dat/01-Revenue-00All.csv
q!
EOS

cp ./tmp/01-Revenue-All.txt ./tmp/each.so
ex ./tmp/each.so <<EOS
"
v/^?#S?/d
g/ *$/s///
g/^?#S?/s///
"
w! ./tmp/p.2
"
g/^./s/^/\//
g/^./s/$/$\/+1;\/^?#E?\/-1w!/
"
w! ./tmp/p.1
"
e! ./tmp/p.2
g/&/s//and/
g/, */s//-/g
g/ /s//-/g
g/./s/$/&.csv/
%!nl
g/^ */s///
g/^.\t/s/^/0/
g/\t/s//-/
g/^./s/^/.\/dat\/02-Revenue-/
"
w! ./tmp/p.2
"
!paste ./tmp/p.1 ./tmp/p.2 > ./tmp/each.so
"
q!
EOS

ex ./tmp/01-Revenue-All.txt <<EOS
"
so ./tmp/all.so
"
g/^?#S?/s///
g/^".*",Class Date,/s//Instructors,Class Date,/
g/?and?/s//\&/g
g?''/s///
"
so ./tmp/each.so
"
q!
EOS

