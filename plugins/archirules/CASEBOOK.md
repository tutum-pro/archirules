# Kazuistyka — skąd wzięły się reguły

Każda reguła w [`RULES.md`](RULES.md) powstała z konkretnej awarii. Awarie są tutaj, oddzielnie,
z trzech powodów:

1. **Reguła musi dać się przeczytać bez nich.** Kto sięga po metodę, chce wiedzieć, co robić,
   a nie poznawać cudzy projekt.
2. **Dowód musi zostać.** Reguła bez awarii jest życzeniem; z awarią jest wnioskiem. Usunięcie
   przypadków zabrałoby jedyny powód, dla którego warto je stosować.
3. **Przypadek daje się rozpoznać u siebie.** Nie chodzi o to, żeby wiedzieć, co się stało
   w cudzym projekcie, tylko żeby zobaczyć ten sam kształt we własnym.

Wszystkie pochodzą z jednego projektu — platformy leasingowej budowanej w Go — ale opisane są
tak, żeby dało się je zrozumieć bez znajomości tamtego kodu. Gdzie potrzebny jest szczegół
techniczny, jest wyjaśniony.

---

## C-01 — Bramka, która nie potrafiła paść

**Reguła:** [W4](RULES.md#w4-kontrola-która-nie-potrafi-paść-wygląda-identycznie-jak-kontrola-która-przechodzi)

Powstała kontrola pilnująca, żeby biblioteki rdzenia nie importowały infrastruktury. Szukała
zakazanych importów wyrażeniem regularnym wymagającym wcięcia — bo w wielu językach importy
zgrupowane są wcięte.

Uruchomiona na celowo zepsutej bibliotece zameldowała **„czysto"**. Import jednolinijkowy nie
ma wcięcia, więc wzorzec go nie widział.

Poprawiona wersja wołała narzędzie języka zamiast grepować źródła — i **znowu przeszła**, bo
błąd narzędzia leciał na stderr przekierowany do `/dev/null`, a pusty wynik czytało się jako
brak naruszeń.

**Jak wyszło:** przez celowe zepsucie kodu i sprawdzenie, czy bramka pada. Nie przez czytanie
jej implementacji — obie wersje wyglądały poprawnie.

---

## C-02 — Sześć testów przeszło mimo zepsutej wartości domyślnej

**Reguła:** [W6](RULES.md#w6-test-nie-może-konfigurować-tego-co-testuje)

Do silnika dodano ponawianie kroków z limitem prób. Napisano sześć testów: ponawia, przestaje
po limicie, odczekuje coraz dłużej, nie ponawia błędu trwałego. Wszystkie przechodziły.

Limit prób wynosił **zero**, a wstrzykiwany zegar był `nil`. Każda pierwsza awaria była
traktowana jako „skończyły się próby", a ścieżka odczekiwania spanikowałaby, gdyby kiedykolwiek
ruszyła.

Powód: **każdy z sześciu testów jawnie podawał własną konfigurację**. Ścieżka domyślna — ta,
której używa produkcja — nie wykonała się ani razu.

**Jak wyszło:** przy okazji innego błędu, gdy jeden test zaczął zachowywać się inaczej, niż
mówiła dokumentacja. Gdyby nie to, weszłoby na produkcję.

---

## C-03 — Zestaw testów przeszedł raz i padł za drugim razem

**Reguła:** [W7](RULES.md#w7-uruchom-dwa-razy-pod-rząd)

Testy integracyjne dzieliły jedną bazę. Przeszły. Uruchomione ponownie — padły: jeden test
zostawiał w bazie obiekt, który drugi test liczył jako swój.

Wersja pierwsza zestawu **przechodziła wyłącznie na czystej bazie**, czyli dokładnie raz.

**Jak wyszło:** przez uruchomienie dwa razy pod rząd, bez czyszczenia. Nie ma innego sposobu.

---

## C-04 — Rejestr decyzji ogłaszał wybór odwrócony dzień wcześniej

**Reguła:** [P7](RULES.md#p7-zapis-który-przestał-być-prawdą-koryguje-się-w-zapisie)

Wybrano gotowy silnik przepływów i zapisano decyzję. Nazajutrz analiza wykazała, że silnik
**po cichu pomija konstrukcje, których nie umie wykonać** — diagram z kompensacją uruchamiał
się i nie kompensował niczego. Decyzję odwrócono i zbudowano własny kompilator.

Przez dobę rejestr decyzji nadal ogłaszał pierwszy wybór jako obowiązujący. Kto by go
przeczytał, wyciągnąłby wniosek wprost przeciwny do tego, co było budowane.

Gorzej: pole `Status` w powiązanym pytaniu otwartym wskazywało odwróconą decyzję **jeszcze
przez kolejny dzień**, mimo że nad nim wisiała notka o odwróceniu. Notka prostowała, pole
kłamało.

**Jak wyszło:** przy audycie kompletności, na pytanie „czy gdyby ktoś przeczytał tylko ten
dokument, wyciągnąłby wniosek zgodny z tym, co zbudowano?".

---

## C-05 — Kontroler szukał liczby mnogiej i nie widział pojedynczej

**Reguła:** [W3](RULES.md#w3-weryfikuj-nie-twierdź), [W9](RULES.md#w9-mechanizm-ponad-konwencję--a-gdy-się-nie-da-nazwij-to-konwencją)

Audyt zgodności zgłosił, że **sześć fundamentalnych rekordów decyzji nie ma sekcji kosztów**.
Zaplanowano dopisanie jej do wszystkich sześciu.

Sekcję miały wszystkie. Sześć z nich używało liczby pojedynczej — „Koszt." zamiast „Koszty." —
a wzorzec kontrolera wymagał mnogiej.

O mało nie doszło do dopisania treści, która już istniała. Zapobiegł temu jeden warunek
postawiony przez zamawiającego: **poprawki mają wynikać z faktów, nie z domysłu** — co zmusiło
do otwarcia plików zamiast zaufania wynikowi.

**Wniosek, który z tego wyszedł:** dopasowuj **prefiksy**, nie pełne brzmienia. Wariant językowy
nie jest niezgodnością. „Koszt." przy jednym koszcie jest poprawne.

---

## C-06 — Zmiana znaku interpunkcyjnego wyłączyła trzydzieści siedem kontroli

**Reguła:** [W4](RULES.md#w4-kontrola-która-nie-potrafi-paść-wygląda-identycznie-jak-kontrola-która-przechodzi)

Przy próbnym przełączeniu dokumentacji na inny język tłumacz zapisał nagłówki pytań otwartych
z dywizem `-` zamiast myślnika `—`.

Kontroler rozpoznał **zero z trzydziestu sześciu** pytań. Kontrola numeracji, duplikatów
i statusów przestała obowiązywać. Zameldował **„czysto"**.

Liczba wykonanych sprawdzeń spadła ze 168 do 131 i **nic tego nie zgłosiło**.

**Naprawa nie jest łatką na myślnik.** Kontroler porównuje teraz liczbę nagłówków
*wyglądających* na pytania z liczbą *sparsowanych* — czyli rozlicza pokrycie własnego parsera.
Dowolny przyszły dryf formatu pada głośno, zamiast wyłączać sekcję.

**Jak wyszło:** przez przećwiczenie procedury na kopii prawdziwego rejestru, zanim ktokolwiek
uruchomił ją na oryginale.

---

## C-07 — Uszczelnienie siatki bezpieczeństwa oślepiło ją

**Reguła:** [W4](RULES.md#w4-kontrola-która-nie-potrafi-paść-wygląda-identycznie-jak-kontrola-która-przechodzi)

Bezpośrednio po C-06 dodano właśnie ten licznik pokrycia. Przy okazji zaostrzono wzorzec
rozpoznający nagłówek, żeby nie łapał wpisu archiwalnego jako duplikatu.

Zaostrzenie objęło **oba** liczniki: i parser, i siatkę. Przy kolejnej deformacji nagłówka —
dwukropek zamiast myślnika — obie liczby spadły do zera równocześnie, `0 == 0`, kontrola
przeszła.

**Siatka bezpieczeństwa musi liczyć najluźniej jak się da.** Wykluczać wolno wyłącznie znane,
celowe wyjątki. Uszczelniona razem z tym, co ma pilnować, przestaje pilnować czegokolwiek.

**Jak wyszło:** przez sprawdzenie siatki na deformacji, której nie przewidziano przy jej
pisaniu.

---

## C-08 — Klucz prywatny przeżył czyszczenie historii

**Reguła:** [W3](RULES.md#w3-weryfikuj-nie-twierdź)

Z historii repozytorium usunięto zacommitowany klucz prywatny certyfikatu. Operację uznano za
zakończoną.

Została gałąź zapasowa, utworzona przed czyszczeniem **właśnie po to, żeby mieć kopię**. Nadal
zawierała klucz. Jedno rutynowe `git push --all` cofnęłoby całą operację.

**Jak wyszło:** przy przeglądzie kompletności dokumentacji, przez sprawdzenie **stanu
faktycznego** (`git branch`, obecność obiektu w bazie) zamiast wspomnienia o wykonanej pracy.

Przy usuwaniu tej gałęzi pierwsze dwa skany historii również zameldowały „czysto", będąc
bezwartościowymi: raz przez błąd wyrażenia regularnego wypisany na stderr i zignorowany, raz
przez to, że powłoka nie dzieliła zmiennej na słowa i pętla zrobiła jeden obieg zamiast
jedenastu. Wykryło to **rozliczenie pokrycia** — licznik „przeskanowanych" kontra „wszystkich",
który przy niezgodności odmawia orzeczenia.

---

## C-09 — Silnik, który wykonywał mniej, niż narysowano

**Reguła:** [W1](RULES.md#w1-odmawiaj-zamiast-zgadywać), [W2](RULES.md#w2-rozróżniaj-niezaimplementowane-od-niemożliwe-z-definicji)

Rozważany silnik przepływów przyjmował diagramy zawierające konstrukcje, których nie
implementował, i **pomijał je bez słowa**. Diagram ze zdarzeniem kompensacji uruchamiał się
i nie kompensował niczego. Nic w logu, nic w wyniku — po prostu mniej, niż napisano.

Dla systemu, w którym kompensacja jest podstawą spójności, była to awaria dyskwalifikująca.

**Wniosek szerszy niż wybór biblioteki:** narzędzie, które napotyka coś, czego nie obsługuje,
ma się **zatrzymać głośno**. Cicha degradacja jest gorsza od odmowy, bo wygląda jak sukces.

---

## C-10 — Pomiar własnego narzędzia pomiarowego

**Reguła:** [W8](RULES.md#w8-nie-mierz-własnego-artefaktu)

Dwukrotnie zaraportowano wynik pomiaru jako właściwość systemu, gdy pochodził z testu:
rzekomy wyciek pamięci okazał się artefaktem samego testu, a rzekomy limit przepustowości —
opóźnieniem wpisanym w pętlę testową.

**Jak wyszło:** przez pytanie „co dokładnie mierzy ten pomiar" zadane, zanim wynik trafił do
wniosków.

## C-11 — Kontrola bez własnego przypadku testowego nie potrafiła zadziałać

**Reguła:** W4, W8

Kontroler międzyrejestrowy przechodził dwadzieścia osiem przypadków własnego selftestu. Jedna z
pięciu kontroli, które ogłaszał, nie potrafiła zadziałać w żadnych okolicznościach: szukała
markera i numeru pytania **w jednej linii** — układu, którego żaden szablon nie produkuje. Była
też jedyną kontrolą bez przypadku testowego u siebie, więc nic tego nie zauważyło.

Przyczyna leżała głębiej niż brakujący przypadek. Kontroler posługiwał się słownictwem, które
sam wymyślił — polami i nagłówkami nieobecnymi w szablonach, w skillach i w regułach — a zestaw
testowy napisano tym samym słownictwem. Zgadzały się ze sobą i to była cała treść dowodu.
Rejestr zbudowany dokładnie według instrukcji metody ten kontroler zgłaszał jako wadliwy.

**Jak wyszło na jaw:** przez zbudowanie rejestru według instrukcji, a nie według zestawu
testowego. Mechanizm, który tego teraz pilnuje, jako jedyny wychodzi poza pliki testowe:
selftest wymaga, żeby **każdy marker kontrolera występował w szablonie albo w skillu**.

Dopisek z tej samej naprawy: nowa asercja przeszła, kiedy kontroler, który mierzyła, przestał
się w ogóle importować. Pusty wynik czytał się jak „niczego nie brakuje". Asercja o wyniku
działania narzędzia musi odróżniać „nic nie znalazłem" od „nie zdołałem uruchomić" — sentynela,
nie pusty łańcuch.
