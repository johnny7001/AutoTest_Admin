#!/bin/bash
sudo apt update
sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel
sudo apt install -y tesseract-ocr
whereis tesseract-ocr
# tesseract --version

# echo hi
# sudo apt-get install g++
# sudo apt-get install autoconf automake libtool
# sudo apt-get install pkg-config
# sudo apt-get install libpng-dev
# sudo apt-get install libjpeg8-dev
# sudo apt-get install libtiff5-dev
# sudo apt-get install zlib1g-dev

# sudo apt-get install libleptonica-dev

# wget https://github.com/tesseract-ocr/tesseract/archive/3.05.02.tar.gz

# ### Compile and run
# ./autogen.sh
# ./configure --prefix=/usr/share/tesseract-ocr/
# make
# make install
# ls -Rl /usr/share/tesseract-ocr/
# ### Set PATH (Optional)
# echo "PATH=/usr/share/tesseract-ocr/bin:\$PATH" >> ~/.profile

# # $ make training
# # $ sudo make training-install