from launcher.database import ApplicationDatabase

db = ApplicationDatabase()

db.add(
    "Chrome",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)

db.add(
    "VS Code",
    r"C:\Users\Sachin\AppData\Local\Programs\Microsoft VS Code\Code.exe"
)

db.save()

print()

print(db.count())

print()

print(db.get("chrome"))

print()

print(db.get("vs code"))