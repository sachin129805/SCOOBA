from ai.engine import AIEngine

engine = AIEngine()

while True:

    text = input("\nYou : ")

    if text.lower() == "exit":
        break

    decision = engine.think(text)

    print("\nDecision")

    print(decision)