

SRC := $(wildcard *.proto)

all:
	protoc --python_out=. --cpp_out=. $(SRC)
	protoc-c --c_out=. $(SRC)

python:
	protoc --python_out=. $(SRC)

cpp:
	protoc --cpp_out=. $(SRC)

c:
	protoc-c --c_out=. $(SRC)

clean:
		rm -f $(wildcard *.pb.cc) $(wildcard *.pb.h) $(wildcard *.pb-c.h) $(wildcard *.pb-c.c) $(wildcard *_pb2.py) $(wildcard *_pb2.pyc)
