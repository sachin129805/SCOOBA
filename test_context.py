from context.engine import ContextEngine

ctx = ContextEngine()

ctx.set("last_app", "chrome")
ctx.set("last_intent", "OPEN_APP")

print(ctx.dump())

print(ctx.get("last_app"))

ctx.clear()

print(ctx.dump())