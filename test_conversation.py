from conversation.manager import ConversationManager

chat = ConversationManager()

chat.add("user", "Open Chrome")

chat.add("assistant", "Opening Chrome.")

chat.add("user", "Go to YouTube")

chat.add("assistant", "Opening YouTube.")

print(chat.all())

print(chat.last())