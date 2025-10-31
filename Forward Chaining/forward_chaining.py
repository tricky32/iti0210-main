EggModel = {
    "Fragile": 0,
    "Fall": 0,
    "Liquid": 0,
    "Spoiled": 0,
    "Breaks": 0,
    "Mess": 0,
    "Smell": 0
}

EggClauses = [
    (['Fragile', 'Fall'], 'Breaks'),
    (['Breaks', 'Liquid'], 'Mess'),
    (['Spoiled', 'Breaks'], 'Smell')
]

def change_states(a):
    i = 0
    # Reset the values of Breaks, Mess, and Smell
    for key in ['Breaks', 'Mess', 'Smell']:
        EggModel[key] = 0
    # Update the first four states (Fragile, Fall, Liquid, Spoiled)
    for egg in list(EggModel.keys())[:4]:
        EggModel[egg] = int(a[i])
        i += 1

def print_current():
    print(f"Fragile: {EggModel['Fragile']} | Fall: {EggModel['Fall']} | Liquid: {EggModel['Liquid']} | Spoiled: {EggModel['Spoiled']} || Breaks: {EggModel['Breaks']} | Mess: {EggModel['Mess']} | Smell: {EggModel['Smell']}")

def check():
    for body, head in EggClauses:
        if all(EggModel[item] == 1 for item in body):  # If all premises are true
            EggModel[head] = 1

# Main execution
print("Evaluating all combinations of Fragile, Fall, Liquid, and Spoiled...\n")
for i in range(16):  # 16 combinations of 4 binary digits
    a = bin(i)[2:].zfill(4)  # Convert to binary and pad to 4 digits
    change_states(a)
    check()
    print(f"Combination {i + 1}: {a}")
    print_current()
    print("-" * 50)
