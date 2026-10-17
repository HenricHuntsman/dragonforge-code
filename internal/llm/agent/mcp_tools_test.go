package agent

import (
	"reflect"
	"testing"
)

func TestParseMCPArguments(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    map[string]any
		wantErr bool
	}{
		{name: "empty", input: "", want: map[string]any{}},
		{name: "whitespace", input: "  \n\t ", want: map[string]any{}},
		{name: "empty object", input: "{}", want: map[string]any{}},
		{name: "normal object", input: "{\"query\":\"read-only\",\"count\":2}", want: map[string]any{"query": "read-only", "count": float64(2)}},
		{name: "invalid JSON remains error", input: "{bad}", wantErr: true},
		{name: "array is not object", input: "[]", wantErr: true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := parseMCPArguments(tt.input)
			if (err != nil) != tt.wantErr {
				t.Fatalf("parseMCPArguments(%q) error = %v, wantErr %v", tt.input, err, tt.wantErr)
			}
			if !tt.wantErr && !reflect.DeepEqual(got, tt.want) {
				t.Fatalf("parseMCPArguments(%q) = %#v, want %#v", tt.input, got, tt.want)
			}
		})
	}
}
