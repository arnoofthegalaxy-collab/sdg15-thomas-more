print("Hallo! Welkom bij de SDG Quiz!")
score = 0

print("🌍 Welkom bij de SDG Quiz!")
print("Beantwoord de vragen met 1, 2, 3 of 4\n")

# Vraag 1
print("Vraag 1: Hoeveel SDGs zijn er?")
print("1. 10")
print("2. 17")
print("3. 20")
print("4. 25")
antwoord = input("Jouw antwoord: ")
if antwoord == "2":
    print("✅ Correct!\n")
    score += 1
else:
    print("❌ Fout! Het juiste antwoord is 2 (17 SDGs)\n")

# Vraag 2
print("Vraag 2: Tegen welk jaar moeten de SDGs bereikt zijn?")
print("1. 2030")
print("2. 2040")
print("3. 2050")
print("4. 2025")
antwoord = input("Jouw antwoord: ")
if antwoord == "1":
    print("✅ Correct!\n")
    score += 1
else:
    print("❌ Fout! Het juiste antwoord is 1 (2030)\n")

# Vraag 3
print("Vraag 3: Wat betekent SDG?")
print("1. Sustainable Development Goals")
print("2. Social Development Goals")
print("3. Sustainable Design Goals")
print("4. Social Design Goals")
antwoord = input("Jouw antwoord: ")
if antwoord == "1":
    print("✅ Correct!\n")
    score += 1
else:
    print("❌ Fout! Het juiste antwoord is 1\n")

# Vraag 4
print("Vraag 4: Welke organisatie lanceerde de SDGs?")
print("1. Europese Unie")
print("2. Rode Kruis")
print("3. Verenigde Naties")
print("4. Wereldbank")
antwoord = input("Jouw antwoord: ")
if antwoord == "3":
    print("✅ Correct!\n")
    score += 1
else:
    print("❌ Fout! Het juiste antwoord is 3 (Verenigde Naties)\n")

# Vraag 5
print("Vraag 5: Welk SDG gaat over klimaatactie?")
print("1. SDG 7")
print("2. SDG 11")
print("3. SDG 13")
print("4. SDG 15")
antwoord = input("Jouw antwoord: ")
if antwoord == "3":
    print("✅ Correct!\n")
    score += 1
else:
    print("❌ Fout! Het juiste antwoord is 3 (SDG 13)\n")

# Eindscore
print("🏁 Quiz afgelopen!")
print(f"Jouw score: {score}/5")
if score == 5:
    print("🌟 Perfect! Jij bent een SDG expert!")
elif score >= 3:
    print("👍 Goed gedaan!")
else:
    print("📚 Nog even studeren!")
    