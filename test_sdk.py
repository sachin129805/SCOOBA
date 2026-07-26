from ai.decision import Decision
from skills.echo import EchoSkill

skill = EchoSkill()

decision = Decision()

decision.intent = "ECHO"

print(skill.name)

print(skill.can_handle(decision))

print(skill.execute(decision))