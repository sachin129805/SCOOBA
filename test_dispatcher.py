from ai.decision import Decision
from ai.dispatcher import AIDispatcher

dispatcher = AIDispatcher()

d = Decision()

d.intent = "GREETING"

print(dispatcher.response(d))

d.intent = "OPEN_APP"

d.entity = "Chrome"

print(dispatcher.response(d))

d.intent = "XYZ"

print(dispatcher.response(d))