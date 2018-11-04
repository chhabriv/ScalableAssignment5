#!/bin/bash
#author: Viren Chhabira - chhabriv.tcd.ie - 18301780
#date: October 3rd, 2018

#download rockyou.txt
#echo "START: Downloading rockyou.txt"
#wget https://www.scrapmaker.com/data/wordlists/dictionaries/rockyou.txt
#echo "END: Download rockyou.txt complete"

#download NVIDIA Driver x86_64-367.128
echo "START: Downloading NVIDIA Driver x86_64-367.128"
wget http://us.download.nvidia.com/XFree86/Linux-x86_64/367.128/NVIDIA-Linux-x86_64-367.128.run
echo "END : Download WGET is complete"

#upgrade cycle and dependencies
echo "START: Update and build essentials"
sudo apt update
sudo apt upgrade
sudo apt-get install build-essential
sudo apt-get install linux-image-extra-virtual
echo "END: Update and build essentials"

#driver install
echo "START: NVIDIA x86_64-367.128 driver install"
sudo /bin/bash NVIDIA-Linux-x86_64-367.128.run
echo "END: Driver install"

echo "START: install john the ripper"
git clone https://github.com/magnumripper/JohnTheRipper.git
cd JohnTheRipper/src/
sudo apt-get install nvidia-opencl-dev
sudo apt-get install cmake bison flex libicu-dev
git clone --recursive https://github.com/teeshop/rexgen.git
./rexgen/install.sh
./configure && make -s clean && make -sj4
cd ../../
echo "END: JTR install"

#install hashcat
echo "START: HASHCAT install"
sudo apt install hashcat
echo "END: HASHCAT install complete"

#checking hashcat sees GPU
echo "HASHCAT Benchmark"
hashcat -I

#checking john sees devices
echo "John Devices"
./JohnTheRipper/run/john --list=opencl-devices | grep "Device #"

