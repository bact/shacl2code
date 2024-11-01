//
//
//

package model

import (
    "strings"
)

// IRI Validation
func IsIRI(iri string) bool {
    if strings.HasPrefix(iri, "_:") {
        return false
    }
    if strings.Contains(iri, ":") {
        return true
    }
    return false
}

func IsBlankNode(iri string) bool {
    return strings.HasPrefix(iri, "_:")
}
