---
name: weryfikacja
description: Verification discipline — prove a new gate can fail, avoid measuring your own test artifacts, run suites twice. Use when adding a check, a test, or before reporting any measured result.
---

# Dyscyplina dowodu

## Nowa bramka nie jest gotowa, dopóki nie pokazano, że pada

Procedura, za każdym razem:

1. Uruchom na czystym drzewie → ma przejść.
2. **Zepsuj celowo**, w każdym kształcie naruszenia, jaki bramka ma łapać.
3. Uruchom → ma paść, z czytelnym komunikatem i **niezerowym kodem wyjścia**.
4. Cofnij zepsucie, uruchom → ma przejść.
5. Zapisz w commicie, na jakich kształtach sprawdzono.

*Dlaczego:* bramka architektoniczna dwukrotnie zgłaszała „czysto" na celowo zepsutej
bibliotece. Raz przez wyrażenie regularne wymagające wcięcia — widziało importy zgrupowane,
nie widziało jednolinijkowych. Raz przez `2>/dev/null`, które zamieniło błąd narzędzia
w pusty wynik czytany jako sukces.

**Kontrola, która nie potrafi paść, wygląda identycznie jak kontrola, która przechodzi.**

## Nie wyciszaj błędów w bramce

`2>/dev/null`, `|| true`, ignorowany kod wyjścia. Jeśli narzędzie zawiodło — **to samo w sobie
jest naruszeniem**, nie brakiem naruszeń.

## Sprawdź ścieżkę domyślną

Jeśli każdy test jawnie konfiguruje badany parametr, **żaden nie sprawdza wartości domyślnej**,
a to jej używa produkcja. Dopisz przynajmniej jeden test biorący obiekt bez opcji.

Normalizuj konfigurację **po** zastosowaniu opcji, nie tylko przed — inaczej wartość absurdalna
podana z zewnątrz wprowadzi ten sam błąd innymi drzwiami.

## Uruchom dwa razy pod rząd

Pierwszy przebieg na czystym stanie nic nie mówi o drugim. Zanieczyszczenie stanu — wspólna
baza, katalog, kolejka — widać wyłącznie w powtórzeniu.

Asercje zawężaj do **bytu badanego**. Licznik globalny policzy również cudzą pracę.

## Nie mierz własnego artefaktu

Zanim przypiszesz obserwację systemowi, sprawdź, czy nie pochodzi z atrapy, z narzędzia
pomiarowego albo z sąsiedniego testu.

*Awaria:* rzekomy wyciek pamięci okazał się artefaktem testu; rzekomy limit przepustowości
okazał się własnym `time.After`.

## Test zależny od zegara jest testem zegara

Jeśli asercja zależy od tego, czy coś zdąży się wykonać w oknie czasowym — **usuń czas**.
Wygaszaj dzierżawy jawnie, wstrzykuj zegar, przesuwaj go w teście. Sen w teście mierzy sieć.

## Raportowanie

Podawaj polecenie i jego wynik, nie wniosek. Gdy test padł — pokaż wyjście. Gdy coś pominięto —
powiedz to. Gdy zrobione i sprawdzone — stwierdź wprost, bez asekuracji.
