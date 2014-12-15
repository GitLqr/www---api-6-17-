# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: news_feature_msg.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='news_feature_msg.proto',
  package='',
  serialized_pb='\n\x16news_feature_msg.proto\"B\n\tVisitInfo\x12\x10\n\x08pv_count\x18\x01 \x01(\x05\x12\x13\n\x0b\x63lick_count\x18\x02 \x01(\x05\x12\x0e\n\x06weight\x18\x03 \x01(\x01\"3\n\x0bItemFeature\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x01 \x01(\t\x12\x0e\n\x06weight\x18\x02 \x01(\x01\"C\n\x0bUserFeature\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x01 \x01(\t\x12\x1e\n\nvisit_info\x18\x03 \x01(\x0b\x32\n.VisitInfo\"0\n\x0fItemFeatureList\x12\x1d\n\x07\x66\x65\x61ture\x18\x01 \x03(\x0b\x32\x0c.ItemFeature\"0\n\x0fUserFeatureList\x12\x1d\n\x07\x66\x65\x61ture\x18\x01 \x03(\x0b\x32\x0c.UserFeature\"\x1d\n\nItemIdList\x12\x0f\n\x07item_id\x18\x01 \x03(\t\"\xb0\x01\n\x15\x46\x65\x61tureNameItemIdList\x12S\n\x19\x66\x65\x61ture_name_item_id_list\x18\x01 \x03(\x0b\x32\x30.FeatureNameItemIdList.FeatureNameItemIdListItem\x1a\x42\n\x19\x46\x65\x61tureNameItemIdListItem\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x03(\t\"7\n\x10\x46\x65\x61tureNameLimit\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x01 \x01(\t\x12\r\n\x05limit\x18\x02 \x01(\x05\"E\n\x14\x46\x65\x61tureNameLimitList\x12-\n\x12\x66\x65\x61ture_name_limit\x18\x01 \x03(\x0b\x32\x11.FeatureNameLimit\"U\n\x13NewsItemFeatureInfo\x12+\n\x11item_feature_list\x18\x01 \x01(\x0b\x32\x10.ItemFeatureList\x12\x11\n\titem_info\x18\x02 \x01(\t\"`\n\x17NewsItemFeatureInfoList\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x01 \x01(\t\x12/\n\x11item_feature_info\x18\x02 \x03(\x0b\x32\x14.NewsItemFeatureInfo\"E\n\x13NewsFeatureItemList\x12.\n\x0c\x66\x65\x61ture_item\x18\x01 \x03(\x0b\x32\x18.NewsItemFeatureInfoList')




_VISITINFO = _descriptor.Descriptor(
  name='VisitInfo',
  full_name='VisitInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pv_count', full_name='VisitInfo.pv_count', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='click_count', full_name='VisitInfo.click_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weight', full_name='VisitInfo.weight', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=26,
  serialized_end=92,
)


_ITEMFEATURE = _descriptor.Descriptor(
  name='ItemFeature',
  full_name='ItemFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_name', full_name='ItemFeature.feature_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weight', full_name='ItemFeature.weight', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=94,
  serialized_end=145,
)


_USERFEATURE = _descriptor.Descriptor(
  name='UserFeature',
  full_name='UserFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_name', full_name='UserFeature.feature_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='visit_info', full_name='UserFeature.visit_info', index=1,
      number=3, type=11, cpp_type=10, label=1,
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
  extension_ranges=[],
  serialized_start=147,
  serialized_end=214,
)


_ITEMFEATURELIST = _descriptor.Descriptor(
  name='ItemFeatureList',
  full_name='ItemFeatureList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature', full_name='ItemFeatureList.feature', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=216,
  serialized_end=264,
)


_USERFEATURELIST = _descriptor.Descriptor(
  name='UserFeatureList',
  full_name='UserFeatureList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature', full_name='UserFeatureList.feature', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=266,
  serialized_end=314,
)


_ITEMIDLIST = _descriptor.Descriptor(
  name='ItemIdList',
  full_name='ItemIdList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='item_id', full_name='ItemIdList.item_id', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=316,
  serialized_end=345,
)


_FEATURENAMEITEMIDLIST_FEATURENAMEITEMIDLISTITEM = _descriptor.Descriptor(
  name='FeatureNameItemIdListItem',
  full_name='FeatureNameItemIdList.FeatureNameItemIdListItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_name', full_name='FeatureNameItemIdList.FeatureNameItemIdListItem.feature_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item_id', full_name='FeatureNameItemIdList.FeatureNameItemIdListItem.item_id', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=458,
  serialized_end=524,
)

_FEATURENAMEITEMIDLIST = _descriptor.Descriptor(
  name='FeatureNameItemIdList',
  full_name='FeatureNameItemIdList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_name_item_id_list', full_name='FeatureNameItemIdList.feature_name_item_id_list', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_FEATURENAMEITEMIDLIST_FEATURENAMEITEMIDLISTITEM, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=348,
  serialized_end=524,
)


_FEATURENAMELIMIT = _descriptor.Descriptor(
  name='FeatureNameLimit',
  full_name='FeatureNameLimit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_name', full_name='FeatureNameLimit.feature_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='limit', full_name='FeatureNameLimit.limit', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=526,
  serialized_end=581,
)


_FEATURENAMELIMITLIST = _descriptor.Descriptor(
  name='FeatureNameLimitList',
  full_name='FeatureNameLimitList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_name_limit', full_name='FeatureNameLimitList.feature_name_limit', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=583,
  serialized_end=652,
)


_NEWSITEMFEATUREINFO = _descriptor.Descriptor(
  name='NewsItemFeatureInfo',
  full_name='NewsItemFeatureInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='item_feature_list', full_name='NewsItemFeatureInfo.item_feature_list', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item_info', full_name='NewsItemFeatureInfo.item_info', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=654,
  serialized_end=739,
)


_NEWSITEMFEATUREINFOLIST = _descriptor.Descriptor(
  name='NewsItemFeatureInfoList',
  full_name='NewsItemFeatureInfoList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_name', full_name='NewsItemFeatureInfoList.feature_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item_feature_info', full_name='NewsItemFeatureInfoList.item_feature_info', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=741,
  serialized_end=837,
)


_NEWSFEATUREITEMLIST = _descriptor.Descriptor(
  name='NewsFeatureItemList',
  full_name='NewsFeatureItemList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_item', full_name='NewsFeatureItemList.feature_item', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=839,
  serialized_end=908,
)

_USERFEATURE.fields_by_name['visit_info'].message_type = _VISITINFO
_ITEMFEATURELIST.fields_by_name['feature'].message_type = _ITEMFEATURE
_USERFEATURELIST.fields_by_name['feature'].message_type = _USERFEATURE
_FEATURENAMEITEMIDLIST_FEATURENAMEITEMIDLISTITEM.containing_type = _FEATURENAMEITEMIDLIST;
_FEATURENAMEITEMIDLIST.fields_by_name['feature_name_item_id_list'].message_type = _FEATURENAMEITEMIDLIST_FEATURENAMEITEMIDLISTITEM
_FEATURENAMELIMITLIST.fields_by_name['feature_name_limit'].message_type = _FEATURENAMELIMIT
_NEWSITEMFEATUREINFO.fields_by_name['item_feature_list'].message_type = _ITEMFEATURELIST
_NEWSITEMFEATUREINFOLIST.fields_by_name['item_feature_info'].message_type = _NEWSITEMFEATUREINFO
_NEWSFEATUREITEMLIST.fields_by_name['feature_item'].message_type = _NEWSITEMFEATUREINFOLIST
DESCRIPTOR.message_types_by_name['VisitInfo'] = _VISITINFO
DESCRIPTOR.message_types_by_name['ItemFeature'] = _ITEMFEATURE
DESCRIPTOR.message_types_by_name['UserFeature'] = _USERFEATURE
DESCRIPTOR.message_types_by_name['ItemFeatureList'] = _ITEMFEATURELIST
DESCRIPTOR.message_types_by_name['UserFeatureList'] = _USERFEATURELIST
DESCRIPTOR.message_types_by_name['ItemIdList'] = _ITEMIDLIST
DESCRIPTOR.message_types_by_name['FeatureNameItemIdList'] = _FEATURENAMEITEMIDLIST
DESCRIPTOR.message_types_by_name['FeatureNameLimit'] = _FEATURENAMELIMIT
DESCRIPTOR.message_types_by_name['FeatureNameLimitList'] = _FEATURENAMELIMITLIST
DESCRIPTOR.message_types_by_name['NewsItemFeatureInfo'] = _NEWSITEMFEATUREINFO
DESCRIPTOR.message_types_by_name['NewsItemFeatureInfoList'] = _NEWSITEMFEATUREINFOLIST
DESCRIPTOR.message_types_by_name['NewsFeatureItemList'] = _NEWSFEATUREITEMLIST

class VisitInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VISITINFO

  # @@protoc_insertion_point(class_scope:VisitInfo)

class ItemFeature(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ITEMFEATURE

  # @@protoc_insertion_point(class_scope:ItemFeature)

class UserFeature(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _USERFEATURE

  # @@protoc_insertion_point(class_scope:UserFeature)

class ItemFeatureList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ITEMFEATURELIST

  # @@protoc_insertion_point(class_scope:ItemFeatureList)

class UserFeatureList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _USERFEATURELIST

  # @@protoc_insertion_point(class_scope:UserFeatureList)

class ItemIdList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ITEMIDLIST

  # @@protoc_insertion_point(class_scope:ItemIdList)

class FeatureNameItemIdList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class FeatureNameItemIdListItem(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FEATURENAMEITEMIDLIST_FEATURENAMEITEMIDLISTITEM

    # @@protoc_insertion_point(class_scope:FeatureNameItemIdList.FeatureNameItemIdListItem)
  DESCRIPTOR = _FEATURENAMEITEMIDLIST

  # @@protoc_insertion_point(class_scope:FeatureNameItemIdList)

class FeatureNameLimit(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FEATURENAMELIMIT

  # @@protoc_insertion_point(class_scope:FeatureNameLimit)

class FeatureNameLimitList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FEATURENAMELIMITLIST

  # @@protoc_insertion_point(class_scope:FeatureNameLimitList)

class NewsItemFeatureInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NEWSITEMFEATUREINFO

  # @@protoc_insertion_point(class_scope:NewsItemFeatureInfo)

class NewsItemFeatureInfoList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NEWSITEMFEATUREINFOLIST

  # @@protoc_insertion_point(class_scope:NewsItemFeatureInfoList)

class NewsFeatureItemList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NEWSFEATUREITEMLIST

  # @@protoc_insertion_point(class_scope:NewsFeatureItemList)


# @@protoc_insertion_point(module_scope)