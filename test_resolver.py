from launcher.resolver import ApplicationResolver

resolver = ApplicationResolver()

print()

print("Chrome")

print(resolver.resolve("chrome"))

print()

print("Docker")

print(resolver.resolve("docker"))

print()

print("Blender")

print(resolver.resolve("blender"))