
INCLUDE := -I=common/ -I=daqcs_pi/ -I=daqcs_msp/ -I=comms_pi/
OUT := out

RMFILES := $(wildcard *.pb.cc) $(wildcard *.pb.h) $(wildcard *_pb2.py) $(wildcard *_pb2.pyc)
RMFILES += $(wildcard $(OUT)/*.pb.cc) $(wildcard $(OUT)/*.pb.h) $(wildcard $(OUT)/*_pb2.py) $(wildcard $(OUT)/*_pb2.pyc)

all:
	mkdir -p $(OUT)
	protoc $(INCLUDE) --python_out=$(OUT) --cpp_out=$(OUT) common/common.proto
	protoc $(INCLUDE) --python_out=$(OUT) --cpp_out=$(OUT) daqcs_pi/daqcs_pi.proto
	protoc $(INCLUDE) --python_out=$(OUT) --cpp_out=$(OUT) daqcs_msp/daqcs_msp.proto
	protoc $(INCLUDE) --python_out=$(OUT) --cpp_out=$(OUT) comms_pi/comms_pi.proto

python:
	mkdir -p $(OUT)
	protoc $(INCLUDE) --python_out=$(OUT) common/common.proto
	protoc $(INCLUDE) --python_out=$(OUT) daqcs_pi/daqcs_pi.proto
	protoc $(INCLUDE) --python_out=$(OUT) daqcs_msp/daqcs_msp.proto
	protoc $(INCLUDE) --python_out=$(OUT) comms_pi/comms_pi.proto

cpp:
	mkdir -p $(OUT)
	protoc $(INCLUDE) --cpp_out=$(OUT) common/common.proto
	protoc $(INCLUDE) --cpp_out=$(OUT) daqcs_pi/daqcs_pi.proto
	protoc $(INCLUDE) --cpp_out=$(OUT) daqcs_msp/daqcs_msp.proto
	protoc $(INCLUDE) --cpp_out=$(OUT) comms_pi/comms_pi.proto

clean:
		rm -f $(RMFILES)
