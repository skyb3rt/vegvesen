## VEGVESEN
Enkel app for å hente kjøretøyinformasjon fra vegvesen.no


### Avhengigheter:
Api nøkkel hentes ut fra Din Side på vegvesen.no og fylles ut i .env filen.

### Henting av kjøretøyinformasjon:
pip install -r requirements.txt

Kjennemerke fylles ut i app/main.py

python app/main.py

kjøretøyinformasjon blir lagret som json fil i output katalogen

### eksempel på utskrift:
kjennemerke='DP99999', merke='FORD', modell='MONDEO', kw=92.0, kontrollfrist='2025-04-30'
