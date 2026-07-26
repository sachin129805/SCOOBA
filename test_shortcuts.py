from scanner.shortcut_scanner import ShortcutScanner

scanner = ShortcutScanner()

count = scanner.scan()

print(f"\nFound {count} Start Menu shortcuts.")