#!/bin/bash
# Convert tabs to spaces and Convert html symbols to text
# source ./bin/s01-initial_process.sh \
#        ./tmp/s00-01All.txt 
#        #Input-: ./tmp/s00-01All.txt
#        #Output: ,/tmp/s01-01All.txt
#        #Output: ./tmp/s01-02All.txt

# 1) Convert tabs to spaces:
/usr/bin/expand $1 > ./tmp/s01-01All.txt

# 2) Convert html symbols to text:
/bin/cat ./tmp/s01-01All.txt | /bin/sed 's/\xC3\xB1/n/g' \
                    | /bin/sed 's/\&#241;/n/g'  \
                    | /bin/sed "s/\&#8217;/'/g" \
                    | /bin/sed 's/\&nbsp;/ /g'  \
                    | /bin/sed "s/\&amp;/\&/g"  \
                    | /bin/sed "s/\&ndash/-/g"  \
> ./tmp/s01-02All.txt

