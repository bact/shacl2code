//
//
//

package model

import (
    "time"
)


// An Abstract class
type HttpExampleOrgAbstractClassObject struct {
    SHACLObjectBase

}


type HttpExampleOrgAbstractClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgAbstractClassType HttpExampleOrgAbstractClassObjectType

func DecodeHttpExampleOrgAbstractClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgAbstractClass], error) {
    return DecodeRef[HttpExampleOrgAbstractClass](data, path, context, httpExampleOrgAbstractClassType, check)
}

func (self HttpExampleOrgAbstractClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgAbstractClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgAbstractClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgAbstractClassObject(&HttpExampleOrgAbstractClassObject{}, self)
}

func ConstructHttpExampleOrgAbstractClassObject(o *HttpExampleOrgAbstractClassObject, typ SHACLType) *HttpExampleOrgAbstractClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgAbstractClass interface {
    SHACLObject
}



func (self *HttpExampleOrgAbstractClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgAbstractClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgAbstractClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgAbstractClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}
type HttpExampleOrgAbstractShClassObject struct {
    SHACLObjectBase

}


type HttpExampleOrgAbstractShClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgAbstractShClassType HttpExampleOrgAbstractShClassObjectType

func DecodeHttpExampleOrgAbstractShClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgAbstractShClass], error) {
    return DecodeRef[HttpExampleOrgAbstractShClass](data, path, context, httpExampleOrgAbstractShClassType, check)
}

func (self HttpExampleOrgAbstractShClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgAbstractShClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgAbstractShClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgAbstractShClassObject(&HttpExampleOrgAbstractShClassObject{}, self)
}

func ConstructHttpExampleOrgAbstractShClassObject(o *HttpExampleOrgAbstractShClassObject, typ SHACLType) *HttpExampleOrgAbstractShClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgAbstractShClass interface {
    SHACLObject
}



func (self *HttpExampleOrgAbstractShClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgAbstractShClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgAbstractShClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgAbstractShClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// An Abstract class using the SPDX type
type HttpExampleOrgAbstractSpdxClassObject struct {
    SHACLObjectBase

}


type HttpExampleOrgAbstractSpdxClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgAbstractSpdxClassType HttpExampleOrgAbstractSpdxClassObjectType

func DecodeHttpExampleOrgAbstractSpdxClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgAbstractSpdxClass], error) {
    return DecodeRef[HttpExampleOrgAbstractSpdxClass](data, path, context, httpExampleOrgAbstractSpdxClassType, check)
}

func (self HttpExampleOrgAbstractSpdxClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgAbstractSpdxClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgAbstractSpdxClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgAbstractSpdxClassObject(&HttpExampleOrgAbstractSpdxClassObject{}, self)
}

func ConstructHttpExampleOrgAbstractSpdxClassObject(o *HttpExampleOrgAbstractSpdxClassObject, typ SHACLType) *HttpExampleOrgAbstractSpdxClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgAbstractSpdxClass interface {
    SHACLObject
}



func (self *HttpExampleOrgAbstractSpdxClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgAbstractSpdxClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgAbstractSpdxClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgAbstractSpdxClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A concrete class
type HttpExampleOrgConcreteClassObject struct {
    HttpExampleOrgAbstractClassObject

}


type HttpExampleOrgConcreteClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgConcreteClassType HttpExampleOrgConcreteClassObjectType

func DecodeHttpExampleOrgConcreteClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgConcreteClass], error) {
    return DecodeRef[HttpExampleOrgConcreteClass](data, path, context, httpExampleOrgConcreteClassType, check)
}

func (self HttpExampleOrgConcreteClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgConcreteClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgConcreteClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgConcreteClassObject(&HttpExampleOrgConcreteClassObject{}, self)
}

func ConstructHttpExampleOrgConcreteClassObject(o *HttpExampleOrgConcreteClassObject, typ SHACLType) *HttpExampleOrgConcreteClassObject {
    ConstructHttpExampleOrgAbstractClassObject(&o.HttpExampleOrgAbstractClassObject, typ)
    return o
}

type HttpExampleOrgConcreteClass interface {
    HttpExampleOrgAbstractClass
}


func MakeHttpExampleOrgConcreteClass() HttpExampleOrgConcreteClass {
    return ConstructHttpExampleOrgConcreteClassObject(&HttpExampleOrgConcreteClassObject{}, httpExampleOrgConcreteClassType)
}

func MakeHttpExampleOrgConcreteClassRef() Ref[HttpExampleOrgConcreteClass] {
    o := MakeHttpExampleOrgConcreteClass()
    return MakeObjectRef[HttpExampleOrgConcreteClass](o)
}

func (self *HttpExampleOrgConcreteClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgAbstractClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgConcreteClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgAbstractClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgConcreteClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgAbstractClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgConcreteClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgAbstractClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A concrete class
type HttpExampleOrgConcreteShClassObject struct {
    HttpExampleOrgAbstractShClassObject

}


type HttpExampleOrgConcreteShClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgConcreteShClassType HttpExampleOrgConcreteShClassObjectType

func DecodeHttpExampleOrgConcreteShClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgConcreteShClass], error) {
    return DecodeRef[HttpExampleOrgConcreteShClass](data, path, context, httpExampleOrgConcreteShClassType, check)
}

func (self HttpExampleOrgConcreteShClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgConcreteShClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgConcreteShClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgConcreteShClassObject(&HttpExampleOrgConcreteShClassObject{}, self)
}

func ConstructHttpExampleOrgConcreteShClassObject(o *HttpExampleOrgConcreteShClassObject, typ SHACLType) *HttpExampleOrgConcreteShClassObject {
    ConstructHttpExampleOrgAbstractShClassObject(&o.HttpExampleOrgAbstractShClassObject, typ)
    return o
}

type HttpExampleOrgConcreteShClass interface {
    HttpExampleOrgAbstractShClass
}


func MakeHttpExampleOrgConcreteShClass() HttpExampleOrgConcreteShClass {
    return ConstructHttpExampleOrgConcreteShClassObject(&HttpExampleOrgConcreteShClassObject{}, httpExampleOrgConcreteShClassType)
}

func MakeHttpExampleOrgConcreteShClassRef() Ref[HttpExampleOrgConcreteShClass] {
    o := MakeHttpExampleOrgConcreteShClass()
    return MakeObjectRef[HttpExampleOrgConcreteShClass](o)
}

func (self *HttpExampleOrgConcreteShClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgAbstractShClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgConcreteShClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgAbstractShClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgConcreteShClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgAbstractShClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgConcreteShClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgAbstractShClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A concrete class
type HttpExampleOrgConcreteSpdxClassObject struct {
    HttpExampleOrgAbstractSpdxClassObject

}


type HttpExampleOrgConcreteSpdxClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgConcreteSpdxClassType HttpExampleOrgConcreteSpdxClassObjectType

func DecodeHttpExampleOrgConcreteSpdxClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgConcreteSpdxClass], error) {
    return DecodeRef[HttpExampleOrgConcreteSpdxClass](data, path, context, httpExampleOrgConcreteSpdxClassType, check)
}

func (self HttpExampleOrgConcreteSpdxClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgConcreteSpdxClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgConcreteSpdxClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgConcreteSpdxClassObject(&HttpExampleOrgConcreteSpdxClassObject{}, self)
}

func ConstructHttpExampleOrgConcreteSpdxClassObject(o *HttpExampleOrgConcreteSpdxClassObject, typ SHACLType) *HttpExampleOrgConcreteSpdxClassObject {
    ConstructHttpExampleOrgAbstractSpdxClassObject(&o.HttpExampleOrgAbstractSpdxClassObject, typ)
    return o
}

type HttpExampleOrgConcreteSpdxClass interface {
    HttpExampleOrgAbstractSpdxClass
}


func MakeHttpExampleOrgConcreteSpdxClass() HttpExampleOrgConcreteSpdxClass {
    return ConstructHttpExampleOrgConcreteSpdxClassObject(&HttpExampleOrgConcreteSpdxClassObject{}, httpExampleOrgConcreteSpdxClassType)
}

func MakeHttpExampleOrgConcreteSpdxClassRef() Ref[HttpExampleOrgConcreteSpdxClass] {
    o := MakeHttpExampleOrgConcreteSpdxClass()
    return MakeObjectRef[HttpExampleOrgConcreteSpdxClass](o)
}

func (self *HttpExampleOrgConcreteSpdxClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgAbstractSpdxClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgConcreteSpdxClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgAbstractSpdxClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgConcreteSpdxClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgAbstractSpdxClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgConcreteSpdxClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgAbstractSpdxClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// An enumerated type
type HttpExampleOrgEnumTypeObject struct {
    SHACLObjectBase

}

// The bar value of enumType
const HttpExampleOrgEnumTypeBar = "http://example.org/enumType/bar"
// The foo value of enumType
const HttpExampleOrgEnumTypeFoo = "http://example.org/enumType/foo"
// This value has no label
const HttpExampleOrgEnumTypeNolabel = "http://example.org/enumType/nolabel"

type HttpExampleOrgEnumTypeObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgEnumTypeType HttpExampleOrgEnumTypeObjectType

func DecodeHttpExampleOrgEnumType (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgEnumType], error) {
    return DecodeRef[HttpExampleOrgEnumType](data, path, context, httpExampleOrgEnumTypeType, check)
}

func (self HttpExampleOrgEnumTypeObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgEnumType)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgEnumTypeObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgEnumTypeObject(&HttpExampleOrgEnumTypeObject{}, self)
}

func ConstructHttpExampleOrgEnumTypeObject(o *HttpExampleOrgEnumTypeObject, typ SHACLType) *HttpExampleOrgEnumTypeObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgEnumType interface {
    SHACLObject
}


func MakeHttpExampleOrgEnumType() HttpExampleOrgEnumType {
    return ConstructHttpExampleOrgEnumTypeObject(&HttpExampleOrgEnumTypeObject{}, httpExampleOrgEnumTypeType)
}

func MakeHttpExampleOrgEnumTypeRef() Ref[HttpExampleOrgEnumType] {
    o := MakeHttpExampleOrgEnumType()
    return MakeObjectRef[HttpExampleOrgEnumType](o)
}

func (self *HttpExampleOrgEnumTypeObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgEnumTypeObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgEnumTypeObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgEnumTypeObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// An extensible abstract class
type HttpExampleOrgExtensibleAbstractClassObject struct {
    SHACLObjectBase
    SHACLExtensibleBase

}


type HttpExampleOrgExtensibleAbstractClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgExtensibleAbstractClassType HttpExampleOrgExtensibleAbstractClassObjectType

func DecodeHttpExampleOrgExtensibleAbstractClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgExtensibleAbstractClass], error) {
    return DecodeRef[HttpExampleOrgExtensibleAbstractClass](data, path, context, httpExampleOrgExtensibleAbstractClassType, check)
}

func (self HttpExampleOrgExtensibleAbstractClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgExtensibleAbstractClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgExtensibleAbstractClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgExtensibleAbstractClassObject(&HttpExampleOrgExtensibleAbstractClassObject{}, self)
}

func ConstructHttpExampleOrgExtensibleAbstractClassObject(o *HttpExampleOrgExtensibleAbstractClassObject, typ SHACLType) *HttpExampleOrgExtensibleAbstractClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgExtensibleAbstractClass interface {
    SHACLObject
}



func (self *HttpExampleOrgExtensibleAbstractClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgExtensibleAbstractClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgExtensibleAbstractClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgExtensibleAbstractClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    self.SHACLExtensibleBase.EncodeExtProperties(data, path)
    return nil
}

// A class with an ID alias
type HttpExampleOrgIdPropClassObject struct {
    SHACLObjectBase

}


type HttpExampleOrgIdPropClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgIdPropClassType HttpExampleOrgIdPropClassObjectType

func DecodeHttpExampleOrgIdPropClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgIdPropClass], error) {
    return DecodeRef[HttpExampleOrgIdPropClass](data, path, context, httpExampleOrgIdPropClassType, check)
}

func (self HttpExampleOrgIdPropClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgIdPropClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgIdPropClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgIdPropClassObject(&HttpExampleOrgIdPropClassObject{}, self)
}

func ConstructHttpExampleOrgIdPropClassObject(o *HttpExampleOrgIdPropClassObject, typ SHACLType) *HttpExampleOrgIdPropClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgIdPropClass interface {
    SHACLObject
}


func MakeHttpExampleOrgIdPropClass() HttpExampleOrgIdPropClass {
    return ConstructHttpExampleOrgIdPropClassObject(&HttpExampleOrgIdPropClassObject{}, httpExampleOrgIdPropClassType)
}

func MakeHttpExampleOrgIdPropClassRef() Ref[HttpExampleOrgIdPropClass] {
    o := MakeHttpExampleOrgIdPropClass()
    return MakeObjectRef[HttpExampleOrgIdPropClass](o)
}

func (self *HttpExampleOrgIdPropClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgIdPropClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgIdPropClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgIdPropClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class that inherits its idPropertyName from the parent
type HttpExampleOrgInheritedIdPropClassObject struct {
    HttpExampleOrgIdPropClassObject

}


type HttpExampleOrgInheritedIdPropClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgInheritedIdPropClassType HttpExampleOrgInheritedIdPropClassObjectType

func DecodeHttpExampleOrgInheritedIdPropClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgInheritedIdPropClass], error) {
    return DecodeRef[HttpExampleOrgInheritedIdPropClass](data, path, context, httpExampleOrgInheritedIdPropClassType, check)
}

func (self HttpExampleOrgInheritedIdPropClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgInheritedIdPropClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgInheritedIdPropClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgInheritedIdPropClassObject(&HttpExampleOrgInheritedIdPropClassObject{}, self)
}

func ConstructHttpExampleOrgInheritedIdPropClassObject(o *HttpExampleOrgInheritedIdPropClassObject, typ SHACLType) *HttpExampleOrgInheritedIdPropClassObject {
    ConstructHttpExampleOrgIdPropClassObject(&o.HttpExampleOrgIdPropClassObject, typ)
    return o
}

type HttpExampleOrgInheritedIdPropClass interface {
    HttpExampleOrgIdPropClass
}


func MakeHttpExampleOrgInheritedIdPropClass() HttpExampleOrgInheritedIdPropClass {
    return ConstructHttpExampleOrgInheritedIdPropClassObject(&HttpExampleOrgInheritedIdPropClassObject{}, httpExampleOrgInheritedIdPropClassType)
}

func MakeHttpExampleOrgInheritedIdPropClassRef() Ref[HttpExampleOrgInheritedIdPropClass] {
    o := MakeHttpExampleOrgInheritedIdPropClass()
    return MakeObjectRef[HttpExampleOrgInheritedIdPropClass](o)
}

func (self *HttpExampleOrgInheritedIdPropClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgIdPropClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgInheritedIdPropClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgIdPropClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgInheritedIdPropClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgIdPropClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgInheritedIdPropClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgIdPropClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class to test links
type HttpExampleOrgLinkClassObject struct {
    SHACLObjectBase

    // A link to an extensible-class
    extensible RefProperty[HttpExampleOrgExtensibleClass]
    // A link-class list property
    linkListProp RefListProperty[HttpExampleOrgLinkClass]
    // A link-class property
    linkProp RefProperty[HttpExampleOrgLinkClass]
    // A link-class property with no sh:class
    linkPropNoClass RefProperty[HttpExampleOrgLinkClass]
    // Tag used to identify object for testing
    tag Property[string]
}


type HttpExampleOrgLinkClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgLinkClassType HttpExampleOrgLinkClassObjectType
var httpExampleOrgLinkClassExtensibleContext = map[string]string{}
var httpExampleOrgLinkClassLinkListPropContext = map[string]string{}
var httpExampleOrgLinkClassLinkPropContext = map[string]string{}
var httpExampleOrgLinkClassLinkPropNoClassContext = map[string]string{}
var httpExampleOrgLinkClassTagContext = map[string]string{}

func DecodeHttpExampleOrgLinkClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgLinkClass], error) {
    return DecodeRef[HttpExampleOrgLinkClass](data, path, context, httpExampleOrgLinkClassType, check)
}

func (self HttpExampleOrgLinkClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgLinkClass)
    _ = obj
    switch name {
    case "http://example.org/link-class-extensible":
        val, err := DecodeHttpExampleOrgExtensibleClass(value, path, httpExampleOrgLinkClassExtensibleContext, obj.Extensible())
        if err != nil {
            return false, err
        }
        err = obj.Extensible().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/link-class-link-list-prop":
        val, err := DecodeList[Ref[HttpExampleOrgLinkClass]](value, path, httpExampleOrgLinkClassLinkListPropContext, DecodeHttpExampleOrgLinkClass, obj.LinkListProp())
        if err != nil {
            return false, err
        }
        err = obj.LinkListProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/link-class-link-prop":
        val, err := DecodeHttpExampleOrgLinkClass(value, path, httpExampleOrgLinkClassLinkPropContext, obj.LinkProp())
        if err != nil {
            return false, err
        }
        err = obj.LinkProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/link-class-link-prop-no-class":
        val, err := DecodeHttpExampleOrgLinkClass(value, path, httpExampleOrgLinkClassLinkPropNoClassContext, obj.LinkPropNoClass())
        if err != nil {
            return false, err
        }
        err = obj.LinkPropNoClass().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/link-class-tag":
        val, err := DecodeString(value, path, httpExampleOrgLinkClassTagContext, obj.Tag())
        if err != nil {
            return false, err
        }
        err = obj.Tag().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgLinkClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgLinkClassObject(&HttpExampleOrgLinkClassObject{}, self)
}

func ConstructHttpExampleOrgLinkClassObject(o *HttpExampleOrgLinkClassObject, typ SHACLType) *HttpExampleOrgLinkClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    {
        validators := []Validator[Ref[HttpExampleOrgExtensibleClass]]{}
        decodeValidators := []Validator[any]{}
        o.extensible = NewRefProperty[HttpExampleOrgExtensibleClass]("extensible", validators, decodeValidators)
    }
    {
        validators := []Validator[Ref[HttpExampleOrgLinkClass]]{}
        decodeValidators := []Validator[any]{}
        o.linkListProp = NewRefListProperty[HttpExampleOrgLinkClass]("linkListProp", validators, decodeValidators)
    }
    {
        validators := []Validator[Ref[HttpExampleOrgLinkClass]]{}
        decodeValidators := []Validator[any]{}
        o.linkProp = NewRefProperty[HttpExampleOrgLinkClass]("linkProp", validators, decodeValidators)
    }
    {
        validators := []Validator[Ref[HttpExampleOrgLinkClass]]{}
        decodeValidators := []Validator[any]{}
        o.linkPropNoClass = NewRefProperty[HttpExampleOrgLinkClass]("linkPropNoClass", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.tag = NewProperty[string]("tag", validators, decodeValidators)
    }
    return o
}

type HttpExampleOrgLinkClass interface {
    SHACLObject
    Extensible() RefPropertyInterface[HttpExampleOrgExtensibleClass]
    LinkListProp() ListPropertyInterface[Ref[HttpExampleOrgLinkClass]]
    LinkProp() RefPropertyInterface[HttpExampleOrgLinkClass]
    LinkPropNoClass() RefPropertyInterface[HttpExampleOrgLinkClass]
    Tag() PropertyInterface[string]
}


func MakeHttpExampleOrgLinkClass() HttpExampleOrgLinkClass {
    return ConstructHttpExampleOrgLinkClassObject(&HttpExampleOrgLinkClassObject{}, httpExampleOrgLinkClassType)
}

func MakeHttpExampleOrgLinkClassRef() Ref[HttpExampleOrgLinkClass] {
    o := MakeHttpExampleOrgLinkClass()
    return MakeObjectRef[HttpExampleOrgLinkClass](o)
}

func (self *HttpExampleOrgLinkClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    {
        prop_path := path.PushPath("extensible")
        if ! self.extensible.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("linkListProp")
        if ! self.linkListProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("linkProp")
        if ! self.linkProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("linkPropNoClass")
        if ! self.linkPropNoClass.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("tag")
        if ! self.tag.Check(prop_path, handler) {
            valid = false
        }
    }
    return valid
}

func (self *HttpExampleOrgLinkClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
    self.extensible.Walk(path, visit)
    self.linkListProp.Walk(path, visit)
    self.linkProp.Walk(path, visit)
    self.linkPropNoClass.Walk(path, visit)
    self.tag.Walk(path, visit)
}

func (self *HttpExampleOrgLinkClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    if err := self.extensible.Link(state); err != nil {
        return err
    }
    if err := self.linkListProp.Link(state); err != nil {
        return err
    }
    if err := self.linkProp.Link(state); err != nil {
        return err
    }
    if err := self.linkPropNoClass.Link(state); err != nil {
        return err
    }
    if err := self.tag.Link(state); err != nil {
        return err
    }
    return nil
}


func (self *HttpExampleOrgLinkClassObject) Extensible() RefPropertyInterface[HttpExampleOrgExtensibleClass] { return &self.extensible }
func (self *HttpExampleOrgLinkClassObject) LinkListProp() ListPropertyInterface[Ref[HttpExampleOrgLinkClass]] { return &self.linkListProp }
func (self *HttpExampleOrgLinkClassObject) LinkProp() RefPropertyInterface[HttpExampleOrgLinkClass] { return &self.linkProp }
func (self *HttpExampleOrgLinkClassObject) LinkPropNoClass() RefPropertyInterface[HttpExampleOrgLinkClass] { return &self.linkPropNoClass }
func (self *HttpExampleOrgLinkClassObject) Tag() PropertyInterface[string] { return &self.tag }

func (self *HttpExampleOrgLinkClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    if self.extensible.IsSet() {
        val, err := EncodeRef[HttpExampleOrgExtensibleClass](self.extensible.Get(), path.PushPath("extensible"), httpExampleOrgLinkClassExtensibleContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/link-class-extensible"] = val
    }
    if self.linkListProp.IsSet() {
        val, err := EncodeList[Ref[HttpExampleOrgLinkClass]](self.linkListProp.Get(), path.PushPath("linkListProp"), httpExampleOrgLinkClassLinkListPropContext, state, EncodeRef[HttpExampleOrgLinkClass])
        if err != nil {
            return err
        }
        data["http://example.org/link-class-link-list-prop"] = val
    }
    if self.linkProp.IsSet() {
        val, err := EncodeRef[HttpExampleOrgLinkClass](self.linkProp.Get(), path.PushPath("linkProp"), httpExampleOrgLinkClassLinkPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/link-class-link-prop"] = val
    }
    if self.linkPropNoClass.IsSet() {
        val, err := EncodeRef[HttpExampleOrgLinkClass](self.linkPropNoClass.Get(), path.PushPath("linkPropNoClass"), httpExampleOrgLinkClassLinkPropNoClassContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/link-class-link-prop-no-class"] = val
    }
    if self.tag.IsSet() {
        val, err := EncodeString(self.tag.Get(), path.PushPath("tag"), httpExampleOrgLinkClassTagContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/link-class-tag"] = val
    }
    return nil
}

// A class derived from link-class
type HttpExampleOrgLinkDerivedClassObject struct {
    HttpExampleOrgLinkClassObject

}


type HttpExampleOrgLinkDerivedClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgLinkDerivedClassType HttpExampleOrgLinkDerivedClassObjectType

func DecodeHttpExampleOrgLinkDerivedClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgLinkDerivedClass], error) {
    return DecodeRef[HttpExampleOrgLinkDerivedClass](data, path, context, httpExampleOrgLinkDerivedClassType, check)
}

func (self HttpExampleOrgLinkDerivedClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgLinkDerivedClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgLinkDerivedClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgLinkDerivedClassObject(&HttpExampleOrgLinkDerivedClassObject{}, self)
}

func ConstructHttpExampleOrgLinkDerivedClassObject(o *HttpExampleOrgLinkDerivedClassObject, typ SHACLType) *HttpExampleOrgLinkDerivedClassObject {
    ConstructHttpExampleOrgLinkClassObject(&o.HttpExampleOrgLinkClassObject, typ)
    return o
}

type HttpExampleOrgLinkDerivedClass interface {
    HttpExampleOrgLinkClass
}


func MakeHttpExampleOrgLinkDerivedClass() HttpExampleOrgLinkDerivedClass {
    return ConstructHttpExampleOrgLinkDerivedClassObject(&HttpExampleOrgLinkDerivedClassObject{}, httpExampleOrgLinkDerivedClassType)
}

func MakeHttpExampleOrgLinkDerivedClassRef() Ref[HttpExampleOrgLinkDerivedClass] {
    o := MakeHttpExampleOrgLinkDerivedClass()
    return MakeObjectRef[HttpExampleOrgLinkDerivedClass](o)
}

func (self *HttpExampleOrgLinkDerivedClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgLinkClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgLinkDerivedClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgLinkClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgLinkDerivedClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgLinkClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgLinkDerivedClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgLinkClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class that must be a blank node
type HttpExampleOrgNodeKindBlankObject struct {
    HttpExampleOrgLinkClassObject

}


type HttpExampleOrgNodeKindBlankObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgNodeKindBlankType HttpExampleOrgNodeKindBlankObjectType

func DecodeHttpExampleOrgNodeKindBlank (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgNodeKindBlank], error) {
    return DecodeRef[HttpExampleOrgNodeKindBlank](data, path, context, httpExampleOrgNodeKindBlankType, check)
}

func (self HttpExampleOrgNodeKindBlankObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgNodeKindBlank)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgNodeKindBlankObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgNodeKindBlankObject(&HttpExampleOrgNodeKindBlankObject{}, self)
}

func ConstructHttpExampleOrgNodeKindBlankObject(o *HttpExampleOrgNodeKindBlankObject, typ SHACLType) *HttpExampleOrgNodeKindBlankObject {
    ConstructHttpExampleOrgLinkClassObject(&o.HttpExampleOrgLinkClassObject, typ)
    return o
}

type HttpExampleOrgNodeKindBlank interface {
    HttpExampleOrgLinkClass
}


func MakeHttpExampleOrgNodeKindBlank() HttpExampleOrgNodeKindBlank {
    return ConstructHttpExampleOrgNodeKindBlankObject(&HttpExampleOrgNodeKindBlankObject{}, httpExampleOrgNodeKindBlankType)
}

func MakeHttpExampleOrgNodeKindBlankRef() Ref[HttpExampleOrgNodeKindBlank] {
    o := MakeHttpExampleOrgNodeKindBlank()
    return MakeObjectRef[HttpExampleOrgNodeKindBlank](o)
}

func (self *HttpExampleOrgNodeKindBlankObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgLinkClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgNodeKindBlankObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgLinkClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgNodeKindBlankObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgLinkClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgNodeKindBlankObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgLinkClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class that must be an IRI
type HttpExampleOrgNodeKindIriObject struct {
    HttpExampleOrgLinkClassObject

}


type HttpExampleOrgNodeKindIriObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgNodeKindIriType HttpExampleOrgNodeKindIriObjectType

func DecodeHttpExampleOrgNodeKindIri (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgNodeKindIri], error) {
    return DecodeRef[HttpExampleOrgNodeKindIri](data, path, context, httpExampleOrgNodeKindIriType, check)
}

func (self HttpExampleOrgNodeKindIriObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgNodeKindIri)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgNodeKindIriObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgNodeKindIriObject(&HttpExampleOrgNodeKindIriObject{}, self)
}

func ConstructHttpExampleOrgNodeKindIriObject(o *HttpExampleOrgNodeKindIriObject, typ SHACLType) *HttpExampleOrgNodeKindIriObject {
    ConstructHttpExampleOrgLinkClassObject(&o.HttpExampleOrgLinkClassObject, typ)
    return o
}

type HttpExampleOrgNodeKindIri interface {
    HttpExampleOrgLinkClass
}


func MakeHttpExampleOrgNodeKindIri() HttpExampleOrgNodeKindIri {
    return ConstructHttpExampleOrgNodeKindIriObject(&HttpExampleOrgNodeKindIriObject{}, httpExampleOrgNodeKindIriType)
}

func MakeHttpExampleOrgNodeKindIriRef() Ref[HttpExampleOrgNodeKindIri] {
    o := MakeHttpExampleOrgNodeKindIri()
    return MakeObjectRef[HttpExampleOrgNodeKindIri](o)
}

func (self *HttpExampleOrgNodeKindIriObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgLinkClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgNodeKindIriObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgLinkClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgNodeKindIriObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgLinkClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgNodeKindIriObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgLinkClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class that can be either a blank node or an IRI
type HttpExampleOrgNodeKindIriOrBlankObject struct {
    HttpExampleOrgLinkClassObject

}


type HttpExampleOrgNodeKindIriOrBlankObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgNodeKindIriOrBlankType HttpExampleOrgNodeKindIriOrBlankObjectType

func DecodeHttpExampleOrgNodeKindIriOrBlank (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgNodeKindIriOrBlank], error) {
    return DecodeRef[HttpExampleOrgNodeKindIriOrBlank](data, path, context, httpExampleOrgNodeKindIriOrBlankType, check)
}

func (self HttpExampleOrgNodeKindIriOrBlankObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgNodeKindIriOrBlank)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgNodeKindIriOrBlankObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgNodeKindIriOrBlankObject(&HttpExampleOrgNodeKindIriOrBlankObject{}, self)
}

func ConstructHttpExampleOrgNodeKindIriOrBlankObject(o *HttpExampleOrgNodeKindIriOrBlankObject, typ SHACLType) *HttpExampleOrgNodeKindIriOrBlankObject {
    ConstructHttpExampleOrgLinkClassObject(&o.HttpExampleOrgLinkClassObject, typ)
    return o
}

type HttpExampleOrgNodeKindIriOrBlank interface {
    HttpExampleOrgLinkClass
}


func MakeHttpExampleOrgNodeKindIriOrBlank() HttpExampleOrgNodeKindIriOrBlank {
    return ConstructHttpExampleOrgNodeKindIriOrBlankObject(&HttpExampleOrgNodeKindIriOrBlankObject{}, httpExampleOrgNodeKindIriOrBlankType)
}

func MakeHttpExampleOrgNodeKindIriOrBlankRef() Ref[HttpExampleOrgNodeKindIriOrBlank] {
    o := MakeHttpExampleOrgNodeKindIriOrBlank()
    return MakeObjectRef[HttpExampleOrgNodeKindIriOrBlank](o)
}

func (self *HttpExampleOrgNodeKindIriOrBlankObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgLinkClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgNodeKindIriOrBlankObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgLinkClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgNodeKindIriOrBlankObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgLinkClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgNodeKindIriOrBlankObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgLinkClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class that is not a nodeshape
type HttpExampleOrgNonShapeClassObject struct {
    SHACLObjectBase

}


type HttpExampleOrgNonShapeClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgNonShapeClassType HttpExampleOrgNonShapeClassObjectType

func DecodeHttpExampleOrgNonShapeClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgNonShapeClass], error) {
    return DecodeRef[HttpExampleOrgNonShapeClass](data, path, context, httpExampleOrgNonShapeClassType, check)
}

func (self HttpExampleOrgNonShapeClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgNonShapeClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgNonShapeClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgNonShapeClassObject(&HttpExampleOrgNonShapeClassObject{}, self)
}

func ConstructHttpExampleOrgNonShapeClassObject(o *HttpExampleOrgNonShapeClassObject, typ SHACLType) *HttpExampleOrgNonShapeClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgNonShapeClass interface {
    SHACLObject
}


func MakeHttpExampleOrgNonShapeClass() HttpExampleOrgNonShapeClass {
    return ConstructHttpExampleOrgNonShapeClassObject(&HttpExampleOrgNonShapeClassObject{}, httpExampleOrgNonShapeClassType)
}

func MakeHttpExampleOrgNonShapeClassRef() Ref[HttpExampleOrgNonShapeClass] {
    o := MakeHttpExampleOrgNonShapeClass()
    return MakeObjectRef[HttpExampleOrgNonShapeClass](o)
}

func (self *HttpExampleOrgNonShapeClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgNonShapeClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgNonShapeClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgNonShapeClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// The parent class
type HttpExampleOrgParentClassObject struct {
    SHACLObjectBase

}


type HttpExampleOrgParentClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgParentClassType HttpExampleOrgParentClassObjectType

func DecodeHttpExampleOrgParentClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgParentClass], error) {
    return DecodeRef[HttpExampleOrgParentClass](data, path, context, httpExampleOrgParentClassType, check)
}

func (self HttpExampleOrgParentClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgParentClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgParentClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgParentClassObject(&HttpExampleOrgParentClassObject{}, self)
}

func ConstructHttpExampleOrgParentClassObject(o *HttpExampleOrgParentClassObject, typ SHACLType) *HttpExampleOrgParentClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgParentClass interface {
    SHACLObject
}


func MakeHttpExampleOrgParentClass() HttpExampleOrgParentClass {
    return ConstructHttpExampleOrgParentClassObject(&HttpExampleOrgParentClassObject{}, httpExampleOrgParentClassType)
}

func MakeHttpExampleOrgParentClassRef() Ref[HttpExampleOrgParentClass] {
    o := MakeHttpExampleOrgParentClass()
    return MakeObjectRef[HttpExampleOrgParentClass](o)
}

func (self *HttpExampleOrgParentClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgParentClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgParentClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgParentClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class with a mandatory abstract class
type HttpExampleOrgRequiredAbstractObject struct {
    SHACLObjectBase

    // A required abstract class property
    abstractClassProp RefProperty[HttpExampleOrgAbstractClass]
}


type HttpExampleOrgRequiredAbstractObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgRequiredAbstractType HttpExampleOrgRequiredAbstractObjectType
var httpExampleOrgRequiredAbstractAbstractClassPropContext = map[string]string{}

func DecodeHttpExampleOrgRequiredAbstract (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgRequiredAbstract], error) {
    return DecodeRef[HttpExampleOrgRequiredAbstract](data, path, context, httpExampleOrgRequiredAbstractType, check)
}

func (self HttpExampleOrgRequiredAbstractObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgRequiredAbstract)
    _ = obj
    switch name {
    case "http://example.org/required-abstract/abstract-class-prop":
        val, err := DecodeHttpExampleOrgAbstractClass(value, path, httpExampleOrgRequiredAbstractAbstractClassPropContext, obj.AbstractClassProp())
        if err != nil {
            return false, err
        }
        err = obj.AbstractClassProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgRequiredAbstractObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgRequiredAbstractObject(&HttpExampleOrgRequiredAbstractObject{}, self)
}

func ConstructHttpExampleOrgRequiredAbstractObject(o *HttpExampleOrgRequiredAbstractObject, typ SHACLType) *HttpExampleOrgRequiredAbstractObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    {
        validators := []Validator[Ref[HttpExampleOrgAbstractClass]]{}
        decodeValidators := []Validator[any]{}
        o.abstractClassProp = NewRefProperty[HttpExampleOrgAbstractClass]("abstractClassProp", validators, decodeValidators)
    }
    return o
}

type HttpExampleOrgRequiredAbstract interface {
    SHACLObject
    AbstractClassProp() RefPropertyInterface[HttpExampleOrgAbstractClass]
}


func MakeHttpExampleOrgRequiredAbstract() HttpExampleOrgRequiredAbstract {
    return ConstructHttpExampleOrgRequiredAbstractObject(&HttpExampleOrgRequiredAbstractObject{}, httpExampleOrgRequiredAbstractType)
}

func MakeHttpExampleOrgRequiredAbstractRef() Ref[HttpExampleOrgRequiredAbstract] {
    o := MakeHttpExampleOrgRequiredAbstract()
    return MakeObjectRef[HttpExampleOrgRequiredAbstract](o)
}

func (self *HttpExampleOrgRequiredAbstractObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    {
        prop_path := path.PushPath("abstractClassProp")
        if ! self.abstractClassProp.Check(prop_path, handler) {
            valid = false
        }
        if ! self.abstractClassProp.IsSet() {
            if handler != nil {
                handler.HandleError(&ValidationError{"abstractClassProp", "Value is required"}, prop_path)
            }
            valid = false
        }
    }
    return valid
}

func (self *HttpExampleOrgRequiredAbstractObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
    self.abstractClassProp.Walk(path, visit)
}

func (self *HttpExampleOrgRequiredAbstractObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    if err := self.abstractClassProp.Link(state); err != nil {
        return err
    }
    return nil
}


func (self *HttpExampleOrgRequiredAbstractObject) AbstractClassProp() RefPropertyInterface[HttpExampleOrgAbstractClass] { return &self.abstractClassProp }

func (self *HttpExampleOrgRequiredAbstractObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    if self.abstractClassProp.IsSet() {
        val, err := EncodeRef[HttpExampleOrgAbstractClass](self.abstractClassProp.Get(), path.PushPath("abstractClassProp"), httpExampleOrgRequiredAbstractAbstractClassPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/required-abstract/abstract-class-prop"] = val
    }
    return nil
}

// Another class
type HttpExampleOrgTestAnotherClassObject struct {
    SHACLObjectBase

}


type HttpExampleOrgTestAnotherClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgTestAnotherClassType HttpExampleOrgTestAnotherClassObjectType

func DecodeHttpExampleOrgTestAnotherClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgTestAnotherClass], error) {
    return DecodeRef[HttpExampleOrgTestAnotherClass](data, path, context, httpExampleOrgTestAnotherClassType, check)
}

func (self HttpExampleOrgTestAnotherClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgTestAnotherClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgTestAnotherClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgTestAnotherClassObject(&HttpExampleOrgTestAnotherClassObject{}, self)
}

func ConstructHttpExampleOrgTestAnotherClassObject(o *HttpExampleOrgTestAnotherClassObject, typ SHACLType) *HttpExampleOrgTestAnotherClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    return o
}

type HttpExampleOrgTestAnotherClass interface {
    SHACLObject
}


func MakeHttpExampleOrgTestAnotherClass() HttpExampleOrgTestAnotherClass {
    return ConstructHttpExampleOrgTestAnotherClassObject(&HttpExampleOrgTestAnotherClassObject{}, httpExampleOrgTestAnotherClassType)
}

func MakeHttpExampleOrgTestAnotherClassRef() Ref[HttpExampleOrgTestAnotherClass] {
    o := MakeHttpExampleOrgTestAnotherClass()
    return MakeObjectRef[HttpExampleOrgTestAnotherClass](o)
}

func (self *HttpExampleOrgTestAnotherClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgTestAnotherClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
}

func (self *HttpExampleOrgTestAnotherClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgTestAnotherClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// The test class
type HttpExampleOrgTestClassObject struct {
    HttpExampleOrgParentClassObject

    // A property that conflicts with an existing SHACLObject property
    encode Property[string]
    // A property that is a keyword
    import_ Property[string]
    // a URI
    anyuriProp Property[string]
    // a boolean property
    booleanProp Property[bool]
    // A test-class list property
    classListProp RefListProperty[HttpExampleOrgTestClass]
    // A test-class property
    classProp RefProperty[HttpExampleOrgTestClass]
    // A test-class property with no sh:class
    classPropNoClass RefProperty[HttpExampleOrgTestClass]
    // A datetime list property
    datetimeListProp ListProperty[time.Time]
    // A scalar datetime property
    datetimeScalarProp Property[time.Time]
    // A scalar dateTimeStamp property
    datetimestampScalarProp Property[time.Time]
    // A enum list property
    enumListProp ListProperty[string]
    // A enum property
    enumProp Property[string]
    // A enum property with no sh:class
    enumPropNoClass Property[string]
    // a float property
    floatProp Property[float64]
    // a non-negative integer
    integerProp Property[int]
    // A named property
    namedProperty Property[string]
    // A class with no shape
    nonShape RefProperty[HttpExampleOrgNonShapeClass]
    // a non-negative integer
    nonnegativeIntegerProp Property[int]
    // A positive integer
    positiveIntegerProp Property[int]
    // A regex validated string
    regex Property[string]
    // A regex dateTime
    regexDatetime Property[time.Time]
    // A regex dateTimeStamp
    regexDatetimestamp Property[time.Time]
    // A regex validated string list
    regexList ListProperty[string]
    // A string list property with no sh:datatype
    stringListNoDatatype ListProperty[string]
    // A string list property
    stringListProp ListProperty[string]
    // A scalar string propery
    stringScalarProp Property[string]
}
const HttpExampleOrgTestClassNamed = "http://example.org/test-class/named"

type HttpExampleOrgTestClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgTestClassType HttpExampleOrgTestClassObjectType
var httpExampleOrgTestClassEncodeContext = map[string]string{}
var httpExampleOrgTestClassImportContext = map[string]string{}
var httpExampleOrgTestClassAnyuriPropContext = map[string]string{}
var httpExampleOrgTestClassBooleanPropContext = map[string]string{}
var httpExampleOrgTestClassClassListPropContext = map[string]string{}
var httpExampleOrgTestClassClassPropContext = map[string]string{}
var httpExampleOrgTestClassClassPropNoClassContext = map[string]string{}
var httpExampleOrgTestClassDatetimeListPropContext = map[string]string{}
var httpExampleOrgTestClassDatetimeScalarPropContext = map[string]string{}
var httpExampleOrgTestClassDatetimestampScalarPropContext = map[string]string{}
var httpExampleOrgTestClassEnumListPropContext = map[string]string{
    "http://example.org/enumType/bar": "http://example.org/enumType/bar",
    "http://example.org/enumType/foo": "http://example.org/enumType/foo",
    "http://example.org/enumType/nolabel": "http://example.org/enumType/nolabel",
    "http://example.org/enumType/non-named-individual": "http://example.org/enumType/non-named-individual",}
var httpExampleOrgTestClassEnumPropContext = map[string]string{
    "http://example.org/enumType/bar": "http://example.org/enumType/bar",
    "http://example.org/enumType/foo": "http://example.org/enumType/foo",
    "http://example.org/enumType/nolabel": "http://example.org/enumType/nolabel",
    "http://example.org/enumType/non-named-individual": "http://example.org/enumType/non-named-individual",}
var httpExampleOrgTestClassEnumPropNoClassContext = map[string]string{
    "http://example.org/enumType/bar": "http://example.org/enumType/bar",
    "http://example.org/enumType/foo": "http://example.org/enumType/foo",
    "http://example.org/enumType/nolabel": "http://example.org/enumType/nolabel",
    "http://example.org/enumType/non-named-individual": "http://example.org/enumType/non-named-individual",}
var httpExampleOrgTestClassFloatPropContext = map[string]string{}
var httpExampleOrgTestClassIntegerPropContext = map[string]string{}
var httpExampleOrgTestClassNamedPropertyContext = map[string]string{}
var httpExampleOrgTestClassNonShapeContext = map[string]string{}
var httpExampleOrgTestClassNonnegativeIntegerPropContext = map[string]string{}
var httpExampleOrgTestClassPositiveIntegerPropContext = map[string]string{}
var httpExampleOrgTestClassRegexContext = map[string]string{}
var httpExampleOrgTestClassRegexDatetimeContext = map[string]string{}
var httpExampleOrgTestClassRegexDatetimestampContext = map[string]string{}
var httpExampleOrgTestClassRegexListContext = map[string]string{}
var httpExampleOrgTestClassStringListNoDatatypeContext = map[string]string{}
var httpExampleOrgTestClassStringListPropContext = map[string]string{}
var httpExampleOrgTestClassStringScalarPropContext = map[string]string{}

func DecodeHttpExampleOrgTestClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgTestClass], error) {
    return DecodeRef[HttpExampleOrgTestClass](data, path, context, httpExampleOrgTestClassType, check)
}

func (self HttpExampleOrgTestClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgTestClass)
    _ = obj
    switch name {
    case "http://example.org/encode":
        val, err := DecodeString(value, path, httpExampleOrgTestClassEncodeContext, obj.Encode())
        if err != nil {
            return false, err
        }
        err = obj.Encode().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/import":
        val, err := DecodeString(value, path, httpExampleOrgTestClassImportContext, obj.Import())
        if err != nil {
            return false, err
        }
        err = obj.Import().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/anyuri-prop":
        val, err := DecodeString(value, path, httpExampleOrgTestClassAnyuriPropContext, obj.AnyuriProp())
        if err != nil {
            return false, err
        }
        err = obj.AnyuriProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/boolean-prop":
        val, err := DecodeBoolean(value, path, httpExampleOrgTestClassBooleanPropContext, obj.BooleanProp())
        if err != nil {
            return false, err
        }
        err = obj.BooleanProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/class-list-prop":
        val, err := DecodeList[Ref[HttpExampleOrgTestClass]](value, path, httpExampleOrgTestClassClassListPropContext, DecodeHttpExampleOrgTestClass, obj.ClassListProp())
        if err != nil {
            return false, err
        }
        err = obj.ClassListProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/class-prop":
        val, err := DecodeHttpExampleOrgTestClass(value, path, httpExampleOrgTestClassClassPropContext, obj.ClassProp())
        if err != nil {
            return false, err
        }
        err = obj.ClassProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/class-prop-no-class":
        val, err := DecodeHttpExampleOrgTestClass(value, path, httpExampleOrgTestClassClassPropNoClassContext, obj.ClassPropNoClass())
        if err != nil {
            return false, err
        }
        err = obj.ClassPropNoClass().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/datetime-list-prop":
        val, err := DecodeList[time.Time](value, path, httpExampleOrgTestClassDatetimeListPropContext, DecodeDateTime, obj.DatetimeListProp())
        if err != nil {
            return false, err
        }
        err = obj.DatetimeListProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/datetime-scalar-prop":
        val, err := DecodeDateTime(value, path, httpExampleOrgTestClassDatetimeScalarPropContext, obj.DatetimeScalarProp())
        if err != nil {
            return false, err
        }
        err = obj.DatetimeScalarProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/datetimestamp-scalar-prop":
        val, err := DecodeDateTimeStamp(value, path, httpExampleOrgTestClassDatetimestampScalarPropContext, obj.DatetimestampScalarProp())
        if err != nil {
            return false, err
        }
        err = obj.DatetimestampScalarProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/enum-list-prop":
        val, err := DecodeList[string](value, path, httpExampleOrgTestClassEnumListPropContext, DecodeIRI, obj.EnumListProp())
        if err != nil {
            return false, err
        }
        err = obj.EnumListProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/enum-prop":
        val, err := DecodeIRI(value, path, httpExampleOrgTestClassEnumPropContext, obj.EnumProp())
        if err != nil {
            return false, err
        }
        err = obj.EnumProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/enum-prop-no-class":
        val, err := DecodeIRI(value, path, httpExampleOrgTestClassEnumPropNoClassContext, obj.EnumPropNoClass())
        if err != nil {
            return false, err
        }
        err = obj.EnumPropNoClass().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/float-prop":
        val, err := DecodeFloat(value, path, httpExampleOrgTestClassFloatPropContext, obj.FloatProp())
        if err != nil {
            return false, err
        }
        err = obj.FloatProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/integer-prop":
        val, err := DecodeInteger(value, path, httpExampleOrgTestClassIntegerPropContext, obj.IntegerProp())
        if err != nil {
            return false, err
        }
        err = obj.IntegerProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/named-property":
        val, err := DecodeString(value, path, httpExampleOrgTestClassNamedPropertyContext, obj.NamedProperty())
        if err != nil {
            return false, err
        }
        err = obj.NamedProperty().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/non-shape":
        val, err := DecodeHttpExampleOrgNonShapeClass(value, path, httpExampleOrgTestClassNonShapeContext, obj.NonShape())
        if err != nil {
            return false, err
        }
        err = obj.NonShape().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/nonnegative-integer-prop":
        val, err := DecodeInteger(value, path, httpExampleOrgTestClassNonnegativeIntegerPropContext, obj.NonnegativeIntegerProp())
        if err != nil {
            return false, err
        }
        err = obj.NonnegativeIntegerProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/positive-integer-prop":
        val, err := DecodeInteger(value, path, httpExampleOrgTestClassPositiveIntegerPropContext, obj.PositiveIntegerProp())
        if err != nil {
            return false, err
        }
        err = obj.PositiveIntegerProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/regex":
        val, err := DecodeString(value, path, httpExampleOrgTestClassRegexContext, obj.Regex())
        if err != nil {
            return false, err
        }
        err = obj.Regex().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/regex-datetime":
        val, err := DecodeDateTime(value, path, httpExampleOrgTestClassRegexDatetimeContext, obj.RegexDatetime())
        if err != nil {
            return false, err
        }
        err = obj.RegexDatetime().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/regex-datetimestamp":
        val, err := DecodeDateTimeStamp(value, path, httpExampleOrgTestClassRegexDatetimestampContext, obj.RegexDatetimestamp())
        if err != nil {
            return false, err
        }
        err = obj.RegexDatetimestamp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/regex-list":
        val, err := DecodeList[string](value, path, httpExampleOrgTestClassRegexListContext, DecodeString, obj.RegexList())
        if err != nil {
            return false, err
        }
        err = obj.RegexList().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/string-list-no-datatype":
        val, err := DecodeList[string](value, path, httpExampleOrgTestClassStringListNoDatatypeContext, DecodeString, obj.StringListNoDatatype())
        if err != nil {
            return false, err
        }
        err = obj.StringListNoDatatype().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/string-list-prop":
        val, err := DecodeList[string](value, path, httpExampleOrgTestClassStringListPropContext, DecodeString, obj.StringListProp())
        if err != nil {
            return false, err
        }
        err = obj.StringListProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/string-scalar-prop":
        val, err := DecodeString(value, path, httpExampleOrgTestClassStringScalarPropContext, obj.StringScalarProp())
        if err != nil {
            return false, err
        }
        err = obj.StringScalarProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgTestClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgTestClassObject(&HttpExampleOrgTestClassObject{}, self)
}

func ConstructHttpExampleOrgTestClassObject(o *HttpExampleOrgTestClassObject, typ SHACLType) *HttpExampleOrgTestClassObject {
    ConstructHttpExampleOrgParentClassObject(&o.HttpExampleOrgParentClassObject, typ)
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.encode = NewProperty[string]("encode", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.import_ = NewProperty[string]("import_", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.anyuriProp = NewProperty[string]("anyuriProp", validators, decodeValidators)
    }
    {
        validators := []Validator[bool]{}
        decodeValidators := []Validator[any]{}
        o.booleanProp = NewProperty[bool]("booleanProp", validators, decodeValidators)
    }
    {
        validators := []Validator[Ref[HttpExampleOrgTestClass]]{}
        decodeValidators := []Validator[any]{}
        o.classListProp = NewRefListProperty[HttpExampleOrgTestClass]("classListProp", validators, decodeValidators)
    }
    {
        validators := []Validator[Ref[HttpExampleOrgTestClass]]{}
        decodeValidators := []Validator[any]{}
        o.classProp = NewRefProperty[HttpExampleOrgTestClass]("classProp", validators, decodeValidators)
    }
    {
        validators := []Validator[Ref[HttpExampleOrgTestClass]]{}
        decodeValidators := []Validator[any]{}
        o.classPropNoClass = NewRefProperty[HttpExampleOrgTestClass]("classPropNoClass", validators, decodeValidators)
    }
    {
        validators := []Validator[time.Time]{}
        decodeValidators := []Validator[any]{}
        o.datetimeListProp = NewListProperty[time.Time]("datetimeListProp", validators, decodeValidators)
    }
    {
        validators := []Validator[time.Time]{}
        decodeValidators := []Validator[any]{}
        o.datetimeScalarProp = NewProperty[time.Time]("datetimeScalarProp", validators, decodeValidators)
    }
    {
        validators := []Validator[time.Time]{}
        decodeValidators := []Validator[any]{}
        o.datetimestampScalarProp = NewProperty[time.Time]("datetimestampScalarProp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators,
            EnumValidator{[]string{
                "http://example.org/enumType/bar",
                "http://example.org/enumType/foo",
                "http://example.org/enumType/nolabel",
                "http://example.org/enumType/non-named-individual",
        }})
        o.enumListProp = NewListProperty[string]("enumListProp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators,
            EnumValidator{[]string{
                "http://example.org/enumType/bar",
                "http://example.org/enumType/foo",
                "http://example.org/enumType/nolabel",
                "http://example.org/enumType/non-named-individual",
        }})
        o.enumProp = NewProperty[string]("enumProp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators,
            EnumValidator{[]string{
                "http://example.org/enumType/bar",
                "http://example.org/enumType/foo",
                "http://example.org/enumType/nolabel",
                "http://example.org/enumType/non-named-individual",
        }})
        o.enumPropNoClass = NewProperty[string]("enumPropNoClass", validators, decodeValidators)
    }
    {
        validators := []Validator[float64]{}
        decodeValidators := []Validator[any]{}
        o.floatProp = NewProperty[float64]("floatProp", validators, decodeValidators)
    }
    {
        validators := []Validator[int]{}
        decodeValidators := []Validator[any]{}
        o.integerProp = NewProperty[int]("integerProp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.namedProperty = NewProperty[string]("namedProperty", validators, decodeValidators)
    }
    {
        validators := []Validator[Ref[HttpExampleOrgNonShapeClass]]{}
        decodeValidators := []Validator[any]{}
        o.nonShape = NewRefProperty[HttpExampleOrgNonShapeClass]("nonShape", validators, decodeValidators)
    }
    {
        validators := []Validator[int]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators, IntegerMinValidator{0})
        o.nonnegativeIntegerProp = NewProperty[int]("nonnegativeIntegerProp", validators, decodeValidators)
    }
    {
        validators := []Validator[int]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators, IntegerMinValidator{1})
        o.positiveIntegerProp = NewProperty[int]("positiveIntegerProp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators, RegexValidator[string]{`^foo\d`})
        decodeValidators = append(decodeValidators, RegexValidator[any]{`^foo\d`})
        o.regex = NewProperty[string]("regex", validators, decodeValidators)
    }
    {
        validators := []Validator[time.Time]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators, RegexValidator[time.Time]{`^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\+01:00$`})
        decodeValidators = append(decodeValidators, RegexValidator[any]{`^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\+01:00$`})
        o.regexDatetime = NewProperty[time.Time]("regexDatetime", validators, decodeValidators)
    }
    {
        validators := []Validator[time.Time]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators, RegexValidator[time.Time]{`^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$`})
        decodeValidators = append(decodeValidators, RegexValidator[any]{`^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$`})
        o.regexDatetimestamp = NewProperty[time.Time]("regexDatetimestamp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        validators = append(validators, RegexValidator[string]{`^foo\d`})
        decodeValidators = append(decodeValidators, RegexValidator[any]{`^foo\d`})
        o.regexList = NewListProperty[string]("regexList", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.stringListNoDatatype = NewListProperty[string]("stringListNoDatatype", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.stringListProp = NewListProperty[string]("stringListProp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.stringScalarProp = NewProperty[string]("stringScalarProp", validators, decodeValidators)
    }
    return o
}

type HttpExampleOrgTestClass interface {
    HttpExampleOrgParentClass
    Encode() PropertyInterface[string]
    Import() PropertyInterface[string]
    AnyuriProp() PropertyInterface[string]
    BooleanProp() PropertyInterface[bool]
    ClassListProp() ListPropertyInterface[Ref[HttpExampleOrgTestClass]]
    ClassProp() RefPropertyInterface[HttpExampleOrgTestClass]
    ClassPropNoClass() RefPropertyInterface[HttpExampleOrgTestClass]
    DatetimeListProp() ListPropertyInterface[time.Time]
    DatetimeScalarProp() PropertyInterface[time.Time]
    DatetimestampScalarProp() PropertyInterface[time.Time]
    EnumListProp() ListPropertyInterface[string]
    EnumProp() PropertyInterface[string]
    EnumPropNoClass() PropertyInterface[string]
    FloatProp() PropertyInterface[float64]
    IntegerProp() PropertyInterface[int]
    NamedProperty() PropertyInterface[string]
    NonShape() RefPropertyInterface[HttpExampleOrgNonShapeClass]
    NonnegativeIntegerProp() PropertyInterface[int]
    PositiveIntegerProp() PropertyInterface[int]
    Regex() PropertyInterface[string]
    RegexDatetime() PropertyInterface[time.Time]
    RegexDatetimestamp() PropertyInterface[time.Time]
    RegexList() ListPropertyInterface[string]
    StringListNoDatatype() ListPropertyInterface[string]
    StringListProp() ListPropertyInterface[string]
    StringScalarProp() PropertyInterface[string]
}


func MakeHttpExampleOrgTestClass() HttpExampleOrgTestClass {
    return ConstructHttpExampleOrgTestClassObject(&HttpExampleOrgTestClassObject{}, httpExampleOrgTestClassType)
}

func MakeHttpExampleOrgTestClassRef() Ref[HttpExampleOrgTestClass] {
    o := MakeHttpExampleOrgTestClass()
    return MakeObjectRef[HttpExampleOrgTestClass](o)
}

func (self *HttpExampleOrgTestClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgParentClassObject.Validate(path, handler) {
        valid = false
    }
    {
        prop_path := path.PushPath("encode")
        if ! self.encode.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("import_")
        if ! self.import_.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("anyuriProp")
        if ! self.anyuriProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("booleanProp")
        if ! self.booleanProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("classListProp")
        if ! self.classListProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("classProp")
        if ! self.classProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("classPropNoClass")
        if ! self.classPropNoClass.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("datetimeListProp")
        if ! self.datetimeListProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("datetimeScalarProp")
        if ! self.datetimeScalarProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("datetimestampScalarProp")
        if ! self.datetimestampScalarProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("enumListProp")
        if ! self.enumListProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("enumProp")
        if ! self.enumProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("enumPropNoClass")
        if ! self.enumPropNoClass.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("floatProp")
        if ! self.floatProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("integerProp")
        if ! self.integerProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("namedProperty")
        if ! self.namedProperty.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("nonShape")
        if ! self.nonShape.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("nonnegativeIntegerProp")
        if ! self.nonnegativeIntegerProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("positiveIntegerProp")
        if ! self.positiveIntegerProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("regex")
        if ! self.regex.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("regexDatetime")
        if ! self.regexDatetime.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("regexDatetimestamp")
        if ! self.regexDatetimestamp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("regexList")
        if ! self.regexList.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("stringListNoDatatype")
        if ! self.stringListNoDatatype.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("stringListProp")
        if ! self.stringListProp.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("stringScalarProp")
        if ! self.stringScalarProp.Check(prop_path, handler) {
            valid = false
        }
    }
    return valid
}

func (self *HttpExampleOrgTestClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgParentClassObject.Walk(path, visit)
    self.encode.Walk(path, visit)
    self.import_.Walk(path, visit)
    self.anyuriProp.Walk(path, visit)
    self.booleanProp.Walk(path, visit)
    self.classListProp.Walk(path, visit)
    self.classProp.Walk(path, visit)
    self.classPropNoClass.Walk(path, visit)
    self.datetimeListProp.Walk(path, visit)
    self.datetimeScalarProp.Walk(path, visit)
    self.datetimestampScalarProp.Walk(path, visit)
    self.enumListProp.Walk(path, visit)
    self.enumProp.Walk(path, visit)
    self.enumPropNoClass.Walk(path, visit)
    self.floatProp.Walk(path, visit)
    self.integerProp.Walk(path, visit)
    self.namedProperty.Walk(path, visit)
    self.nonShape.Walk(path, visit)
    self.nonnegativeIntegerProp.Walk(path, visit)
    self.positiveIntegerProp.Walk(path, visit)
    self.regex.Walk(path, visit)
    self.regexDatetime.Walk(path, visit)
    self.regexDatetimestamp.Walk(path, visit)
    self.regexList.Walk(path, visit)
    self.stringListNoDatatype.Walk(path, visit)
    self.stringListProp.Walk(path, visit)
    self.stringScalarProp.Walk(path, visit)
}

func (self *HttpExampleOrgTestClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgParentClassObject.Link(state); err != nil {
        return err
    }
    if err := self.encode.Link(state); err != nil {
        return err
    }
    if err := self.import_.Link(state); err != nil {
        return err
    }
    if err := self.anyuriProp.Link(state); err != nil {
        return err
    }
    if err := self.booleanProp.Link(state); err != nil {
        return err
    }
    if err := self.classListProp.Link(state); err != nil {
        return err
    }
    if err := self.classProp.Link(state); err != nil {
        return err
    }
    if err := self.classPropNoClass.Link(state); err != nil {
        return err
    }
    if err := self.datetimeListProp.Link(state); err != nil {
        return err
    }
    if err := self.datetimeScalarProp.Link(state); err != nil {
        return err
    }
    if err := self.datetimestampScalarProp.Link(state); err != nil {
        return err
    }
    if err := self.enumListProp.Link(state); err != nil {
        return err
    }
    if err := self.enumProp.Link(state); err != nil {
        return err
    }
    if err := self.enumPropNoClass.Link(state); err != nil {
        return err
    }
    if err := self.floatProp.Link(state); err != nil {
        return err
    }
    if err := self.integerProp.Link(state); err != nil {
        return err
    }
    if err := self.namedProperty.Link(state); err != nil {
        return err
    }
    if err := self.nonShape.Link(state); err != nil {
        return err
    }
    if err := self.nonnegativeIntegerProp.Link(state); err != nil {
        return err
    }
    if err := self.positiveIntegerProp.Link(state); err != nil {
        return err
    }
    if err := self.regex.Link(state); err != nil {
        return err
    }
    if err := self.regexDatetime.Link(state); err != nil {
        return err
    }
    if err := self.regexDatetimestamp.Link(state); err != nil {
        return err
    }
    if err := self.regexList.Link(state); err != nil {
        return err
    }
    if err := self.stringListNoDatatype.Link(state); err != nil {
        return err
    }
    if err := self.stringListProp.Link(state); err != nil {
        return err
    }
    if err := self.stringScalarProp.Link(state); err != nil {
        return err
    }
    return nil
}


func (self *HttpExampleOrgTestClassObject) Encode() PropertyInterface[string] { return &self.encode }
func (self *HttpExampleOrgTestClassObject) Import() PropertyInterface[string] { return &self.import_ }
func (self *HttpExampleOrgTestClassObject) AnyuriProp() PropertyInterface[string] { return &self.anyuriProp }
func (self *HttpExampleOrgTestClassObject) BooleanProp() PropertyInterface[bool] { return &self.booleanProp }
func (self *HttpExampleOrgTestClassObject) ClassListProp() ListPropertyInterface[Ref[HttpExampleOrgTestClass]] { return &self.classListProp }
func (self *HttpExampleOrgTestClassObject) ClassProp() RefPropertyInterface[HttpExampleOrgTestClass] { return &self.classProp }
func (self *HttpExampleOrgTestClassObject) ClassPropNoClass() RefPropertyInterface[HttpExampleOrgTestClass] { return &self.classPropNoClass }
func (self *HttpExampleOrgTestClassObject) DatetimeListProp() ListPropertyInterface[time.Time] { return &self.datetimeListProp }
func (self *HttpExampleOrgTestClassObject) DatetimeScalarProp() PropertyInterface[time.Time] { return &self.datetimeScalarProp }
func (self *HttpExampleOrgTestClassObject) DatetimestampScalarProp() PropertyInterface[time.Time] { return &self.datetimestampScalarProp }
func (self *HttpExampleOrgTestClassObject) EnumListProp() ListPropertyInterface[string] { return &self.enumListProp }
func (self *HttpExampleOrgTestClassObject) EnumProp() PropertyInterface[string] { return &self.enumProp }
func (self *HttpExampleOrgTestClassObject) EnumPropNoClass() PropertyInterface[string] { return &self.enumPropNoClass }
func (self *HttpExampleOrgTestClassObject) FloatProp() PropertyInterface[float64] { return &self.floatProp }
func (self *HttpExampleOrgTestClassObject) IntegerProp() PropertyInterface[int] { return &self.integerProp }
func (self *HttpExampleOrgTestClassObject) NamedProperty() PropertyInterface[string] { return &self.namedProperty }
func (self *HttpExampleOrgTestClassObject) NonShape() RefPropertyInterface[HttpExampleOrgNonShapeClass] { return &self.nonShape }
func (self *HttpExampleOrgTestClassObject) NonnegativeIntegerProp() PropertyInterface[int] { return &self.nonnegativeIntegerProp }
func (self *HttpExampleOrgTestClassObject) PositiveIntegerProp() PropertyInterface[int] { return &self.positiveIntegerProp }
func (self *HttpExampleOrgTestClassObject) Regex() PropertyInterface[string] { return &self.regex }
func (self *HttpExampleOrgTestClassObject) RegexDatetime() PropertyInterface[time.Time] { return &self.regexDatetime }
func (self *HttpExampleOrgTestClassObject) RegexDatetimestamp() PropertyInterface[time.Time] { return &self.regexDatetimestamp }
func (self *HttpExampleOrgTestClassObject) RegexList() ListPropertyInterface[string] { return &self.regexList }
func (self *HttpExampleOrgTestClassObject) StringListNoDatatype() ListPropertyInterface[string] { return &self.stringListNoDatatype }
func (self *HttpExampleOrgTestClassObject) StringListProp() ListPropertyInterface[string] { return &self.stringListProp }
func (self *HttpExampleOrgTestClassObject) StringScalarProp() PropertyInterface[string] { return &self.stringScalarProp }

func (self *HttpExampleOrgTestClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgParentClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    if self.encode.IsSet() {
        val, err := EncodeString(self.encode.Get(), path.PushPath("encode"), httpExampleOrgTestClassEncodeContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/encode"] = val
    }
    if self.import_.IsSet() {
        val, err := EncodeString(self.import_.Get(), path.PushPath("import_"), httpExampleOrgTestClassImportContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/import"] = val
    }
    if self.anyuriProp.IsSet() {
        val, err := EncodeString(self.anyuriProp.Get(), path.PushPath("anyuriProp"), httpExampleOrgTestClassAnyuriPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/anyuri-prop"] = val
    }
    if self.booleanProp.IsSet() {
        val, err := EncodeBoolean(self.booleanProp.Get(), path.PushPath("booleanProp"), httpExampleOrgTestClassBooleanPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/boolean-prop"] = val
    }
    if self.classListProp.IsSet() {
        val, err := EncodeList[Ref[HttpExampleOrgTestClass]](self.classListProp.Get(), path.PushPath("classListProp"), httpExampleOrgTestClassClassListPropContext, state, EncodeRef[HttpExampleOrgTestClass])
        if err != nil {
            return err
        }
        data["http://example.org/test-class/class-list-prop"] = val
    }
    if self.classProp.IsSet() {
        val, err := EncodeRef[HttpExampleOrgTestClass](self.classProp.Get(), path.PushPath("classProp"), httpExampleOrgTestClassClassPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/class-prop"] = val
    }
    if self.classPropNoClass.IsSet() {
        val, err := EncodeRef[HttpExampleOrgTestClass](self.classPropNoClass.Get(), path.PushPath("classPropNoClass"), httpExampleOrgTestClassClassPropNoClassContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/class-prop-no-class"] = val
    }
    if self.datetimeListProp.IsSet() {
        val, err := EncodeList[time.Time](self.datetimeListProp.Get(), path.PushPath("datetimeListProp"), httpExampleOrgTestClassDatetimeListPropContext, state, EncodeDateTime)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/datetime-list-prop"] = val
    }
    if self.datetimeScalarProp.IsSet() {
        val, err := EncodeDateTime(self.datetimeScalarProp.Get(), path.PushPath("datetimeScalarProp"), httpExampleOrgTestClassDatetimeScalarPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/datetime-scalar-prop"] = val
    }
    if self.datetimestampScalarProp.IsSet() {
        val, err := EncodeDateTime(self.datetimestampScalarProp.Get(), path.PushPath("datetimestampScalarProp"), httpExampleOrgTestClassDatetimestampScalarPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/datetimestamp-scalar-prop"] = val
    }
    if self.enumListProp.IsSet() {
        val, err := EncodeList[string](self.enumListProp.Get(), path.PushPath("enumListProp"), httpExampleOrgTestClassEnumListPropContext, state, EncodeIRI)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/enum-list-prop"] = val
    }
    if self.enumProp.IsSet() {
        val, err := EncodeIRI(self.enumProp.Get(), path.PushPath("enumProp"), httpExampleOrgTestClassEnumPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/enum-prop"] = val
    }
    if self.enumPropNoClass.IsSet() {
        val, err := EncodeIRI(self.enumPropNoClass.Get(), path.PushPath("enumPropNoClass"), httpExampleOrgTestClassEnumPropNoClassContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/enum-prop-no-class"] = val
    }
    if self.floatProp.IsSet() {
        val, err := EncodeFloat(self.floatProp.Get(), path.PushPath("floatProp"), httpExampleOrgTestClassFloatPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/float-prop"] = val
    }
    if self.integerProp.IsSet() {
        val, err := EncodeInteger(self.integerProp.Get(), path.PushPath("integerProp"), httpExampleOrgTestClassIntegerPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/integer-prop"] = val
    }
    if self.namedProperty.IsSet() {
        val, err := EncodeString(self.namedProperty.Get(), path.PushPath("namedProperty"), httpExampleOrgTestClassNamedPropertyContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/named-property"] = val
    }
    if self.nonShape.IsSet() {
        val, err := EncodeRef[HttpExampleOrgNonShapeClass](self.nonShape.Get(), path.PushPath("nonShape"), httpExampleOrgTestClassNonShapeContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/non-shape"] = val
    }
    if self.nonnegativeIntegerProp.IsSet() {
        val, err := EncodeInteger(self.nonnegativeIntegerProp.Get(), path.PushPath("nonnegativeIntegerProp"), httpExampleOrgTestClassNonnegativeIntegerPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/nonnegative-integer-prop"] = val
    }
    if self.positiveIntegerProp.IsSet() {
        val, err := EncodeInteger(self.positiveIntegerProp.Get(), path.PushPath("positiveIntegerProp"), httpExampleOrgTestClassPositiveIntegerPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/positive-integer-prop"] = val
    }
    if self.regex.IsSet() {
        val, err := EncodeString(self.regex.Get(), path.PushPath("regex"), httpExampleOrgTestClassRegexContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/regex"] = val
    }
    if self.regexDatetime.IsSet() {
        val, err := EncodeDateTime(self.regexDatetime.Get(), path.PushPath("regexDatetime"), httpExampleOrgTestClassRegexDatetimeContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/regex-datetime"] = val
    }
    if self.regexDatetimestamp.IsSet() {
        val, err := EncodeDateTime(self.regexDatetimestamp.Get(), path.PushPath("regexDatetimestamp"), httpExampleOrgTestClassRegexDatetimestampContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/regex-datetimestamp"] = val
    }
    if self.regexList.IsSet() {
        val, err := EncodeList[string](self.regexList.Get(), path.PushPath("regexList"), httpExampleOrgTestClassRegexListContext, state, EncodeString)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/regex-list"] = val
    }
    if self.stringListNoDatatype.IsSet() {
        val, err := EncodeList[string](self.stringListNoDatatype.Get(), path.PushPath("stringListNoDatatype"), httpExampleOrgTestClassStringListNoDatatypeContext, state, EncodeString)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/string-list-no-datatype"] = val
    }
    if self.stringListProp.IsSet() {
        val, err := EncodeList[string](self.stringListProp.Get(), path.PushPath("stringListProp"), httpExampleOrgTestClassStringListPropContext, state, EncodeString)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/string-list-prop"] = val
    }
    if self.stringScalarProp.IsSet() {
        val, err := EncodeString(self.stringScalarProp.Get(), path.PushPath("stringScalarProp"), httpExampleOrgTestClassStringScalarPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/string-scalar-prop"] = val
    }
    return nil
}
type HttpExampleOrgTestClassRequiredObject struct {
    HttpExampleOrgTestClassObject

    // A required string list property
    requiredStringListProp ListProperty[string]
    // A required scalar string property
    requiredStringScalarProp Property[string]
}


type HttpExampleOrgTestClassRequiredObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgTestClassRequiredType HttpExampleOrgTestClassRequiredObjectType
var httpExampleOrgTestClassRequiredRequiredStringListPropContext = map[string]string{}
var httpExampleOrgTestClassRequiredRequiredStringScalarPropContext = map[string]string{}

func DecodeHttpExampleOrgTestClassRequired (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgTestClassRequired], error) {
    return DecodeRef[HttpExampleOrgTestClassRequired](data, path, context, httpExampleOrgTestClassRequiredType, check)
}

func (self HttpExampleOrgTestClassRequiredObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgTestClassRequired)
    _ = obj
    switch name {
    case "http://example.org/test-class/required-string-list-prop":
        val, err := DecodeList[string](value, path, httpExampleOrgTestClassRequiredRequiredStringListPropContext, DecodeString, obj.RequiredStringListProp())
        if err != nil {
            return false, err
        }
        err = obj.RequiredStringListProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/test-class/required-string-scalar-prop":
        val, err := DecodeString(value, path, httpExampleOrgTestClassRequiredRequiredStringScalarPropContext, obj.RequiredStringScalarProp())
        if err != nil {
            return false, err
        }
        err = obj.RequiredStringScalarProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgTestClassRequiredObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgTestClassRequiredObject(&HttpExampleOrgTestClassRequiredObject{}, self)
}

func ConstructHttpExampleOrgTestClassRequiredObject(o *HttpExampleOrgTestClassRequiredObject, typ SHACLType) *HttpExampleOrgTestClassRequiredObject {
    ConstructHttpExampleOrgTestClassObject(&o.HttpExampleOrgTestClassObject, typ)
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.requiredStringListProp = NewListProperty[string]("requiredStringListProp", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.requiredStringScalarProp = NewProperty[string]("requiredStringScalarProp", validators, decodeValidators)
    }
    return o
}

type HttpExampleOrgTestClassRequired interface {
    HttpExampleOrgTestClass
    RequiredStringListProp() ListPropertyInterface[string]
    RequiredStringScalarProp() PropertyInterface[string]
}


func MakeHttpExampleOrgTestClassRequired() HttpExampleOrgTestClassRequired {
    return ConstructHttpExampleOrgTestClassRequiredObject(&HttpExampleOrgTestClassRequiredObject{}, httpExampleOrgTestClassRequiredType)
}

func MakeHttpExampleOrgTestClassRequiredRef() Ref[HttpExampleOrgTestClassRequired] {
    o := MakeHttpExampleOrgTestClassRequired()
    return MakeObjectRef[HttpExampleOrgTestClassRequired](o)
}

func (self *HttpExampleOrgTestClassRequiredObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgTestClassObject.Validate(path, handler) {
        valid = false
    }
    {
        prop_path := path.PushPath("requiredStringListProp")
        if ! self.requiredStringListProp.Check(prop_path, handler) {
            valid = false
        }
        if len(self.requiredStringListProp.Get()) < 1 {
            if handler != nil {
                handler.HandleError(&ValidationError{
                    "requiredStringListProp",
                    "Too few elements. Minimum of 1 required"},
                    prop_path)
            }
            valid = false
        }
        if len(self.requiredStringListProp.Get()) > 2 {
            if handler != nil {
                handler.HandleError(&ValidationError{
                    "requiredStringListProp",
                    "Too many elements. Maximum of 2 allowed"},
                    prop_path)
            }
            valid = false
        }
    }
    {
        prop_path := path.PushPath("requiredStringScalarProp")
        if ! self.requiredStringScalarProp.Check(prop_path, handler) {
            valid = false
        }
        if ! self.requiredStringScalarProp.IsSet() {
            if handler != nil {
                handler.HandleError(&ValidationError{"requiredStringScalarProp", "Value is required"}, prop_path)
            }
            valid = false
        }
    }
    return valid
}

func (self *HttpExampleOrgTestClassRequiredObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgTestClassObject.Walk(path, visit)
    self.requiredStringListProp.Walk(path, visit)
    self.requiredStringScalarProp.Walk(path, visit)
}

func (self *HttpExampleOrgTestClassRequiredObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgTestClassObject.Link(state); err != nil {
        return err
    }
    if err := self.requiredStringListProp.Link(state); err != nil {
        return err
    }
    if err := self.requiredStringScalarProp.Link(state); err != nil {
        return err
    }
    return nil
}


func (self *HttpExampleOrgTestClassRequiredObject) RequiredStringListProp() ListPropertyInterface[string] { return &self.requiredStringListProp }
func (self *HttpExampleOrgTestClassRequiredObject) RequiredStringScalarProp() PropertyInterface[string] { return &self.requiredStringScalarProp }

func (self *HttpExampleOrgTestClassRequiredObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgTestClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    if self.requiredStringListProp.IsSet() {
        val, err := EncodeList[string](self.requiredStringListProp.Get(), path.PushPath("requiredStringListProp"), httpExampleOrgTestClassRequiredRequiredStringListPropContext, state, EncodeString)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/required-string-list-prop"] = val
    }
    if self.requiredStringScalarProp.IsSet() {
        val, err := EncodeString(self.requiredStringScalarProp.Get(), path.PushPath("requiredStringScalarProp"), httpExampleOrgTestClassRequiredRequiredStringScalarPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-class/required-string-scalar-prop"] = val
    }
    return nil
}

// A class derived from test-class
type HttpExampleOrgTestDerivedClassObject struct {
    HttpExampleOrgTestClassObject

    // A string property in a derived class
    stringProp Property[string]
}


type HttpExampleOrgTestDerivedClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgTestDerivedClassType HttpExampleOrgTestDerivedClassObjectType
var httpExampleOrgTestDerivedClassStringPropContext = map[string]string{}

func DecodeHttpExampleOrgTestDerivedClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgTestDerivedClass], error) {
    return DecodeRef[HttpExampleOrgTestDerivedClass](data, path, context, httpExampleOrgTestDerivedClassType, check)
}

func (self HttpExampleOrgTestDerivedClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgTestDerivedClass)
    _ = obj
    switch name {
    case "http://example.org/test-derived-class/string-prop":
        val, err := DecodeString(value, path, httpExampleOrgTestDerivedClassStringPropContext, obj.StringProp())
        if err != nil {
            return false, err
        }
        err = obj.StringProp().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgTestDerivedClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgTestDerivedClassObject(&HttpExampleOrgTestDerivedClassObject{}, self)
}

func ConstructHttpExampleOrgTestDerivedClassObject(o *HttpExampleOrgTestDerivedClassObject, typ SHACLType) *HttpExampleOrgTestDerivedClassObject {
    ConstructHttpExampleOrgTestClassObject(&o.HttpExampleOrgTestClassObject, typ)
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.stringProp = NewProperty[string]("stringProp", validators, decodeValidators)
    }
    return o
}

type HttpExampleOrgTestDerivedClass interface {
    HttpExampleOrgTestClass
    StringProp() PropertyInterface[string]
}


func MakeHttpExampleOrgTestDerivedClass() HttpExampleOrgTestDerivedClass {
    return ConstructHttpExampleOrgTestDerivedClassObject(&HttpExampleOrgTestDerivedClassObject{}, httpExampleOrgTestDerivedClassType)
}

func MakeHttpExampleOrgTestDerivedClassRef() Ref[HttpExampleOrgTestDerivedClass] {
    o := MakeHttpExampleOrgTestDerivedClass()
    return MakeObjectRef[HttpExampleOrgTestDerivedClass](o)
}

func (self *HttpExampleOrgTestDerivedClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgTestClassObject.Validate(path, handler) {
        valid = false
    }
    {
        prop_path := path.PushPath("stringProp")
        if ! self.stringProp.Check(prop_path, handler) {
            valid = false
        }
    }
    return valid
}

func (self *HttpExampleOrgTestDerivedClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgTestClassObject.Walk(path, visit)
    self.stringProp.Walk(path, visit)
}

func (self *HttpExampleOrgTestDerivedClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgTestClassObject.Link(state); err != nil {
        return err
    }
    if err := self.stringProp.Link(state); err != nil {
        return err
    }
    return nil
}


func (self *HttpExampleOrgTestDerivedClassObject) StringProp() PropertyInterface[string] { return &self.stringProp }

func (self *HttpExampleOrgTestDerivedClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgTestClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    if self.stringProp.IsSet() {
        val, err := EncodeString(self.stringProp.Get(), path.PushPath("stringProp"), httpExampleOrgTestDerivedClassStringPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/test-derived-class/string-prop"] = val
    }
    return nil
}

// A class that uses an abstract extensible class
type HttpExampleOrgUsesExtensibleAbstractClassObject struct {
    SHACLObjectBase

    // A property that references and abstract extensible class
    prop RefProperty[HttpExampleOrgExtensibleAbstractClass]
}


type HttpExampleOrgUsesExtensibleAbstractClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgUsesExtensibleAbstractClassType HttpExampleOrgUsesExtensibleAbstractClassObjectType
var httpExampleOrgUsesExtensibleAbstractClassPropContext = map[string]string{}

func DecodeHttpExampleOrgUsesExtensibleAbstractClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgUsesExtensibleAbstractClass], error) {
    return DecodeRef[HttpExampleOrgUsesExtensibleAbstractClass](data, path, context, httpExampleOrgUsesExtensibleAbstractClassType, check)
}

func (self HttpExampleOrgUsesExtensibleAbstractClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgUsesExtensibleAbstractClass)
    _ = obj
    switch name {
    case "http://example.org/uses-extensible-abstract-class/prop":
        val, err := DecodeHttpExampleOrgExtensibleAbstractClass(value, path, httpExampleOrgUsesExtensibleAbstractClassPropContext, obj.Prop())
        if err != nil {
            return false, err
        }
        err = obj.Prop().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgUsesExtensibleAbstractClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgUsesExtensibleAbstractClassObject(&HttpExampleOrgUsesExtensibleAbstractClassObject{}, self)
}

func ConstructHttpExampleOrgUsesExtensibleAbstractClassObject(o *HttpExampleOrgUsesExtensibleAbstractClassObject, typ SHACLType) *HttpExampleOrgUsesExtensibleAbstractClassObject {
    ConstructSHACLObjectBase(&o.SHACLObjectBase, typ)
    {
        validators := []Validator[Ref[HttpExampleOrgExtensibleAbstractClass]]{}
        decodeValidators := []Validator[any]{}
        o.prop = NewRefProperty[HttpExampleOrgExtensibleAbstractClass]("prop", validators, decodeValidators)
    }
    return o
}

type HttpExampleOrgUsesExtensibleAbstractClass interface {
    SHACLObject
    Prop() RefPropertyInterface[HttpExampleOrgExtensibleAbstractClass]
}


func MakeHttpExampleOrgUsesExtensibleAbstractClass() HttpExampleOrgUsesExtensibleAbstractClass {
    return ConstructHttpExampleOrgUsesExtensibleAbstractClassObject(&HttpExampleOrgUsesExtensibleAbstractClassObject{}, httpExampleOrgUsesExtensibleAbstractClassType)
}

func MakeHttpExampleOrgUsesExtensibleAbstractClassRef() Ref[HttpExampleOrgUsesExtensibleAbstractClass] {
    o := MakeHttpExampleOrgUsesExtensibleAbstractClass()
    return MakeObjectRef[HttpExampleOrgUsesExtensibleAbstractClass](o)
}

func (self *HttpExampleOrgUsesExtensibleAbstractClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.SHACLObjectBase.Validate(path, handler) {
        valid = false
    }
    {
        prop_path := path.PushPath("prop")
        if ! self.prop.Check(prop_path, handler) {
            valid = false
        }
        if ! self.prop.IsSet() {
            if handler != nil {
                handler.HandleError(&ValidationError{"prop", "Value is required"}, prop_path)
            }
            valid = false
        }
    }
    return valid
}

func (self *HttpExampleOrgUsesExtensibleAbstractClassObject) Walk(path Path, visit Visit) {
    self.SHACLObjectBase.Walk(path, visit)
    self.prop.Walk(path, visit)
}

func (self *HttpExampleOrgUsesExtensibleAbstractClassObject) Link(state *LinkState) error {
    if err := self.SHACLObjectBase.Link(state); err != nil {
        return err
    }
    if err := self.prop.Link(state); err != nil {
        return err
    }
    return nil
}


func (self *HttpExampleOrgUsesExtensibleAbstractClassObject) Prop() RefPropertyInterface[HttpExampleOrgExtensibleAbstractClass] { return &self.prop }

func (self *HttpExampleOrgUsesExtensibleAbstractClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.SHACLObjectBase.EncodeProperties(data, path, state); err != nil {
        return err
    }
    if self.prop.IsSet() {
        val, err := EncodeRef[HttpExampleOrgExtensibleAbstractClass](self.prop.Get(), path.PushPath("prop"), httpExampleOrgUsesExtensibleAbstractClassPropContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/uses-extensible-abstract-class/prop"] = val
    }
    return nil
}

// Derived class that sorts before the parent to test ordering
type HttpExampleOrgAaaDerivedClassObject struct {
    HttpExampleOrgParentClassObject

}


type HttpExampleOrgAaaDerivedClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgAaaDerivedClassType HttpExampleOrgAaaDerivedClassObjectType

func DecodeHttpExampleOrgAaaDerivedClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgAaaDerivedClass], error) {
    return DecodeRef[HttpExampleOrgAaaDerivedClass](data, path, context, httpExampleOrgAaaDerivedClassType, check)
}

func (self HttpExampleOrgAaaDerivedClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgAaaDerivedClass)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgAaaDerivedClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgAaaDerivedClassObject(&HttpExampleOrgAaaDerivedClassObject{}, self)
}

func ConstructHttpExampleOrgAaaDerivedClassObject(o *HttpExampleOrgAaaDerivedClassObject, typ SHACLType) *HttpExampleOrgAaaDerivedClassObject {
    ConstructHttpExampleOrgParentClassObject(&o.HttpExampleOrgParentClassObject, typ)
    return o
}

type HttpExampleOrgAaaDerivedClass interface {
    HttpExampleOrgParentClass
}


func MakeHttpExampleOrgAaaDerivedClass() HttpExampleOrgAaaDerivedClass {
    return ConstructHttpExampleOrgAaaDerivedClassObject(&HttpExampleOrgAaaDerivedClassObject{}, httpExampleOrgAaaDerivedClassType)
}

func MakeHttpExampleOrgAaaDerivedClassRef() Ref[HttpExampleOrgAaaDerivedClass] {
    o := MakeHttpExampleOrgAaaDerivedClass()
    return MakeObjectRef[HttpExampleOrgAaaDerivedClass](o)
}

func (self *HttpExampleOrgAaaDerivedClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgParentClassObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgAaaDerivedClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgParentClassObject.Walk(path, visit)
}

func (self *HttpExampleOrgAaaDerivedClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgParentClassObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgAaaDerivedClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgParentClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// A class that derives its nodeKind from parent
type HttpExampleOrgDerivedNodeKindIriObject struct {
    HttpExampleOrgNodeKindIriObject

}


type HttpExampleOrgDerivedNodeKindIriObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgDerivedNodeKindIriType HttpExampleOrgDerivedNodeKindIriObjectType

func DecodeHttpExampleOrgDerivedNodeKindIri (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgDerivedNodeKindIri], error) {
    return DecodeRef[HttpExampleOrgDerivedNodeKindIri](data, path, context, httpExampleOrgDerivedNodeKindIriType, check)
}

func (self HttpExampleOrgDerivedNodeKindIriObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgDerivedNodeKindIri)
    _ = obj
    switch name {
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgDerivedNodeKindIriObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgDerivedNodeKindIriObject(&HttpExampleOrgDerivedNodeKindIriObject{}, self)
}

func ConstructHttpExampleOrgDerivedNodeKindIriObject(o *HttpExampleOrgDerivedNodeKindIriObject, typ SHACLType) *HttpExampleOrgDerivedNodeKindIriObject {
    ConstructHttpExampleOrgNodeKindIriObject(&o.HttpExampleOrgNodeKindIriObject, typ)
    return o
}

type HttpExampleOrgDerivedNodeKindIri interface {
    HttpExampleOrgNodeKindIri
}


func MakeHttpExampleOrgDerivedNodeKindIri() HttpExampleOrgDerivedNodeKindIri {
    return ConstructHttpExampleOrgDerivedNodeKindIriObject(&HttpExampleOrgDerivedNodeKindIriObject{}, httpExampleOrgDerivedNodeKindIriType)
}

func MakeHttpExampleOrgDerivedNodeKindIriRef() Ref[HttpExampleOrgDerivedNodeKindIri] {
    o := MakeHttpExampleOrgDerivedNodeKindIri()
    return MakeObjectRef[HttpExampleOrgDerivedNodeKindIri](o)
}

func (self *HttpExampleOrgDerivedNodeKindIriObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgNodeKindIriObject.Validate(path, handler) {
        valid = false
    }
    return valid
}

func (self *HttpExampleOrgDerivedNodeKindIriObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgNodeKindIriObject.Walk(path, visit)
}

func (self *HttpExampleOrgDerivedNodeKindIriObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgNodeKindIriObject.Link(state); err != nil {
        return err
    }
    return nil
}



func (self *HttpExampleOrgDerivedNodeKindIriObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgNodeKindIriObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    return nil
}

// An extensible class
type HttpExampleOrgExtensibleClassObject struct {
    HttpExampleOrgLinkClassObject
    SHACLExtensibleBase

    // An extensible property
    property Property[string]
    // A required extensible property
    required Property[string]
}


type HttpExampleOrgExtensibleClassObjectType struct {
    SHACLTypeBase
}
var httpExampleOrgExtensibleClassType HttpExampleOrgExtensibleClassObjectType
var httpExampleOrgExtensibleClassPropertyContext = map[string]string{}
var httpExampleOrgExtensibleClassRequiredContext = map[string]string{}

func DecodeHttpExampleOrgExtensibleClass (data any, path Path, context map[string]string, check DecodeCheckType) (Ref[HttpExampleOrgExtensibleClass], error) {
    return DecodeRef[HttpExampleOrgExtensibleClass](data, path, context, httpExampleOrgExtensibleClassType, check)
}

func (self HttpExampleOrgExtensibleClassObjectType) DecodeProperty(o SHACLObject, name string, value interface{}, path Path) (bool, error) {
    obj := o.(HttpExampleOrgExtensibleClass)
    _ = obj
    switch name {
    case "http://example.org/extensible-class/property":
        val, err := DecodeString(value, path, httpExampleOrgExtensibleClassPropertyContext, obj.Property())
        if err != nil {
            return false, err
        }
        err = obj.Property().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    case "http://example.org/extensible-class/required":
        val, err := DecodeString(value, path, httpExampleOrgExtensibleClassRequiredContext, obj.Required())
        if err != nil {
            return false, err
        }
        err = obj.Required().Set(val)
        if err != nil {
            return false, err
        }
        return true, nil
    default:
        found, err := self.SHACLTypeBase.DecodeProperty(o, name, value, path)
        if err != nil || found {
            return found, err
        }
    }

    return false, nil
}

func (self HttpExampleOrgExtensibleClassObjectType) Create() SHACLObject {
    return ConstructHttpExampleOrgExtensibleClassObject(&HttpExampleOrgExtensibleClassObject{}, self)
}

func ConstructHttpExampleOrgExtensibleClassObject(o *HttpExampleOrgExtensibleClassObject, typ SHACLType) *HttpExampleOrgExtensibleClassObject {
    ConstructHttpExampleOrgLinkClassObject(&o.HttpExampleOrgLinkClassObject, typ)
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.property = NewProperty[string]("property", validators, decodeValidators)
    }
    {
        validators := []Validator[string]{}
        decodeValidators := []Validator[any]{}
        o.required = NewProperty[string]("required", validators, decodeValidators)
    }
    return o
}

type HttpExampleOrgExtensibleClass interface {
    HttpExampleOrgLinkClass
    Property() PropertyInterface[string]
    Required() PropertyInterface[string]
}


func MakeHttpExampleOrgExtensibleClass() HttpExampleOrgExtensibleClass {
    return ConstructHttpExampleOrgExtensibleClassObject(&HttpExampleOrgExtensibleClassObject{}, httpExampleOrgExtensibleClassType)
}

func MakeHttpExampleOrgExtensibleClassRef() Ref[HttpExampleOrgExtensibleClass] {
    o := MakeHttpExampleOrgExtensibleClass()
    return MakeObjectRef[HttpExampleOrgExtensibleClass](o)
}

func (self *HttpExampleOrgExtensibleClassObject) Validate(path Path, handler ErrorHandler) bool {
    var valid bool = true
    if ! self.HttpExampleOrgLinkClassObject.Validate(path, handler) {
        valid = false
    }
    {
        prop_path := path.PushPath("property")
        if ! self.property.Check(prop_path, handler) {
            valid = false
        }
    }
    {
        prop_path := path.PushPath("required")
        if ! self.required.Check(prop_path, handler) {
            valid = false
        }
        if ! self.required.IsSet() {
            if handler != nil {
                handler.HandleError(&ValidationError{"required", "Value is required"}, prop_path)
            }
            valid = false
        }
    }
    return valid
}

func (self *HttpExampleOrgExtensibleClassObject) Walk(path Path, visit Visit) {
    self.HttpExampleOrgLinkClassObject.Walk(path, visit)
    self.property.Walk(path, visit)
    self.required.Walk(path, visit)
}

func (self *HttpExampleOrgExtensibleClassObject) Link(state *LinkState) error {
    if err := self.HttpExampleOrgLinkClassObject.Link(state); err != nil {
        return err
    }
    if err := self.property.Link(state); err != nil {
        return err
    }
    if err := self.required.Link(state); err != nil {
        return err
    }
    return nil
}


func (self *HttpExampleOrgExtensibleClassObject) Property() PropertyInterface[string] { return &self.property }
func (self *HttpExampleOrgExtensibleClassObject) Required() PropertyInterface[string] { return &self.required }

func (self *HttpExampleOrgExtensibleClassObject) EncodeProperties(data map[string]interface{}, path Path, state *EncodeState) error {
    if err := self.HttpExampleOrgLinkClassObject.EncodeProperties(data, path, state); err != nil {
        return err
    }
    if self.property.IsSet() {
        val, err := EncodeString(self.property.Get(), path.PushPath("property"), httpExampleOrgExtensibleClassPropertyContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/extensible-class/property"] = val
    }
    if self.required.IsSet() {
        val, err := EncodeString(self.required.Get(), path.PushPath("required"), httpExampleOrgExtensibleClassRequiredContext, state)
        if err != nil {
            return err
        }
        data["http://example.org/extensible-class/required"] = val
    }
    self.SHACLExtensibleBase.EncodeExtProperties(data, path)
    return nil
}


func init() {
    objectTypes = make(map[string] SHACLType)
    httpExampleOrgAbstractClassType = HttpExampleOrgAbstractClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/abstract-class",
            isAbstract: true,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgAbstractClassType)
    httpExampleOrgAbstractShClassType = HttpExampleOrgAbstractShClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/abstract-sh-class",
            isAbstract: true,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgAbstractShClassType)
    httpExampleOrgAbstractSpdxClassType = HttpExampleOrgAbstractSpdxClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/abstract-spdx-class",
            isAbstract: true,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgAbstractSpdxClassType)
    httpExampleOrgConcreteClassType = HttpExampleOrgConcreteClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/concrete-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/abstract-class",
            },
        },
    }
    RegisterType(httpExampleOrgConcreteClassType)
    httpExampleOrgConcreteShClassType = HttpExampleOrgConcreteShClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/concrete-sh-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/abstract-sh-class",
            },
        },
    }
    RegisterType(httpExampleOrgConcreteShClassType)
    httpExampleOrgConcreteSpdxClassType = HttpExampleOrgConcreteSpdxClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/concrete-spdx-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/abstract-spdx-class",
            },
        },
    }
    RegisterType(httpExampleOrgConcreteSpdxClassType)
    httpExampleOrgEnumTypeType = HttpExampleOrgEnumTypeObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/enumType",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgEnumTypeType)
    httpExampleOrgExtensibleAbstractClassType = HttpExampleOrgExtensibleAbstractClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/extensible-abstract-class",
            isAbstract: true,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            isExtensible: NewOptional[bool](true),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgExtensibleAbstractClassType)
    httpExampleOrgIdPropClassType = HttpExampleOrgIdPropClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/id-prop-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            idAlias: NewOptional[string]("testid"),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgIdPropClassType)
    httpExampleOrgInheritedIdPropClassType = HttpExampleOrgInheritedIdPropClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/inherited-id-prop-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            idAlias: NewOptional[string]("testid"),
            parentIRIs: []string{
                "http://example.org/id-prop-class",
            },
        },
    }
    RegisterType(httpExampleOrgInheritedIdPropClassType)
    httpExampleOrgLinkClassType = HttpExampleOrgLinkClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/link-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgLinkClassType)
    httpExampleOrgLinkDerivedClassType = HttpExampleOrgLinkDerivedClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/link-derived-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/link-class",
            },
        },
    }
    RegisterType(httpExampleOrgLinkDerivedClassType)
    httpExampleOrgNodeKindBlankType = HttpExampleOrgNodeKindBlankObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/node-kind-blank",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNode),
            parentIRIs: []string{
                "http://example.org/link-class",
            },
        },
    }
    RegisterType(httpExampleOrgNodeKindBlankType)
    httpExampleOrgNodeKindIriType = HttpExampleOrgNodeKindIriObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/node-kind-iri",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindIRI),
            parentIRIs: []string{
                "http://example.org/link-class",
            },
        },
    }
    RegisterType(httpExampleOrgNodeKindIriType)
    httpExampleOrgNodeKindIriOrBlankType = HttpExampleOrgNodeKindIriOrBlankObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/node-kind-iri-or-blank",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/link-class",
            },
        },
    }
    RegisterType(httpExampleOrgNodeKindIriOrBlankType)
    httpExampleOrgNonShapeClassType = HttpExampleOrgNonShapeClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/non-shape-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgNonShapeClassType)
    httpExampleOrgParentClassType = HttpExampleOrgParentClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/parent-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgParentClassType)
    httpExampleOrgRequiredAbstractType = HttpExampleOrgRequiredAbstractObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/required-abstract",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgRequiredAbstractType)
    httpExampleOrgTestAnotherClassType = HttpExampleOrgTestAnotherClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/test-another-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgTestAnotherClassType)
    httpExampleOrgTestClassType = HttpExampleOrgTestClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/test-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/parent-class",
            },
        },
    }
    RegisterType(httpExampleOrgTestClassType)
    httpExampleOrgTestClassRequiredType = HttpExampleOrgTestClassRequiredObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/test-class-required",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/test-class",
            },
        },
    }
    RegisterType(httpExampleOrgTestClassRequiredType)
    httpExampleOrgTestDerivedClassType = HttpExampleOrgTestDerivedClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/test-derived-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/test-class",
            },
        },
    }
    RegisterType(httpExampleOrgTestDerivedClassType)
    httpExampleOrgUsesExtensibleAbstractClassType = HttpExampleOrgUsesExtensibleAbstractClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/uses-extensible-abstract-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
            },
        },
    }
    RegisterType(httpExampleOrgUsesExtensibleAbstractClassType)
    httpExampleOrgAaaDerivedClassType = HttpExampleOrgAaaDerivedClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/aaa-derived-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            parentIRIs: []string{
                "http://example.org/parent-class",
            },
        },
    }
    RegisterType(httpExampleOrgAaaDerivedClassType)
    httpExampleOrgDerivedNodeKindIriType = HttpExampleOrgDerivedNodeKindIriObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/derived-node-kind-iri",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindIRI),
            parentIRIs: []string{
                "http://example.org/node-kind-iri",
            },
        },
    }
    RegisterType(httpExampleOrgDerivedNodeKindIriType)
    httpExampleOrgExtensibleClassType = HttpExampleOrgExtensibleClassObjectType{
        SHACLTypeBase: SHACLTypeBase{
            typeIRI: "http://example.org/extensible-class",
            isAbstract: false,
            nodeKind: NewOptional[int](NodeKindBlankNodeOrIRI),
            isExtensible: NewOptional[bool](true),
            parentIRIs: []string{
                "http://example.org/link-class",
            },
        },
    }
    RegisterType(httpExampleOrgExtensibleClassType)
}
