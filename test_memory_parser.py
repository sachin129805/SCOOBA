from memory.parser import MemoryParser

parser = MemoryParser()

while True:

    text = input("\nYou : ")

    if text == "exit":
        break

    print(parser.parse(text))