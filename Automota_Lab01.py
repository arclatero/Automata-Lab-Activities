# DFA Simulator with dynamic sample checking

def run_dfa(dfa, s):
    state = dfa["start"]
    for ch in s:
        if ch not in dfa["alphabet"]:
            return False, f"symbol {ch!r} not in alphabet {dfa['alphabet']}"
        state = dfa["delta"][(state, ch)]
    return state in dfa["accept"], f"ended in {state}, accept={state in dfa['accept']}"

# ---------- DFA #1 ----------
dfa1 = {
    "states": {"a", "b", "c"},
    "alphabet": {"0", "1"},
    "start": "a",
    "accept": {"c"},  # only c is accepting
    "delta": {
        ("a","0"):"a", ("a","1"):"b",
        ("b","0"):"c", ("b","1"):"a",
        ("c","0"):"b", ("c","1"):"c"
    }
}

# ---------- DFA #2 ----------
dfa2 = {
    "states": {"q0","q1","q2","q3"},
    "alphabet": {"a","b"},
    "start": "q0",
    "accept": {"q0"q3"}, 
    "delta": {
        ("q0","a"):"q1", ("q1","a"):"q0",
        ("q2","a"):"q3", ("q3","a"):"q2",
        ("q0","b"):"q2", ("q2","b"):"q0",
        ("q1","b"):"q3", ("q3","b"):"q1",
    }
}

# Test strings (3 accepted + 3 rejected for each DFA)
machines = {
    "1": (dfa1, ["0101", "101", "1011", "1", "11", "100"]),
    "2": (dfa2, ["ab", "ba", "aaba", "a", "b", "aa"]),
}

# ----------- Show samples dynamically -----------
for key, (dfa, samples) in machines.items():
    print(f"\nDFA #{key} samples:")
    for s in samples:
        ok, info = run_dfa(dfa, s)
        print(f"  Input {s!r}: {'ACCEPTED' if ok else 'REJECTED'} - {info}")

# ----------- Interactive testing -----------
print("\nChoose DFA to test:")
print("1 - DFA #1 (binary, states a,b,c, input (1,0)) ")
print("2 - DFA #2 (alphabet {a,b})")

choice = input("Enter 1 or 2: ").strip()
dfa, _ = machines.get(choice, (None, None))

if dfa is None:
    print("Invalid choice")
else:
    print(f"\nTesting DFA #{choice} — enter strings (blank line to quit).")
    while True:
        s = input("> ")
        if s == "":
            break
        ok, info = run_dfa(dfa, s)
        print("ACCEPTED" if ok else "REJECTED", "-", info)
