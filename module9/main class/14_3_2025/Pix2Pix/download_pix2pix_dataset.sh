FILE=$1
URL=https://efrosgans.eecs.berkeley.edu/pix2pix/datasets/$FILE.tar.gz
TAR_FILE=./$FILE.tar.gz
TARGET_DIR=./$FILE/
wget -N $URL -O $TAR_FILE
mkdir ./data
tar -zxvf $TAR_FILE -C ./data
rm $TAR_FILE