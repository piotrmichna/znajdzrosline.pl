# Aplikacja do zarządzania specyfikacją materiału roślinnego w dokumentacji projektowej dla terenów zieleni

### Apilkacja umieszczona na edukacyjnym VPS (http://mikr.us) dostępna pod adresem http://www.znajdzrosline.pl

## Podstawą aplikacji będzie baza roślin:

```
ROŚLINA (baza główna)
 |
 + Autor
 |
 + Systematyka
 |   |
 |   + Rodzaj (nazwa łacińska, nazwa polska, synonimy, mieszaniec)
 |   |   |
 |   |   + Gatunek (nazwa łacińska, nazwa polska, synonimy, mieszaniec)
 |   |   |   |
 |   |   |   + Odmiana (nazwa odmianowa, synonim)
 |   |   |   |
 |   +---+---+ Roślina (typ pokroju, jadalność)
 |               |
 |               + Opisy (botaniczny, uprawa, zastosowanie)
