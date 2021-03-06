/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: daqcs_msp.proto */

#ifndef PROTOBUF_C_daqcs_5fmsp_2eproto__INCLUDED
#define PROTOBUF_C_daqcs_5fmsp_2eproto__INCLUDED

#include <protobuf-c/protobuf-c.h>

PROTOBUF_C__BEGIN_DECLS

#if PROTOBUF_C_VERSION_NUMBER < 1000000
# error This file was generated by a newer version of protoc-c which is incompatible with your libprotobuf-c headers. Please update your headers.
#elif 1002001 < PROTOBUF_C_MIN_COMPILER_VERSION
# error This file was generated by an older version of protoc-c which is incompatible with your libprotobuf-c headers. Please regenerate this file with a newer version of protoc-c.
#endif

#include "common.pb-c.h"
#include "daqcs_pi.pb-c.h"

typedef struct _DaqcsMsp__Data DaqcsMsp__Data;


/* --- enums --- */


/* --- messages --- */

struct  _DaqcsMsp__Data
{
  ProtobufCMessage base;
  protobuf_c_boolean has_id;
  int32_t id;
  size_t n_raspberrypis;
  DaqcsPi__Data **raspberrypis;
  Common__TempSensor *tempsensor;
};
#define DAQCS_MSP__DATA__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&daqcs_msp__data__descriptor) \
    , 0,0, 0,NULL, NULL }


/* DaqcsMsp__Data methods */
void   daqcs_msp__data__init
                     (DaqcsMsp__Data         *message);
size_t daqcs_msp__data__get_packed_size
                     (const DaqcsMsp__Data   *message);
size_t daqcs_msp__data__pack
                     (const DaqcsMsp__Data   *message,
                      uint8_t             *out);
size_t daqcs_msp__data__pack_to_buffer
                     (const DaqcsMsp__Data   *message,
                      ProtobufCBuffer     *buffer);
DaqcsMsp__Data *
       daqcs_msp__data__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   daqcs_msp__data__free_unpacked
                     (DaqcsMsp__Data *message,
                      ProtobufCAllocator *allocator);
/* --- per-message closures --- */

typedef void (*DaqcsMsp__Data_Closure)
                 (const DaqcsMsp__Data *message,
                  void *closure_data);

/* --- services --- */


/* --- descriptors --- */

extern const ProtobufCMessageDescriptor daqcs_msp__data__descriptor;

PROTOBUF_C__END_DECLS


#endif  /* PROTOBUF_C_daqcs_5fmsp_2eproto__INCLUDED */
