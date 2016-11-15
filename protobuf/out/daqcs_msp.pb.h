// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: daqcs_msp.proto

#ifndef PROTOBUF_daqcs_5fmsp_2eproto__INCLUDED
#define PROTOBUF_daqcs_5fmsp_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 3001000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 3001000 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/unknown_field_set.h>
#include "common.pb.h"
#include "daqcs_pi.pb.h"
// @@protoc_insertion_point(includes)

namespace daqcs_msp {

// Internal implementation detail -- do not call these.
void protobuf_AddDesc_daqcs_5fmsp_2eproto();
void protobuf_InitDefaults_daqcs_5fmsp_2eproto();
void protobuf_AssignDesc_daqcs_5fmsp_2eproto();
void protobuf_ShutdownFile_daqcs_5fmsp_2eproto();

class Data;

// ===================================================================

class Data : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:daqcs_msp.Data) */ {
 public:
  Data();
  virtual ~Data();

  Data(const Data& from);

  inline Data& operator=(const Data& from) {
    CopyFrom(from);
    return *this;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const Data& default_instance();

  static const Data* internal_default_instance();

  void Swap(Data* other);

  // implements Message ----------------------------------------------

  inline Data* New() const { return New(NULL); }

  Data* New(::google::protobuf::Arena* arena) const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const Data& from);
  void MergeFrom(const Data& from);
  void Clear();
  bool IsInitialized() const;

  size_t ByteSizeLong() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* InternalSerializeWithCachedSizesToArray(
      bool deterministic, ::google::protobuf::uint8* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const {
    return InternalSerializeWithCachedSizesToArray(false, output);
  }
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  void InternalSwap(Data* other);
  void UnsafeMergeFrom(const Data& from);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return _internal_metadata_.arena();
  }
  inline void* MaybeArenaPtr() const {
    return _internal_metadata_.raw_arena_ptr();
  }
  public:

  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // optional int32 id = 1;
  void clear_id();
  static const int kIdFieldNumber = 1;
  ::google::protobuf::int32 id() const;
  void set_id(::google::protobuf::int32 value);

  // repeated .daqcs_pi.Data raspberryPis = 2;
  int raspberrypis_size() const;
  void clear_raspberrypis();
  static const int kRaspberryPisFieldNumber = 2;
  const ::daqcs_pi::Data& raspberrypis(int index) const;
  ::daqcs_pi::Data* mutable_raspberrypis(int index);
  ::daqcs_pi::Data* add_raspberrypis();
  ::google::protobuf::RepeatedPtrField< ::daqcs_pi::Data >*
      mutable_raspberrypis();
  const ::google::protobuf::RepeatedPtrField< ::daqcs_pi::Data >&
      raspberrypis() const;

  // optional .common.TempSensor tempSensor = 3;
  bool has_tempsensor() const;
  void clear_tempsensor();
  static const int kTempSensorFieldNumber = 3;
  const ::common::TempSensor& tempsensor() const;
  ::common::TempSensor* mutable_tempsensor();
  ::common::TempSensor* release_tempsensor();
  void set_allocated_tempsensor(::common::TempSensor* tempsensor);

  // @@protoc_insertion_point(class_scope:daqcs_msp.Data)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::RepeatedPtrField< ::daqcs_pi::Data > raspberrypis_;
  ::common::TempSensor* tempsensor_;
  ::google::protobuf::int32 id_;
  mutable int _cached_size_;
  friend void  protobuf_InitDefaults_daqcs_5fmsp_2eproto_impl();
  friend void  protobuf_AddDesc_daqcs_5fmsp_2eproto_impl();
  friend void protobuf_AssignDesc_daqcs_5fmsp_2eproto();
  friend void protobuf_ShutdownFile_daqcs_5fmsp_2eproto();

  void InitAsDefaultInstance();
};
extern ::google::protobuf::internal::ExplicitlyConstructed<Data> Data_default_instance_;

// ===================================================================


// ===================================================================

#if !PROTOBUF_INLINE_NOT_IN_HEADERS
// Data

// optional int32 id = 1;
inline void Data::clear_id() {
  id_ = 0;
}
inline ::google::protobuf::int32 Data::id() const {
  // @@protoc_insertion_point(field_get:daqcs_msp.Data.id)
  return id_;
}
inline void Data::set_id(::google::protobuf::int32 value) {
  
  id_ = value;
  // @@protoc_insertion_point(field_set:daqcs_msp.Data.id)
}

// repeated .daqcs_pi.Data raspberryPis = 2;
inline int Data::raspberrypis_size() const {
  return raspberrypis_.size();
}
inline void Data::clear_raspberrypis() {
  raspberrypis_.Clear();
}
inline const ::daqcs_pi::Data& Data::raspberrypis(int index) const {
  // @@protoc_insertion_point(field_get:daqcs_msp.Data.raspberryPis)
  return raspberrypis_.Get(index);
}
inline ::daqcs_pi::Data* Data::mutable_raspberrypis(int index) {
  // @@protoc_insertion_point(field_mutable:daqcs_msp.Data.raspberryPis)
  return raspberrypis_.Mutable(index);
}
inline ::daqcs_pi::Data* Data::add_raspberrypis() {
  // @@protoc_insertion_point(field_add:daqcs_msp.Data.raspberryPis)
  return raspberrypis_.Add();
}
inline ::google::protobuf::RepeatedPtrField< ::daqcs_pi::Data >*
Data::mutable_raspberrypis() {
  // @@protoc_insertion_point(field_mutable_list:daqcs_msp.Data.raspberryPis)
  return &raspberrypis_;
}
inline const ::google::protobuf::RepeatedPtrField< ::daqcs_pi::Data >&
Data::raspberrypis() const {
  // @@protoc_insertion_point(field_list:daqcs_msp.Data.raspberryPis)
  return raspberrypis_;
}

// optional .common.TempSensor tempSensor = 3;
inline bool Data::has_tempsensor() const {
  return this != internal_default_instance() && tempsensor_ != NULL;
}
inline void Data::clear_tempsensor() {
  if (GetArenaNoVirtual() == NULL && tempsensor_ != NULL) delete tempsensor_;
  tempsensor_ = NULL;
}
inline const ::common::TempSensor& Data::tempsensor() const {
  // @@protoc_insertion_point(field_get:daqcs_msp.Data.tempSensor)
  return tempsensor_ != NULL ? *tempsensor_
                         : *::common::TempSensor::internal_default_instance();
}
inline ::common::TempSensor* Data::mutable_tempsensor() {
  
  if (tempsensor_ == NULL) {
    tempsensor_ = new ::common::TempSensor;
  }
  // @@protoc_insertion_point(field_mutable:daqcs_msp.Data.tempSensor)
  return tempsensor_;
}
inline ::common::TempSensor* Data::release_tempsensor() {
  // @@protoc_insertion_point(field_release:daqcs_msp.Data.tempSensor)
  
  ::common::TempSensor* temp = tempsensor_;
  tempsensor_ = NULL;
  return temp;
}
inline void Data::set_allocated_tempsensor(::common::TempSensor* tempsensor) {
  delete tempsensor_;
  tempsensor_ = tempsensor;
  if (tempsensor) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_set_allocated:daqcs_msp.Data.tempSensor)
}

inline const Data* Data::internal_default_instance() {
  return &Data_default_instance_.get();
}
#endif  // !PROTOBUF_INLINE_NOT_IN_HEADERS

// @@protoc_insertion_point(namespace_scope)

}  // namespace daqcs_msp

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_daqcs_5fmsp_2eproto__INCLUDED
