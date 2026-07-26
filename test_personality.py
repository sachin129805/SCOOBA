from personality.engine import PersonalityEngine

p = PersonalityEngine()

print(p.speak("GREETING"))

print(p.speak("OPEN_APP", "Chrome"))

print(p.speak("UNKNOWN"))