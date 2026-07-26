from pathlib import Path

folders = [
    Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"),
    Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
]

print("=" * 50)

for folder in folders:

    print("\nFolder:", folder)

    if not folder.exists():
        print("❌ Does not exist")
        continue

    count = 0

    for shortcut in folder.rglob("*.lnk"):

        count += 1

        if count <= 10:
            print(shortcut.name)

    print(f"\nTotal shortcuts found: {count}")

print("\n" + "=" * 50)