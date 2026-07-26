from skills.filesystem import FileSystemSkill

fs = FileSystemSkill()

print("Creating Folder...")
print(fs.create_folder("WeatherApp"))

print("\nCreating main.py...")
print(fs.create_file("WeatherApp/main.py"))

print("\nCreating requirements.txt...")
print(fs.create_file("WeatherApp/requirements.txt"))