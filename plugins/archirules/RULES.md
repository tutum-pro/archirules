# archirules — meta-reguły prowadzenia projektu wytwórczego

**Wersja:** 1.0 · **Język kanoniczny:** polski (przy rozbieżności z `RULES.en.md` rozstrzyga ta wersja)

Metoda wypracowana w praktyce. **Każda reguła poniżej istnieje dlatego, że jej brak coś
zepsuł** — nie dlatego, że dobrze brzmi.

Awarie, z których reguły powstały, opisane są w [`CASEBOOK.md`](CASEBOOK.md) i wskazywane
odnośnikiem `(C-NN)`. Rozdzielenie jest celowe: **regułę ma dać się przeczytać i zastosować
bez znajomości cudzego projektu**, a dowód ma zostać dla tych, którzy chcą wiedzieć, dlaczego
reguła brzmi właśnie tak.

---

## Po co to jest

Projekt wytwórczy przegrywa nie z powodu trudnych decyzji, tylko z powodu decyzji **podjętych
milcząco**: przez kolejność refaktorów, przez domyślną wartość, przez to, że nikt nie zapisał
alternatywy. Pół roku później nikt nie pamięta, czy coś było wyborem, czy przypadkiem.

Ta metoda zamienia decyzje, wątpliwości i dowody w **artefakty pierwszej klasy** — wersjonowane
razem z kodem, przeglądane jak kod, i tak samo jak kod zdolne stać się nieaktualnymi, co też
się odnotowuje.

---

## Artefakty

Wszystko żyje w `docs/architecture/` i jest wersjonowane razem z kodem.

| plik | odpowiada na pytanie |
|---|---|
| `README.md` | co obowiązuje **każdą** nową pracę, nie tylko swój obszar |
| `decisions/ADR-NNNN-*.md` | co postanowiono, czego nie i jakim kosztem |
| `open-questions.md` | czego jeszcze nie wiemy i co to blokuje |
| `fazy-realizacji.md` | co zrobione, co następne, po czym poznamy, że gotowe |
| `rejestr-weryfikacji.md` | co sprawdzone, a co tylko stwierdzone |
| `analiza-*.md` | opcje rozważone **przed** decyzją |

Trzy pierwsze są obowiązkowe od pierwszego dnia. `rejestr-weryfikacji.md` zakłada się przy
pierwszym błędzie wynikającym z niesprawdzonego twierdzenia — i wtedy okazuje się potrzebny.

---

## Reguły prowadzenia

### P1. Proces przed implementacją

Projekt zaczyna się od modelu procesu biznesowego, nie od schematu bazy ani od API. Model jest
artefaktem wersjonowanym, nie obrazkiem w prezentacji.

Konsekwencja praktyczna: jeśli czegoś nie da się pokazać na modelu procesu, prawdopodobnie nie
wiadomo jeszcze, co się buduje.

### P2. Decyzja ma koszty i one też są zapisane

Każdy ADR ma sekcję **„Koszty, przyjęte świadomie"**. Nie „ryzyka", nie „do rozważenia" —
koszty, w trybie oznajmującym, przyjęte.

*Dlaczego:* dokument wymieniający wyłącznie zalety nie jest decyzją, tylko uzasadnieniem po
fakcie. Za pół roku, gdy koszt się zmaterializuje, jedyne pytanie brzmi „czy wiedzieliśmy?".
Ta sekcja jest odpowiedzią.

### P3. Decyzja odrzucona jest zapisana razem z powodem

Sekcja **„Rozważone i odrzucone"** jest częścią ADR-a, nie osobnym dokumentem. Bez niej ktoś
zaproponuje odrzuconą opcję ponownie i nikt nie będzie umiał powiedzieć, dlaczego odpadła.

### P4. Pytanie zarejestrowane, nie rozstrzygnięte milcząco

Wątpliwość, na którą nie ma teraz odpowiedzi, dostaje wpis **OQ-NN** ze statusem, priorytetem
i zależnościami (*blokuje / zależy od / dotyka*).

*Dlaczego:* pytanie niezapisane zostaje rozstrzygnięte przez kolejność, w jakiej ktoś dotknie
plików. To jest rozstrzygnięcie — tylko nikt go nie podjął.

Numeracja jest **ciągła i bez duplikatów**. Numer OQ jest odwołaniem publicznym; dwa pytania
pod jednym numerem sprawiają, że każde odwołanie staje się niejednoznaczne.

### P5. Faza ma kryterium akceptacji ustalone **przed** pracą

Nie „zrobić persystencję", tylko „**instancja przeżywa restart i wznawia się**". Kryterium
zapisane po fakcie zawsze jest spełnione.

### P6. Twarda bramka

Przy podejściu kosztownym lub odwracalnym tylko drogo zapisuje się warunek jego porzucenia,
**zanim** się je zacznie: *„jeśli fazy B1–B5 nie mieszczą się w tygodniu pracy, opcja C była
zła"*.

*Dlaczego:* bez bramki ustalonej wcześniej porzucenie zawsze wygląda na porażkę, więc nikt go
nie zaproponuje.

### P7. Zapis, który przestał być prawdą, koryguje się w zapisie

Gdy dokument mówi coś, co przestało obowiązywać, **nie usuwa się zdania po cichu**. Pisze się,
że przez pewien czas było nieprawdziwe, i od kiedy. ADR zastąpiony dostaje status
**Zastąpiony przez ADR-NNNN** i zostaje w rejestrze — opisuje rozumowanie, które doprowadziło
do zmiany.

*Dlaczego:* rejestr decyzji, który po cichu przepisuje przeszłość, przestaje być dowodem
czegokolwiek. Uwaga praktyczna: **pole statusu i notka nad nim to dwa różne miejsca** — notka
prostująca nad polem, które nadal kłamie, nie jest korektą.
[C-04](CASEBOOK.md#c-04--rejestr-decyzji-ogłaszał-wybór-odwrócony-dzień-wcześniej)

---

## Reguły wykonawcze

Te dotyczą już samej pracy. **Każda pochodzi z konkretnej awarii** — opisanej w
[kazuistyce](CASEBOOK.md).

### W1. Odmawiaj, zamiast zgadywać

Narzędzie, które napotyka coś, czego nie obsługuje, **zatrzymuje się głośno** i mówi, czego
dotyczy problem — najlepiej z odwołaniem do normy, specyfikacji albo decyzji.

Cicha degradacja jest gorsza od odmowy, bo **wygląda jak sukces**. Narzędzie, które robi mniej,
niż mu zlecono, i nie mówi o tym, jest nieodróżnialne od narzędzia, które zrobiło wszystko.
[C-09](CASEBOOK.md#c-09--silnik-który-wykonywał-mniej-niż-narysowano)

### W2. Rozróżniaj „niezaimplementowane" od „niemożliwe z definicji"

To dwa różne komunikaty dla dwóch różnych rozmów. „Jeszcze nieobsługiwane" zaprasza do prośby
o funkcję. „Nie ma semantyki wykonania i nigdy nie będzie" kończy temat.

Ta sama zasada dotyczy granic domenowych: nieznana operacja to literówka i potrzebuje listy
dostępnych; operacja **świadomie odebrana** potrzebuje informacji, **czyja to reguła** i gdzie
po nią iść.

### W3. Weryfikuj, nie twierdź

Twierdzenie o zachowaniu systemu jest warte tyle, ile polecenie, które je pokazuje. Zanim
napiszesz „działa" — uruchom. Zanim napiszesz „jest bezpieczne" — sprawdź obiekt, nie
referencję do niego, i nie wspomnienie o wykonanej pracy.

Dotyczy to również **własnych narzędzi kontrolnych**: wynik kontroli jest twierdzeniem
o dokumencie albo o kodzie, więc podlega tej samej regule. Zanim zgłosisz brak — otwórz plik.
[C-05](CASEBOOK.md#c-05--kontroler-szukał-liczby-mnogiej-i-nie-widział-pojedynczej) ·
[C-08](CASEBOOK.md#c-08--klucz-prywatny-przeżył-czyszczenie-historii)

### W4. Kontrola, która nie potrafi paść, wygląda identycznie jak kontrola, która przechodzi

**Nowa bramka nie jest gotowa, dopóki nie pokazano, że pada.** Zepsuj celowo, uruchom, obejrzyj
błąd, cofnij. Zapisz w commicie, na jakich kształtach naruszenia ją sprawdzono.

Dotyczy to również **siatek bezpieczeństwa**: licznik pilnujący, czy kontrola w ogóle się
wykonała, musi być luźniejszy od kontroli, którą pilnuje. Uszczelniony razem z nią przestaje
cokolwiek pilnować.
[C-01](CASEBOOK.md#c-01--bramka-która-nie-potrafiła-paść) ·
[C-06](CASEBOOK.md#c-06--zmiana-znaku-interpunkcyjnego-wyłączyła-trzydzieści-siedem-kontroli) ·
[C-07](CASEBOOK.md#c-07--uszczelnienie-siatki-bezpieczeństwa-oślepiło-ją)

### W5. Nie wyciszaj błędów w bramce

`2>/dev/null`, `|| true` i ignorowany kod wyjścia zamieniają awarię narzędzia w wynik
pozytywny. Jeśli narzędzie zawiodło, **to samo w sobie jest naruszeniem**.

### W6. Test nie może konfigurować tego, co testuje

Jeśli każdy test jawnie ustawia parametr, żaden nie sprawdzi wartości domyślnej — a to jej
używa produkcja.

[C-02](CASEBOOK.md#c-02--sześć-testów-przeszło-mimo-zepsutej-wartości-domyślnej)

### W7. Uruchom dwa razy pod rząd

Pierwszy przebieg na czystym stanie niczego nie mówi o drugim. Testy dzielące bazę,
katalog albo kolejkę wykrywa się wyłącznie powtórzeniem.

[C-03](CASEBOOK.md#c-03--zestaw-testów-przeszedł-raz-i-padł-za-drugim-razem)

### W8. Nie mierz własnego artefaktu

Zanim przypiszesz obserwację systemowi, sprawdź, czy nie pochodzi z narzędzia pomiarowego,
z atrapy albo z sąsiedniego testu. Asercje zawężaj do bytu badanego, nie do stanu globalnego.
[C-10](CASEBOOK.md#c-10--pomiar-własnego-narzędzia-pomiarowego)

### W9. Mechanizm ponad konwencję — a gdy się nie da, nazwij to konwencją

Regułę, którą da się sprawdzić maszynowo, sprawdzaj maszynowo. Regułę, której nie da się —
zapisz **jawnie jako konwencję przeglądu**, razem z sygnałem ostrzegawczym, po którym się ją
rozpoznaje.

*Dlaczego:* reguła udająca egzekwowaną, a nieegzekwowana, jest gorsza od jawnej konwencji —
bo nikt jej nie pilnuje, wszyscy sądzą, że ktoś inny.

### W10. Granica biblioteki: liczy, nie sięga po świat

Rdzeń obliczeniowy nie dotyka wejścia-wyjścia. Czego potrzebuje ze świata, **deklaruje jako
interfejs u siebie**; wdrożenie go dostarcza.

*Test jednozdaniowy:* **jeżeli test biblioteki potrzebuje port-forwarda, granica jest w złym
miejscu.**

---

## Rytm pracy

1. **Zanim zaczniesz fazę** — zapisz kryterium akceptacji w rejestrze faz.
2. **Gdy napotkasz wątpliwość** — OQ, nie decyzja w locie.
3. **Gdy podejmiesz decyzję** — ADR z kosztami i odrzuconymi opcjami.
4. **Gdy zbudujesz bramkę** — udowodnij, że pada.
5. **Gdy zamykasz fazę** — dowód, nie deklaracja; dwa przebiegi.
6. **Okresowo** — audyt kompletności (`/archirules:audyt`).

---

## Czego ta metoda **nie** robi

- **Nie zastępuje przeglądu kodu.** Rejestry pilnują decyzji, nie implementacji.
- **Nie działa bez utrzymania.** Rejestr nieaktualizowany jest gorszy niż jego brak, bo
  wygląda na aktualny. Stąd reguła P7 i skill audytu.
- **Nie przenosi bramek mechanicznych między projektami.** Konkretne kontrole są kodem danego
  repozytorium; metoda niesie wzorzec i listę kontrolną.
- **Nie chroni przed złą decyzją.** Sprawia tylko, że zła decyzja jest widoczna, datowana
  i ma zapisaną alternatywę.
