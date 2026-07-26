from ai.nlp.processor import NLPProcessor

processor = NLPProcessor()

print("=" * 50)
print("SCOOBA NLP TEST")
print("=" * 50)

while True:

    text = input("\nYou : ")

    if text.lower() == "exit":
        break

    result = processor.process(text)

    print("\nResult:")
    print(result)