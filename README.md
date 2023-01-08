# TextSteganographyApp
Text steganography console application  - my thesis. 

Wiodącym celem aplikacji jest steganografia (ukrywanie) tekstu w plikach graficznych formatu BMP w przestrzeni barw RGB oraz dekodowanie ukrytych informacji. Program jest oparty  na metodzie najmniej znaczącego bity - LSB (Least Significant Bit).
## Instrukcja obsługi aplikacji
Aplikacja została napisana w języku Python, przy pomocy zintegrowanego środowiska PyCharm. Funkcjonowanie aplikacji oparte jest na ogólnodostępnej bibliotece Pillow. Należy ją zainstalować. Pod warunkiem, że mamy prawidłowo zainstalowanego pythona z modułem pip, należy wpisać w terminalu: pip install Pillow.
### Uruchomienie
W celu uruchomienia programu należy przy pomocy środowiska PyCharm uruchomić plik z kodem źródłowym o nazwie main.py. Następnie należy podać program procesowi kompilacji przy użyciu skrótu klawiszowego Shift+F10.

### Instrukcja programu
Po zakończeniu sukcesem procesu kompilacji pojawi nam się ekran startowy aplikacji okienkowej, który prezentuje się następująco.
![image](https://user-images.githubusercontent.com/32534922/211213913-b066145f-945f-4c65-92dd-b0b2a2cdafb6.png)

W ekranie głównym znajdują się przyciski takie jak: „Otwórz obraz” - służący do otwierania plików graficznych, „Zapisz obraz” - służący do zapisywania zachodzących zmian w pliku graficznym, przycisk do wybrania ilości bitów, na których chcemy kodować informacje w obrazie(1-8), „Zakoduj tekst powyżej” - pozwalający zakodować informację z pola tekstowego znajdującego się nad przyciskiem oraz „Odkoduj tekst z obrazka”, który odpowiada za odkodowanie ukrytych informacji w obrazie i wyświetlenie ich w polu tekstowym znajdującym się nad tym przyciskiem. Pokazana jest również informacja o rozmiarze danego obrazu oraz znajdujący się pod nią komunikat o maksymalnej ilości znaków, które zmieszczą się w pliku graficznym przy wybranej ilości bitów.

Pierwszym krokiem, który należy wykonać jest załadowanie obrazu z dysku twardego przy użyciu przycisku „Otwórz obraz”. Po kliknięciu przycisku otworzy się okienko, w którym trzeba wybrać obraz w formacie BMP za pomocą przycisku „Otwórz”.
![image](https://user-images.githubusercontent.com/32534922/211213952-302dece1-f4fb-4585-9de4-bbee3b1654d1.png)

Po wyborze obrazu zostanie on wyświetlony po prawej stronie aplikacji. Z lewej strony zaktualizuje się komunikat o wymiarach obrazka oraz pojemności znaków przy wybranej ilości bitów do zakodowania.

![image](https://user-images.githubusercontent.com/32534922/211213964-e48bbbf5-e73f-4567-9955-2637df61d267.png)

Po załadowaniu obrazu, należy wybrać odpowiednią ilość bitów, na których będziemy kodować komunikat, a następnie w polu znajdującym się nad przyciskiem „Zakoduj tekst powyżej” należy wpisać informacje, które będą ukryte i zatwierdzić kliknięciem przycisku. Na koniec trzeba użyć przycisku „Zapisz obraz” w celu zapisania zmian, które zaszły oraz nadać nazwę pliku z rozszerzeniem .bmp. 
Po wybraniu przycisku „Zapisz obraz” aplikacja otworzy nam okno wyboru lokalizacji zapisu pliku.

Po pomyślnym zapisaniu obrazu aplikacja wygląda następująco.

![image](https://user-images.githubusercontent.com/32534922/211214044-86029cbc-0162-4968-8da5-3f850bcf809c.png)

W celu odkodowania wiadomości należy wczytać obraz z komputera poprzez użycie przycisku „Otwórz obraz”. Następnie wybrać liczbę bitów, na których była kodowana wiadomość i posłużyć się przyciskiem „Odkoduj tekst z obrazka”.

![image](https://user-images.githubusercontent.com/32534922/211214066-8eb33804-8135-4f9c-8898-1d815744b778.png)

Zmiany zachodzące w obrazie podczas kodowania informacji są niemal niezauważalne dla ludzkiego oka, w szczególności, gdy kodowanie odbywa się na małej ilości bitów. Dopiero przy ogromnej liczbie kodowanych znaków oraz przy wyborze większej ilości bitów, na których będzie wykonywana operacja kodowania, możemy dostrzec zmiany w obrazie.

#### O aplikacji
Działanie programu oparte jest na operacji podmiany najmniej znaczących bitów dla poszczególnych kolorów pikseli obrazu. W standardowym obrazie formatu BMP RGB każdemu z kolorów przypisany jest jeden bajt. Jego wartość numeryczna odpowiada stopniowi nasycenia danego piksela tym kolorem. Z wymieszania trzech kolorów podstawowych o różnym natężeniu powstaje wypadkowy, oryginalny kolor piksela. Działanie programu opiera się na obserwacji, że zmiana najmniej znaczących bitów opisujących intensywność poszczególnych kolorów jest praktycznie niezauważalna dla ludzkiego oka. W praktyce zmiana najmniej znaczącego bitu sprowadza się do zmiany wartości liczbowej nasycenia koloru np. z 124 na 125 w skali od 0 do 255.

Prezentowany program pozwala użytkownikowi na wybór ilości najmniej znaczących bitów dla każdego koloru każdego piksela, które zostaną użyte do kodowania treści. Pozwala to na zwiększenie rozmiaru zapisanej w danym obrazie wiadomości, ale kosztem zwiększenia szansy, że obserwator dostrzeże, że obraz był modyfikowany.

Zastosowane kodowanie polega na zamianie całego tekstu na ciąg bitów, zgodnie z tabelą ASCII, a następnie nadpisaniu odpowiednich bitów obrazu bitami naszego ciągu. Analogicznie dekodowanie polega na odczytaniu odpowiednich bitów z obrazu i ich interpretacji jako znaków zgodnie z tabelą ASCII. Żeby program „wiedział” kiedy skończyć dekodowanie, do kodowanego ciągu bitów zostaje doklejony tzw. „znak końca ciągu” – osiem zerowych bitów. Dlatego też, kiedy dekodując program napotka ciąg ośmiu zer, przerywa swoje działanie i nie interpretuje dalszych bitów jako tekstu.
