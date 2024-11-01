//
//
//

package model

type SHACLExtensibleBase struct {
    properties map[string][]any
}

func (self *SHACLExtensibleBase) GetExtProperty(name string) []any {
    return self.properties[name]
}

func (self *SHACLExtensibleBase) SetExtProperty(name string, value []any) {
    if self.properties == nil {
        self.properties = make(map[string][]any)
    }
    self.properties[name] = value
}

func (self *SHACLExtensibleBase) DeleteExtProperty(name string) {
    delete(self.properties, name)
}

func (self *SHACLExtensibleBase) EncodeExtProperties(data map[string]any, path Path) error {
    for k, values := range self.properties {
        if len(values) == 0 {
            continue
        }

        lst := []any{}
        for _, v := range values {
            lst = append(lst, v)
        }
        data[k] = lst
    }
    return nil
}

type SHACLExtensibleObject interface {
    GetExtProperty(string) []any
    SetExtProperty(string, []any)
    DeleteExtProperty(string)
}
