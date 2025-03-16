#!/bin/bash
FILE=$1
URL=https://efrosgans.eecs.berkeley.edu/cyclegan/datasets/$FILE.zip
ZIP_FILE=./$FILE.zip
TARGET_DIR=./$FILE
wget -N $URL -O $ZIP_FILE
mkdir ./data
unzip $ZIP_FILE -d ./data
rm $ZIP_FILE