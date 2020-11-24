#!/bin/bash

set -e

# Define the nmag version
version="0.2.1";

# Install Dependencies
sudo apt install python2 python2-dev libreadline-dev g++ libblas-dev libreadline-dev make m4 gawk zlib1g-dev liblapack-dev mpich mpi-default-bin ocaml

curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
sudo python2 get-pip.py

sudo pip2 install numpy pyvtk ipython py ply scipy tables

# Untar archive
tar xzvf nmag-$version.tar.gz

# Navigate to the nmag directory
cd nmag-$version

# Replace the original Makefile with the modified Makefile
mv Makefile Makefile.old
cp ../Makefile .

# Replace the original shell.py with the modified shell.py
mv nsim/interface/nsim/shell.py nsim/interface/nsim/shell.py.old
cp ../shell.py nsim/interface/nsim

# Convert old pytables camel casing to underscore notation
grep -rl nsim -e setNodeAttr | xargs sed -i s/setNodeAttr/set_node_attr/g
grep -rl nsim -e getNodeAttr | xargs sed -i s/getNodeAttr/get_node_attr/g
grep -rl nsim -e isPyTablesFile | xargs sed -i s/isPyTablesFile/is_pytables_file/g
grep -rl nsim -e isHDF5File | xargs sed -i s/isHDF5File/is_hdf5_file/g
grep -rl nsim -e openFile | xargs sed -i s/openFile/open_file/g
grep -rl nsim -e createGroup | xargs sed -i s/createGroup/create_group/g
grep -rl nsim -e createArray | xargs sed -i s/createArray/create_array/g
grep -rl nsim -e createCArray | xargs sed -i s/createCArray/create_carray/g
grep -rl nsim -e createTable | xargs sed -i s/createTable/create_table/g
grep -rl nsim -e getNode | xargs sed -i s/getNode/get_node/g

# Update out of date python
grep -rl nsim -e 'if None in vals\[:3\]:' | xargs sed -i 's/if None in vals\[:3\]:/if True in \[val is None for val in vals\[:3\]\]:/g'

# Compile the code
if make; then
	echo -e "\n\033[5mCompilation Complete.\033[0m The binaries can be foud in the nmag-$version/bin directory."
else
	echo -e "\n\033[5mCompilation Failed.\033[0m"
fi
