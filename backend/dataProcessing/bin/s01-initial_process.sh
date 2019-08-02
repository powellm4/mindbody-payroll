#!/bin/bash
# Convert tabs to spaces and Convert html symbols to text
# source ./bin/s01-initial_process.sh \
#        ./tmp/s00-01All.txt 
#        #Input-: ./tmp/s00-01All.txt
#        #Output: ,/tmp/s01-01All.txt
#        #Output: ./tmp/s01-02All.txt

# 1) Convert tabs to spaces:
expand $1 > ./tmp/s01-01All.txt

# 2) Convert html symbols to text:
cat ./tmp/s01-01All.txt | sed 's/\xC3\xB1/n/g' \
                    | sed 's/\&#241;/n/g'  \
                    | sed "s/\&#8217;/'/g" \
                    | sed 's/\&nbsp;/ /g'  \
                    | sed "s/\&amp;/\&/g"  \
                    | sed "s/\&ndash/-/g"  \
> ./tmp/s01-02All.txt

