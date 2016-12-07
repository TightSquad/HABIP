# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: comms_pi.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2
import daqcs_msp_pb2 as daqcs__msp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='comms_pi.proto',
  package='comms_pi',
  syntax='proto3',
  serialized_pb=_b('\n\x0e\x63omms_pi.proto\x12\x08\x63omms_pi\x1a\x0c\x63ommon.proto\x1a\x0f\x64\x61qcs_msp.proto\"\xc5\x01\n\x04\x44\x61ta\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1c\n\x03msp\x18\x02 \x01(\x0b\x32\x0f.daqcs_msp.Data\x12%\n\tcommsTemp\x18\x03 \x01(\x0b\x32\x12.common.TempSensor\x12-\n\rcommsPressure\x18\x04 \x01(\x0b\x32\x16.common.PressureSensor\x12 \n\tgpsSensor\x18\x05 \x01(\x0b\x32\r.comms_pi.GPS\x12\x1b\n\x04\x61prs\x18\x06 \x01(\x0b\x32\r.comms_pi.GPS\"m\n\x03GPS\x12\n\n\x02id\x18\x01 \x01(\x05\x12#\n\x05north\x18\x02 \x01(\x0b\x32\x14.comms_pi.Coordinate\x12\"\n\x04west\x18\x03 \x01(\x0b\x32\x14.comms_pi.Coordinate\x12\x11\n\televation\x18\x04 \x01(\x02\".\n\nCoordinate\x12\x0f\n\x07\x64\x65grees\x18\x01 \x01(\x02\x12\x0f\n\x07minutes\x18\x02 \x01(\x02\x62\x06proto3')
  ,
  dependencies=[common__pb2.DESCRIPTOR,daqcs__msp__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DATA = _descriptor.Descriptor(
  name='Data',
  full_name='comms_pi.Data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='comms_pi.Data.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msp', full_name='comms_pi.Data.msp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='commsTemp', full_name='comms_pi.Data.commsTemp', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='commsPressure', full_name='comms_pi.Data.commsPressure', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gpsSensor', full_name='comms_pi.Data.gpsSensor', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aprs', full_name='comms_pi.Data.aprs', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=257,
)


_GPS = _descriptor.Descriptor(
  name='GPS',
  full_name='comms_pi.GPS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='comms_pi.GPS.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='north', full_name='comms_pi.GPS.north', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='west', full_name='comms_pi.GPS.west', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='elevation', full_name='comms_pi.GPS.elevation', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=259,
  serialized_end=368,
)


_COORDINATE = _descriptor.Descriptor(
  name='Coordinate',
  full_name='comms_pi.Coordinate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='degrees', full_name='comms_pi.Coordinate.degrees', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='minutes', full_name='comms_pi.Coordinate.minutes', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=370,
  serialized_end=416,
)

_DATA.fields_by_name['msp'].message_type = daqcs__msp__pb2._DATA
_DATA.fields_by_name['commsTemp'].message_type = common__pb2._TEMPSENSOR
_DATA.fields_by_name['commsPressure'].message_type = common__pb2._PRESSURESENSOR
_DATA.fields_by_name['gpsSensor'].message_type = _GPS
_DATA.fields_by_name['aprs'].message_type = _GPS
_GPS.fields_by_name['north'].message_type = _COORDINATE
_GPS.fields_by_name['west'].message_type = _COORDINATE
DESCRIPTOR.message_types_by_name['Data'] = _DATA
DESCRIPTOR.message_types_by_name['GPS'] = _GPS
DESCRIPTOR.message_types_by_name['Coordinate'] = _COORDINATE

Data = _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), dict(
  DESCRIPTOR = _DATA,
  __module__ = 'comms_pi_pb2'
  # @@protoc_insertion_point(class_scope:comms_pi.Data)
  ))
_sym_db.RegisterMessage(Data)

GPS = _reflection.GeneratedProtocolMessageType('GPS', (_message.Message,), dict(
  DESCRIPTOR = _GPS,
  __module__ = 'comms_pi_pb2'
  # @@protoc_insertion_point(class_scope:comms_pi.GPS)
  ))
_sym_db.RegisterMessage(GPS)

Coordinate = _reflection.GeneratedProtocolMessageType('Coordinate', (_message.Message,), dict(
  DESCRIPTOR = _COORDINATE,
  __module__ = 'comms_pi_pb2'
  # @@protoc_insertion_point(class_scope:comms_pi.Coordinate)
  ))
_sym_db.RegisterMessage(Coordinate)


# @@protoc_insertion_point(module_scope)