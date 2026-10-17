package theme

import "testing"

func TestDragonForgeThemeRegistered(t *testing.T) {
    got := GetTheme("dragonforge")
    if got == nil {
        t.Fatal("DragonForge terminal theme is not registered")
    }
    if got.Accent().Dark != "#ff7518" {
        t.Fatalf("DragonForge dark accent = %s; want flame orange", got.Accent().Dark)
    }
    if got.Primary().Dark != "#18c5ff" {
        t.Fatalf("DragonForge dark primary = %s; want cyan coding blue", got.Primary().Dark)
    }
    if got.Background().Light == "" || got.Background().Dark == "" {
        t.Fatal("DragonForge must provide adaptive light and dark colours")
    }
}
