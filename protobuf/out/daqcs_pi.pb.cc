// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: daqcs_pi.proto

#define INTERNAL_SUPPRESS_PROTOBUF_FIELD_DEPRECATION
#include "daqcs_pi.pb.h"

#include <algorithm>

#include <google/protobuf/stubs/common.h>
#include <google/protobuf/stubs/port.h>
#include <google/protobuf/stubs/once.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/wire_format_lite_inl.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/reflection_ops.h>
#include <google/protobuf/wire_format.h>
// @@protoc_insertion_point(includes)

namespace daqcs_pi {

namespace {

const ::google::protobuf::Descriptor* Data_descriptor_ = NULL;
const ::google::protobuf::internal::GeneratedMessageReflection*
  Data_reflection_ = NULL;

}  // namespace


void protobuf_AssignDesc_daqcs_5fpi_2eproto() GOOGLE_ATTRIBUTE_COLD;
void protobuf_AssignDesc_daqcs_5fpi_2eproto() {
  protobuf_AddDesc_daqcs_5fpi_2eproto();
  const ::google::protobuf::FileDescriptor* file =
    ::google::protobuf::DescriptorPool::generated_pool()->FindFileByName(
      "daqcs_pi.proto");
  GOOGLE_CHECK(file != NULL);
  Data_descriptor_ = file->message_type(0);
  static const int Data_offsets_[3] = {
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(Data, id_),
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(Data, tempsensors_),
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(Data, pressuresensors_),
  };
  Data_reflection_ =
    ::google::protobuf::internal::GeneratedMessageReflection::NewGeneratedMessageReflection(
      Data_descriptor_,
      Data::internal_default_instance(),
      Data_offsets_,
      -1,
      -1,
      -1,
      sizeof(Data),
      GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(Data, _internal_metadata_));
}

namespace {

GOOGLE_PROTOBUF_DECLARE_ONCE(protobuf_AssignDescriptors_once_);
void protobuf_AssignDescriptorsOnce() {
  ::google::protobuf::GoogleOnceInit(&protobuf_AssignDescriptors_once_,
                 &protobuf_AssignDesc_daqcs_5fpi_2eproto);
}

void protobuf_RegisterTypes(const ::std::string&) GOOGLE_ATTRIBUTE_COLD;
void protobuf_RegisterTypes(const ::std::string&) {
  protobuf_AssignDescriptorsOnce();
  ::google::protobuf::MessageFactory::InternalRegisterGeneratedMessage(
      Data_descriptor_, Data::internal_default_instance());
}

}  // namespace

void protobuf_ShutdownFile_daqcs_5fpi_2eproto() {
  Data_default_instance_.Shutdown();
  delete Data_reflection_;
}

void protobuf_InitDefaults_daqcs_5fpi_2eproto_impl() {
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  ::common::protobuf_InitDefaults_common_2eproto();
  Data_default_instance_.DefaultConstruct();
  Data_default_instance_.get_mutable()->InitAsDefaultInstance();
}

GOOGLE_PROTOBUF_DECLARE_ONCE(protobuf_InitDefaults_daqcs_5fpi_2eproto_once_);
void protobuf_InitDefaults_daqcs_5fpi_2eproto() {
  ::google::protobuf::GoogleOnceInit(&protobuf_InitDefaults_daqcs_5fpi_2eproto_once_,
                 &protobuf_InitDefaults_daqcs_5fpi_2eproto_impl);
}
void protobuf_AddDesc_daqcs_5fpi_2eproto_impl() {
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  protobuf_InitDefaults_daqcs_5fpi_2eproto();
  ::google::protobuf::DescriptorPool::InternalAddGeneratedFile(
    "\n\016daqcs_pi.proto\022\010daqcs_pi\032\014common.proto"
    "\"l\n\004Data\022\n\n\002id\030\001 \001(\005\022\'\n\013tempSensors\030\002 \003("
    "\0132\022.common.TempSensor\022/\n\017pressureSensors"
    "\030\003 \003(\0132\026.common.PressureSensorb\006proto3", 158);
  ::google::protobuf::MessageFactory::InternalRegisterGeneratedFile(
    "daqcs_pi.proto", &protobuf_RegisterTypes);
  ::common::protobuf_AddDesc_common_2eproto();
  ::google::protobuf::internal::OnShutdown(&protobuf_ShutdownFile_daqcs_5fpi_2eproto);
}

GOOGLE_PROTOBUF_DECLARE_ONCE(protobuf_AddDesc_daqcs_5fpi_2eproto_once_);
void protobuf_AddDesc_daqcs_5fpi_2eproto() {
  ::google::protobuf::GoogleOnceInit(&protobuf_AddDesc_daqcs_5fpi_2eproto_once_,
                 &protobuf_AddDesc_daqcs_5fpi_2eproto_impl);
}
// Force AddDescriptors() to be called at static initialization time.
struct StaticDescriptorInitializer_daqcs_5fpi_2eproto {
  StaticDescriptorInitializer_daqcs_5fpi_2eproto() {
    protobuf_AddDesc_daqcs_5fpi_2eproto();
  }
} static_descriptor_initializer_daqcs_5fpi_2eproto_;

namespace {

static void MergeFromFail(int line) GOOGLE_ATTRIBUTE_COLD GOOGLE_ATTRIBUTE_NORETURN;
static void MergeFromFail(int line) {
  ::google::protobuf::internal::MergeFromFail(__FILE__, line);
}

}  // namespace


// ===================================================================

#if !defined(_MSC_VER) || _MSC_VER >= 1900
const int Data::kIdFieldNumber;
const int Data::kTempSensorsFieldNumber;
const int Data::kPressureSensorsFieldNumber;
#endif  // !defined(_MSC_VER) || _MSC_VER >= 1900

Data::Data()
  : ::google::protobuf::Message(), _internal_metadata_(NULL) {
  if (this != internal_default_instance()) protobuf_InitDefaults_daqcs_5fpi_2eproto();
  SharedCtor();
  // @@protoc_insertion_point(constructor:daqcs_pi.Data)
}

void Data::InitAsDefaultInstance() {
}

Data::Data(const Data& from)
  : ::google::protobuf::Message(),
    _internal_metadata_(NULL) {
  SharedCtor();
  UnsafeMergeFrom(from);
  // @@protoc_insertion_point(copy_constructor:daqcs_pi.Data)
}

void Data::SharedCtor() {
  id_ = 0;
  _cached_size_ = 0;
}

Data::~Data() {
  // @@protoc_insertion_point(destructor:daqcs_pi.Data)
  SharedDtor();
}

void Data::SharedDtor() {
}

void Data::SetCachedSize(int size) const {
  GOOGLE_SAFE_CONCURRENT_WRITES_BEGIN();
  _cached_size_ = size;
  GOOGLE_SAFE_CONCURRENT_WRITES_END();
}
const ::google::protobuf::Descriptor* Data::descriptor() {
  protobuf_AssignDescriptorsOnce();
  return Data_descriptor_;
}

const Data& Data::default_instance() {
  protobuf_InitDefaults_daqcs_5fpi_2eproto();
  return *internal_default_instance();
}

::google::protobuf::internal::ExplicitlyConstructed<Data> Data_default_instance_;

Data* Data::New(::google::protobuf::Arena* arena) const {
  Data* n = new Data;
  if (arena != NULL) {
    arena->Own(n);
  }
  return n;
}

void Data::Clear() {
// @@protoc_insertion_point(message_clear_start:daqcs_pi.Data)
  id_ = 0;
  tempsensors_.Clear();
  pressuresensors_.Clear();
}

bool Data::MergePartialFromCodedStream(
    ::google::protobuf::io::CodedInputStream* input) {
#define DO_(EXPRESSION) if (!GOOGLE_PREDICT_TRUE(EXPRESSION)) goto failure
  ::google::protobuf::uint32 tag;
  // @@protoc_insertion_point(parse_start:daqcs_pi.Data)
  for (;;) {
    ::std::pair< ::google::protobuf::uint32, bool> p = input->ReadTagWithCutoff(127);
    tag = p.first;
    if (!p.second) goto handle_unusual;
    switch (::google::protobuf::internal::WireFormatLite::GetTagFieldNumber(tag)) {
      // optional int32 id = 1;
      case 1: {
        if (tag == 8) {

          DO_((::google::protobuf::internal::WireFormatLite::ReadPrimitive<
                   ::google::protobuf::int32, ::google::protobuf::internal::WireFormatLite::TYPE_INT32>(
                 input, &id_)));
        } else {
          goto handle_unusual;
        }
        if (input->ExpectTag(18)) goto parse_tempSensors;
        break;
      }

      // repeated .common.TempSensor tempSensors = 2;
      case 2: {
        if (tag == 18) {
         parse_tempSensors:
          DO_(input->IncrementRecursionDepth());
         parse_loop_tempSensors:
          DO_(::google::protobuf::internal::WireFormatLite::ReadMessageNoVirtualNoRecursionDepth(
                input, add_tempsensors()));
        } else {
          goto handle_unusual;
        }
        if (input->ExpectTag(18)) goto parse_loop_tempSensors;
        if (input->ExpectTag(26)) goto parse_loop_pressureSensors;
        input->UnsafeDecrementRecursionDepth();
        break;
      }

      // repeated .common.PressureSensor pressureSensors = 3;
      case 3: {
        if (tag == 26) {
          DO_(input->IncrementRecursionDepth());
         parse_loop_pressureSensors:
          DO_(::google::protobuf::internal::WireFormatLite::ReadMessageNoVirtualNoRecursionDepth(
                input, add_pressuresensors()));
        } else {
          goto handle_unusual;
        }
        if (input->ExpectTag(26)) goto parse_loop_pressureSensors;
        input->UnsafeDecrementRecursionDepth();
        if (input->ExpectAtEnd()) goto success;
        break;
      }

      default: {
      handle_unusual:
        if (tag == 0 ||
            ::google::protobuf::internal::WireFormatLite::GetTagWireType(tag) ==
            ::google::protobuf::internal::WireFormatLite::WIRETYPE_END_GROUP) {
          goto success;
        }
        DO_(::google::protobuf::internal::WireFormatLite::SkipField(input, tag));
        break;
      }
    }
  }
success:
  // @@protoc_insertion_point(parse_success:daqcs_pi.Data)
  return true;
failure:
  // @@protoc_insertion_point(parse_failure:daqcs_pi.Data)
  return false;
#undef DO_
}

void Data::SerializeWithCachedSizes(
    ::google::protobuf::io::CodedOutputStream* output) const {
  // @@protoc_insertion_point(serialize_start:daqcs_pi.Data)
  // optional int32 id = 1;
  if (this->id() != 0) {
    ::google::protobuf::internal::WireFormatLite::WriteInt32(1, this->id(), output);
  }

  // repeated .common.TempSensor tempSensors = 2;
  for (unsigned int i = 0, n = this->tempsensors_size(); i < n; i++) {
    ::google::protobuf::internal::WireFormatLite::WriteMessageMaybeToArray(
      2, this->tempsensors(i), output);
  }

  // repeated .common.PressureSensor pressureSensors = 3;
  for (unsigned int i = 0, n = this->pressuresensors_size(); i < n; i++) {
    ::google::protobuf::internal::WireFormatLite::WriteMessageMaybeToArray(
      3, this->pressuresensors(i), output);
  }

  // @@protoc_insertion_point(serialize_end:daqcs_pi.Data)
}

::google::protobuf::uint8* Data::InternalSerializeWithCachedSizesToArray(
    bool deterministic, ::google::protobuf::uint8* target) const {
  (void)deterministic; // Unused
  // @@protoc_insertion_point(serialize_to_array_start:daqcs_pi.Data)
  // optional int32 id = 1;
  if (this->id() != 0) {
    target = ::google::protobuf::internal::WireFormatLite::WriteInt32ToArray(1, this->id(), target);
  }

  // repeated .common.TempSensor tempSensors = 2;
  for (unsigned int i = 0, n = this->tempsensors_size(); i < n; i++) {
    target = ::google::protobuf::internal::WireFormatLite::
      InternalWriteMessageNoVirtualToArray(
        2, this->tempsensors(i), false, target);
  }

  // repeated .common.PressureSensor pressureSensors = 3;
  for (unsigned int i = 0, n = this->pressuresensors_size(); i < n; i++) {
    target = ::google::protobuf::internal::WireFormatLite::
      InternalWriteMessageNoVirtualToArray(
        3, this->pressuresensors(i), false, target);
  }

  // @@protoc_insertion_point(serialize_to_array_end:daqcs_pi.Data)
  return target;
}

size_t Data::ByteSizeLong() const {
// @@protoc_insertion_point(message_byte_size_start:daqcs_pi.Data)
  size_t total_size = 0;

  // optional int32 id = 1;
  if (this->id() != 0) {
    total_size += 1 +
      ::google::protobuf::internal::WireFormatLite::Int32Size(
        this->id());
  }

  // repeated .common.TempSensor tempSensors = 2;
  {
    unsigned int count = this->tempsensors_size();
    total_size += 1UL * count;
    for (unsigned int i = 0; i < count; i++) {
      total_size +=
        ::google::protobuf::internal::WireFormatLite::MessageSizeNoVirtual(
          this->tempsensors(i));
    }
  }

  // repeated .common.PressureSensor pressureSensors = 3;
  {
    unsigned int count = this->pressuresensors_size();
    total_size += 1UL * count;
    for (unsigned int i = 0; i < count; i++) {
      total_size +=
        ::google::protobuf::internal::WireFormatLite::MessageSizeNoVirtual(
          this->pressuresensors(i));
    }
  }

  int cached_size = ::google::protobuf::internal::ToCachedSize(total_size);
  GOOGLE_SAFE_CONCURRENT_WRITES_BEGIN();
  _cached_size_ = cached_size;
  GOOGLE_SAFE_CONCURRENT_WRITES_END();
  return total_size;
}

void Data::MergeFrom(const ::google::protobuf::Message& from) {
// @@protoc_insertion_point(generalized_merge_from_start:daqcs_pi.Data)
  if (GOOGLE_PREDICT_FALSE(&from == this)) MergeFromFail(__LINE__);
  const Data* source =
      ::google::protobuf::internal::DynamicCastToGenerated<const Data>(
          &from);
  if (source == NULL) {
  // @@protoc_insertion_point(generalized_merge_from_cast_fail:daqcs_pi.Data)
    ::google::protobuf::internal::ReflectionOps::Merge(from, this);
  } else {
  // @@protoc_insertion_point(generalized_merge_from_cast_success:daqcs_pi.Data)
    UnsafeMergeFrom(*source);
  }
}

void Data::MergeFrom(const Data& from) {
// @@protoc_insertion_point(class_specific_merge_from_start:daqcs_pi.Data)
  if (GOOGLE_PREDICT_TRUE(&from != this)) {
    UnsafeMergeFrom(from);
  } else {
    MergeFromFail(__LINE__);
  }
}

void Data::UnsafeMergeFrom(const Data& from) {
  GOOGLE_DCHECK(&from != this);
  tempsensors_.MergeFrom(from.tempsensors_);
  pressuresensors_.MergeFrom(from.pressuresensors_);
  if (from.id() != 0) {
    set_id(from.id());
  }
}

void Data::CopyFrom(const ::google::protobuf::Message& from) {
// @@protoc_insertion_point(generalized_copy_from_start:daqcs_pi.Data)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

void Data::CopyFrom(const Data& from) {
// @@protoc_insertion_point(class_specific_copy_from_start:daqcs_pi.Data)
  if (&from == this) return;
  Clear();
  UnsafeMergeFrom(from);
}

bool Data::IsInitialized() const {

  return true;
}

void Data::Swap(Data* other) {
  if (other == this) return;
  InternalSwap(other);
}
void Data::InternalSwap(Data* other) {
  std::swap(id_, other->id_);
  tempsensors_.UnsafeArenaSwap(&other->tempsensors_);
  pressuresensors_.UnsafeArenaSwap(&other->pressuresensors_);
  _internal_metadata_.Swap(&other->_internal_metadata_);
  std::swap(_cached_size_, other->_cached_size_);
}

::google::protobuf::Metadata Data::GetMetadata() const {
  protobuf_AssignDescriptorsOnce();
  ::google::protobuf::Metadata metadata;
  metadata.descriptor = Data_descriptor_;
  metadata.reflection = Data_reflection_;
  return metadata;
}

#if PROTOBUF_INLINE_NOT_IN_HEADERS
// Data

// optional int32 id = 1;
void Data::clear_id() {
  id_ = 0;
}
::google::protobuf::int32 Data::id() const {
  // @@protoc_insertion_point(field_get:daqcs_pi.Data.id)
  return id_;
}
void Data::set_id(::google::protobuf::int32 value) {
  
  id_ = value;
  // @@protoc_insertion_point(field_set:daqcs_pi.Data.id)
}

// repeated .common.TempSensor tempSensors = 2;
int Data::tempsensors_size() const {
  return tempsensors_.size();
}
void Data::clear_tempsensors() {
  tempsensors_.Clear();
}
const ::common::TempSensor& Data::tempsensors(int index) const {
  // @@protoc_insertion_point(field_get:daqcs_pi.Data.tempSensors)
  return tempsensors_.Get(index);
}
::common::TempSensor* Data::mutable_tempsensors(int index) {
  // @@protoc_insertion_point(field_mutable:daqcs_pi.Data.tempSensors)
  return tempsensors_.Mutable(index);
}
::common::TempSensor* Data::add_tempsensors() {
  // @@protoc_insertion_point(field_add:daqcs_pi.Data.tempSensors)
  return tempsensors_.Add();
}
::google::protobuf::RepeatedPtrField< ::common::TempSensor >*
Data::mutable_tempsensors() {
  // @@protoc_insertion_point(field_mutable_list:daqcs_pi.Data.tempSensors)
  return &tempsensors_;
}
const ::google::protobuf::RepeatedPtrField< ::common::TempSensor >&
Data::tempsensors() const {
  // @@protoc_insertion_point(field_list:daqcs_pi.Data.tempSensors)
  return tempsensors_;
}

// repeated .common.PressureSensor pressureSensors = 3;
int Data::pressuresensors_size() const {
  return pressuresensors_.size();
}
void Data::clear_pressuresensors() {
  pressuresensors_.Clear();
}
const ::common::PressureSensor& Data::pressuresensors(int index) const {
  // @@protoc_insertion_point(field_get:daqcs_pi.Data.pressureSensors)
  return pressuresensors_.Get(index);
}
::common::PressureSensor* Data::mutable_pressuresensors(int index) {
  // @@protoc_insertion_point(field_mutable:daqcs_pi.Data.pressureSensors)
  return pressuresensors_.Mutable(index);
}
::common::PressureSensor* Data::add_pressuresensors() {
  // @@protoc_insertion_point(field_add:daqcs_pi.Data.pressureSensors)
  return pressuresensors_.Add();
}
::google::protobuf::RepeatedPtrField< ::common::PressureSensor >*
Data::mutable_pressuresensors() {
  // @@protoc_insertion_point(field_mutable_list:daqcs_pi.Data.pressureSensors)
  return &pressuresensors_;
}
const ::google::protobuf::RepeatedPtrField< ::common::PressureSensor >&
Data::pressuresensors() const {
  // @@protoc_insertion_point(field_list:daqcs_pi.Data.pressureSensors)
  return pressuresensors_;
}

inline const Data* Data::internal_default_instance() {
  return &Data_default_instance_.get();
}
#endif  // PROTOBUF_INLINE_NOT_IN_HEADERS

// @@protoc_insertion_point(namespace_scope)

}  // namespace daqcs_pi

// @@protoc_insertion_point(global_scope)
