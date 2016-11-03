# Protobuffer Steps:

## Installation

1. Installed the protobuf compiler on my Mac from here: https://github.com/google/protobuf/releases

2. Installed the protobuf package for Python:
	$ sudo pip install protobuf

	OR:

	- Downloaded from here: https://github.com/google/protobuf/releases
	$ ./configure
	$ make

	* NOTE: On macOS, System Integrity Protection must be disabled for this next step if you are installing to the system's Python installation
	Then installed the package by running:
	$ python python/setup.py build
	$ python python/setup.py install

## Creating a Proto File

1. Create a protobuf package (a .proto file)
2. Compile the proto file u