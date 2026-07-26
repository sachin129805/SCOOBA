from ai.normalizer.command_normalizer import CommandNormalizer

normalizer = CommandNormalizer()

while True:

    text = input("\nYou : ")

    if text == "exit":
        break

    print("\nNormalized :", normalizer.normalize(text))