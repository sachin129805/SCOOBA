from scanner.app_scanner import ApplicationScanner

scanner = ApplicationScanner()

count = scanner.scan()

print(f"\nFound {count} applications.")