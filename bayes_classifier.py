import yaml

ok = False

while not ok:
    print("Jaki plik chcesz otworzyc: ")
    print("0 - choroby1.yaml")
    print("1 - choroby2.yaml")
    print("2 - egzamin.yaml")
    file_selected = int(input())
    ok = isinstance(file_selected, int) & (0 <= file_selected <= 2)


def switch(s):
    return {
        0: "data/choroby1.yaml",
        1: "data/choroby2.yaml",
        2: "data/egzamin.yaml"
    }[s]


file = open(switch(file_selected), "r", encoding='utf8')
data = yaml.safe_load(file)

hypotheses = data["Hypotheses"]
facts = data["Facts"]

print("Hipoteza, prawdopodobieństwo a priori (1/100%):")
for h in hypotheses:
    print("{}, {}".format(h["name"], h["prob"]))

print()
print("POJEDYNCZE FAKTY")

Pr_f = []
for f in facts:
    sum = 0
    for indexh, h in enumerate(hypotheses):
        sum += h["prob"]*f["prob"][indexh]
    Pr_f.append([f["name"], round(sum, 5)])

print("Fakt, prawdopodobieństwo (1/100%):")
for x in Pr_f:
    print(*x, sep=", ")  


Pr_h_f = []
for indexh, h in enumerate(hypotheses):
    for indexf, f in enumerate(facts):
        pr = round(h["prob"]*f["prob"][indexh] / Pr_f[indexf][1], 5)
        Pr_h_f.append([h["name"], f["name"], pr])

print()
print("Hipoteza, fakt, prawdopodobieństwo (1/100%):")
for x in Pr_h_f:
    print(*x, sep=', ')


print()
print("KILKA FAKTÓW JEDNOCZEŚNIE")
print("Fakty:")
for index, f in enumerate(facts):
    print(index, f["name"])


ok = False
while not ok:
    selected_facts_indexes = sorted(input("Podaj numery objawów, oddzielając je spacjami: ").split())
    selected_facts_indexes = [int(i) for i in selected_facts_indexes]
    selected_facts_indexes = list(dict.fromkeys(selected_facts_indexes))
    ok = set(selected_facts_indexes).issubset(range(len(facts)))

selected_facts_names = [facts[int(i)]["name"] for i in selected_facts_indexes]
selected_facts = [facts[int(i)] for i in selected_facts_indexes]


def product(facts, i):
    p = 1
    for f in facts:
        p *= f["prob"][i]
    return p


Pr_selected = []

for index in range(len(hypotheses)):
    denominator = hypotheses[index]["prob"]*product(selected_facts, index)

    nominator = 0;
    for i, hi in enumerate(hypotheses):
       nominator += hi["prob"] * product(selected_facts, i)

    Pr_selected.append(round(denominator/nominator * 100, 2))

print()
for i, h in enumerate(hypotheses):
    print("Prawdopodobieństwo hipotezy {} przy uwzględnieniu faktów ({}) wynosi: {}%."
          .format(h["name"], ', '.join(selected_facts_names), Pr_selected[i]))
