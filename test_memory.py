from memory.manager import MemoryManager

memory = MemoryManager()

memory.remember("name", "Sachin")
memory.remember("assistant", "SCOOBA")

print(memory.recall("name"))
print(memory.recall("assistant"))