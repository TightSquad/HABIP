

SRC := $(wildcard *.proto)

all:
	protoc --python_out=. --cpp_out=. $(SRC)

python:
	protoc --python_out=. $(SRC)

cpp:
	protoc --cpp_out=. $(SRC)

clean:
		rm -f $(wildcard *.pb.cc) $(wildcard *.pb.h) $(wildcard *_pb2.py) $(wildcard *_pb2.pyc)
