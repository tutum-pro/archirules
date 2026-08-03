#!/usr/bin/env python3
"""Sprawdza zgodność strukturalną rejestrów z archirules (RULES.md).

Checks an architecture documentation set against the archirules structure.

    conform.py <katalog docs/architecture> [--lang pl|en|auto]

Kod wyjścia 0, gdy nie ma naruszeń; 1 w przeciwnym razie.

DOPASOWANIE PREFIKSAMI, nie pełnymi brzmieniami. `**Koszt.**` przy jednym koszcie
jest poprawne i nie jest niezgodnością — pierwsza wersja tego kontrolera wymagała
`**Koszty` i zgłosiła sześć fałszywych braków. Wariant językowy to nie wada.

Kontroler NIE zgłasza braku sekcji „Rozważone i odrzucone": w praktyce treść
bywa w prozie, a zgłoszenie braku byłoby twierdzeniem o dokumencie bez jego
przeczytania (reguła W3). Wyodrębnienie sekcji prowadzi szablon dla nowych ADR-ów.
"""
import os, re, sys, glob

M = {
    "pl": {"conseq": r"^## Konsekwencje", "impl": r"^## Stan realizacji",
           "cost": r"\*\*Koszt", "binding": "Wymagania obowiązujące",
           "legend": "Legenda", "criterion": "Kryterium akceptacji", "gate": "Twarda bramka"},
    "en": {"conseq": r"^## Consequences", "impl": r"^## Implementation status",
           "cost": r"\*\*Cost", "binding": "Binding requirements",
           "legend": "Legend", "criterion": "Acceptance criterion", "gate": "Hard gate"},
}
PHASES = ["fazy-realizacji.md", "phases.md"]
VERIF  = ["rejestr-weryfikacji.md", "verification.md"]


def first_existing(d, names):
    for n in names:
        if os.path.isfile(os.path.join(d, n)):
            return n
    return None


def detect_lang(d):
    rd = os.path.join(d, "README.md")
    if os.path.isfile(rd):
        t = open(rd, encoding="utf-8").read()
        if M["pl"]["binding"] in t:
            return "pl"
        if M["en"]["binding"] in t:
            return "en"
    return "pl"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    d = sys.argv[1]
    lang = "auto"
    if "--lang" in sys.argv:
        lang = sys.argv[sys.argv.index("--lang") + 1]
    if lang == "auto":
        lang = detect_lang(d)
    m = M[lang]

    issues, checks = [], 0

    def chk(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            issues.append(msg)

    # 1. artefakty
    chk(os.path.isfile(f"{d}/README.md"), "brak artefaktu: README.md")
    chk(os.path.isfile(f"{d}/open-questions.md"), "brak artefaktu: open-questions.md")
    phases = first_existing(d, PHASES)
    chk(phases is not None, f"brak rejestru faz ({' albo '.join(PHASES)})")
    chk(first_existing(d, VERIF) is not None,
        f"brak rejestru weryfikacji ({' albo '.join(VERIF)})")
    chk(os.path.isdir(f"{d}/decisions"), "brak katalogu decisions/")

    # 2. ADR-y
    adrs = sorted(glob.glob(f"{d}/decisions/ADR-*.md"))
    chk(len(adrs) > 0, "brak ADR-ów w decisions/")
    for f in adrs:
        t = open(f, encoding="utf-8").read()
        n = os.path.basename(f)
        chk(re.search(r"^\*\*Status:\*\*", t, re.M), f"{n}: brak **Status:**")
        chk(re.search(m["conseq"], t, re.M), f"{n}: brak sekcji konsekwencji")
        chk(re.search(m["impl"], t, re.M), f"{n}: brak sekcji stanu realizacji")
        chk(re.search(m["cost"], t), f"{n}: brak sekcji kosztów (prefiks {m['cost']})")

    # 3. indeks
    if os.path.isfile(f"{d}/README.md"):
        rd = open(f"{d}/README.md", encoding="utf-8").read()
        rows = len(re.findall(r"^\| \[\d{4}\]", rd, re.M))
        chk(rows == len(adrs), f"indeks README ma {rows} wierszy, plików ADR jest {len(adrs)}")
        chk(m["binding"] in rd, f"README: brak sekcji „{m['binding']}”")

    # 4. pytania otwarte
    if os.path.isfile(f"{d}/open-questions.md"):
        oq = open(f"{d}/open-questions.md", encoding="utf-8").read()
        nums = [int(x) for x in re.findall(r"^### OQ-(\d+) —", oq, re.M)]
        dup = sorted({n for n in nums if nums.count(n) > 1})
        chk(not dup, f"duplikaty numerów OQ: {dup}")
        if nums:
            gaps = sorted(set(range(1, max(nums) + 1)) - set(nums))
            chk(not gaps, f"luki w numeracji OQ: {gaps}")
        for mm in re.finditer(r"^### OQ-(\d+) —[^\n]*\n(.*)$", oq, re.M):
            chk(mm.group(2).startswith("**Status:**"),
                f"OQ-{mm.group(1)}: **Status:** nie jest bezpośrednio pod nagłówkiem")

    # 5. rejestr faz
    if phases:
        fz = open(f"{d}/{phases}", encoding="utf-8").read()
        chk(m["legend"] in fz, "rejestr faz: brak legendy")
        chk(m["criterion"] in fz, "rejestr faz: brak kolumny kryterium akceptacji")
        chk(m["gate"] in fz, "rejestr faz: brak twardej bramki")

    print(f"  język: {lang} · sprawdzeń: {checks} · naruszeń: {len(issues)}")
    for i in issues:
        print(f"    ✗ {i}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
