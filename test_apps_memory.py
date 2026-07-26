from memory.apps_memory import ApplicationMemory

memory = ApplicationMemory()

memory.remember(
    "docker",
    r"C:\Program Files\Docker\Docker Desktop.exe"
)

memory.remember(
    "blender",
    r"C:\Program Files\Blender Foundation\Blender\blender.exe"
)

print(memory.recall("docker"))

print(memory.recall("blender"))

print(memory.all())