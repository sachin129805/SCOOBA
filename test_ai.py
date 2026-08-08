from ai.engine import AIEngine


ai = AIEngine()

commands = [
    "open youtube",
    "search youtube for good day",
    "find cats on youtube",
    "open google and search python tutorials",
    "create a folder called projects",
    "create a python project called scooba"
]

for command in commands:

    print("\n" + "=" * 60)
    print("COMMAND:", command)
    print("=" * 60)

    decision = ai.think(command)

    print(decision)