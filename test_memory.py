from memory.manager import MemoryManager

memory = MemoryManager()

memory.remember_project(

    "VisionAI",

    "C:/Users/sachi/Documents/SCOOBA_Workspace/VisionAI",

    "Python"

)

print(

    memory.find_project(

        "VisionAI"

    )

)