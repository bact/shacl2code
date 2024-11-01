//
//
//

package model

import (
    "encoding/json"
    "fmt"
)

type SHACLObjectSet interface {
    Objects(yield func(SHACLObject) bool)
    AddObject(r SHACLObject)
    Decode(decoder *json.Decoder) error
    Encode(encoder *json.Encoder) error
    Walk(visit Visit)
    Validate(handler ErrorHandler) bool
    Link() (map[string]bool, error)
    GetMissingIDs() map[string]bool
}

type SHACLObjectSetObject struct {
    objects []SHACLObject
    missingIDs map[string]bool
}

func (self *SHACLObjectSetObject) Objects(yield func(SHACLObject) bool) {
    for _, o := range self.objects {
        if !yield(o) {
            return
        }
    }
}

func (self *SHACLObjectSetObject) AddObject(r SHACLObject) {
    self.objects = append(self.objects, r)
}


func (self *SHACLObjectSetObject) Decode(decoder *json.Decoder) error {
    path := Path{}

    var data map[string]interface{}
    if err := decoder.Decode(&data); err != nil {
        return err
    }

    {
        v, ok := data["@context"]
        if ! ok {
            return &DecodeError{path, "@context missing"}
        }

        sub_path := path.PushPath("@context")
        value, ok := v.(string)
        if ! ok {
            return &DecodeError{sub_path, "@context must be a string, or list of string"}
        }
        if value != "https://spdx.github.io/spdx-3-model/context.json" {
            return &DecodeError{sub_path, "Wrong context URL '" + value + "'"}
        }
    }

    delete(data, "@context")

    decodeProxy := func (data any, path Path, context map[string]string, check DecodeCheckType) (SHACLObject, error) {
        return DecodeSHACLObject[SHACLObject](data, path, context, nil)
    }

    _, has_graph := data["@graph"]
    if has_graph {
        for k, v := range data {
            switch k {
            case "@graph": {
                objs, err := DecodeList[SHACLObject](
                    v,
                    path.PushPath("@graph"),
                    map[string]string{},
                    decodeProxy,
                    nil,
                )

                if err != nil {
                    return err
                }

                for _, obj := range objs {
                    self.AddObject(obj)
                }
            }

            default:
                return &DecodeError{path, "Unknown property '" + k + "'"}
            }
        }
    } else {
        obj, err := decodeProxy(data, path, map[string]string{}, nil)
        if err != nil {
            return err
        }

        self.AddObject(obj)
    }

    missing, err := self.Link()
    self.missingIDs = missing
    return err
}

func (self *SHACLObjectSetObject) Encode(encoder *json.Encoder) error {
    data := make(map[string]interface{})
    data["@context"] = "https://spdx.github.io/spdx-3-model/context.json"
    path := Path{}
    state := EncodeState{
        Written: make(map[SHACLObject]bool),
    }

    ref_counts := make(map[SHACLObject]int)

    // Count references
    self.Walk(func (path Path, v any) {
        r, ok := v.(Ref[SHACLObject])
        if ! ok {
            return
        }

        if ! r.IsObj() {
            return
        }

        o := r.GetObj()

        // Remove blank nodes for reassignment
        if o.ID().IsSet() && IsBlankNode(o.ID().Get()) {
            o.ID().Delete()
        }

        ref_counts[o] = ref_counts[o] + 1
    })

    blank_count := 0
    for o, count := range ref_counts {
        if count <= 1 {
            continue
        }

        if o.ID().IsSet() {
            continue
        }

        o.ID().Set(fmt.Sprintf("_:%d", blank_count))
        blank_count += 1
    }

    if len(self.objects) == 1 {
        err := self.objects[0].EncodeProperties(data, path, &state)
        if err != nil {
            return err
        }
    } else if len(self.objects) > 1 {
        // All objects directly added to the object set should be written as
        // top level objects, so mark then as written until they are ready to
        // be serialized, which will force them to be referenced by IRI until
        // we are ready
        for _, o := range self.objects {
            state.Written[o] = true
        }

        graph_path := path.PushPath("@graph")
        lst := []interface{}{}
        for idx, o := range self.objects {
            // Remove this object from the written set now so it gets serialized
            delete(state.Written, o)

            d, err := EncodeSHACLObject(o, graph_path.PushIndex(idx), &state)
            if err != nil {
                return err
            }
            lst = append(lst, d)
        }

        data["@graph"] = lst
    }

    return encoder.Encode(data)
}

func (self *SHACLObjectSetObject) Walk(visit Visit) {
    path := Path{}
    visited := map[SHACLObject]bool{}

    visit_proxy := func (path Path, v any) {
        switch v.(type) {
        case Ref[SHACLObject]:
            r := v.(Ref[SHACLObject])
            if ! r.IsObj() {
                visit(path, v)
                return
            }

            o := r.GetObj()
            _, ok := visited[o]
            if ok {
                return
            }
            visited[o] = true
            visit(path, v)
            o.Walk(path, visit)
            return

        default:
            visit(path, v)
            return
        }
    }

    for idx, o := range(self.objects) {
        sub_path := path.PushIndex(idx)
        visit_proxy(sub_path, MakeObjectRef(o))
    }
}

func (self *SHACLObjectSetObject) Validate(handler ErrorHandler) bool {
    valid := true

    self.Walk(func (path Path, v any) {
        r, ok := v.(Ref[SHACLObject])
        if ! ok {
            return
        }

        if ! r.IsObj() {
            return
        }

        if ! r.GetObj().Validate(path, handler) {
            valid = false
        }
    })

    return valid
}

func (self *SHACLObjectSetObject) Link() (map[string]bool, error) {
    state := LinkState{
        make(map[string]SHACLObject),
        make(map[string]bool),
    }

    // Collect IDs and remove blank nodes
    self.Walk(func (path Path, v any) {
        r, ok := v.(Ref[SHACLObject])
        if ! ok {
            return
        }

        if ! r.IsObj() {
            return
        }

        o := r.GetObj()
        if o.ID().IsSet() {
            state.Objs[o.ID().Get()] = o

            if IsBlankNode(o.ID().Get()) {
                o.ID().Delete()
            }
        }
    })

    // Link references
    self.Walk(func (path Path, v any) {
        r, ok := v.(Ref[SHACLObject])
        if ! ok {
            return
        }

        if ! r.IsObj() {
            return
        }

        o := r.GetObj()
        o.Link(&state)
    })

    return state.Missing, nil
}

func (self *SHACLObjectSetObject) GetMissingIDs() map[string]bool {
    return self.missingIDs
}

func NewSHACLObjectSet() SHACLObjectSet {
    os := SHACLObjectSetObject{}
    return &os
}
