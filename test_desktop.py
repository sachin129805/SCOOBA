from skills.desktop import DesktopSkill

desktop = DesktopSkill()

while True:

    app = input("\nOpen app: ")

    if app.lower() == "exit":
        break

    if desktop.open(app):
        print("✅ Opened")
    else:
        print("❌ Failed")