//
//
//

package model

type RefPropertyInterface[T SHACLObject] interface {
    PropertyInterface[Ref[T]]

    SetObj(val T) error
    SetIRI(iri string) error

    GetIRI() string
    GetObj() T
    IsObj() bool
    IsIRI() bool
}

type RefProperty[T SHACLObject] struct {
    Property[Ref[T]]
}

func NewRefProperty[T SHACLObject](name string, validators []Validator[Ref[T]], decodeValidators []Validator[any]) RefProperty[T] {
    return RefProperty[T]{
        Property: Property[Ref[T]]{
            value: NewEmptyOptional[Ref[T]](),
            name: name,
            validators: validators,
            decodeValidators: decodeValidators,
        },
    }
}

func (self *RefProperty[T]) SetObj(obj T) error {
    // Shorthand to assign an object by making a reference to it
    return self.Set(MakeObjectRef(obj))
}

func (self *RefProperty[T]) SetIRI(iri string) error {
    // Shorthand to assign an IRI by making a reference to it
    return self.Set(MakeIRIRef[T](iri))
}

func (self *RefProperty[T]) GetIRI() string {
    // Shorthand to get the IRI value
    return self.Get().GetIRI()
}

func (self *RefProperty[T]) GetObj() T {
    // Shorthand to get the Object value
    return self.Get().GetObj()
}

func (self *RefProperty[T]) IsSet() bool {
    return self.Property.IsSet() && self.Get().IsSet()
}

func (self *RefProperty[T]) IsObj() bool {
    // Shorthand to check if the property references an object
    return self.Property.IsSet() && self.Get().IsObj()
}

func (self *RefProperty[T]) IsIRI() bool {
    // Shorthand to check if the property references an IRI
    return self.Property.IsSet() && self.Get().IsIRI()
}

func (self *RefProperty[T]) Walk(path Path, visit Visit) {
    if ! self.IsSet() {
        return
    }

    r, err := ConvertRef[SHACLObject](self.value.Get())
    if err != nil {
        return
    }

    visit(path.PushPath(self.name), r)
}

func (self *RefProperty[T]) Link(state *LinkState) error {
    if ! self.IsSet() {
        return nil
    }

    return self.Get().link(state)
}
