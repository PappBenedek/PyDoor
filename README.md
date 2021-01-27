# PyDoor
### Egy kis buta projektem unaloműzés céljából.
Célkitűzésem az volt, hogy egy elektromos zárat működtessek telefonról.
Egy adott ulr-re lépve basicAuth-os bejelentkezés után (Username/Password) kapunk egy képet, amely egy QR-code.
Ha ezt felmutatjuk a kamerának akkor kinyílik az ajtó.

Működése:
A username / password párokat egy lokális adatbázisban tároljuk, amelyet minden bejelentkezésnél lekérdezünk, hogy valid -e az input.
Amennyiben igen, ezt az eseményt logoljuk, valamint http-n keresztül küldünk egy képet, amelyet akkor generálunk a secret.key-ből.
A secret.key tartalma minden órában változik(lehetne sokkal sűrűbben is, de mivel egyébként is ez csak egy kis buta "játék" mindegy is).

A kamerával 2 mp-én készétünk egy képet, majd megpróbáljuk dekódolni, amennyiben sikerül és a tartalma eggyezik is a secret.key-el akkor triggereljük a 14-es pint,
amely hozzá van kötve egy relayhez amely működteti az elektromos zárat.
