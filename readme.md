# Projet OCR

##Lancement

Pour exécuter le projet, il faut ouvrir deux terminaux dans lequel il faudra lancer

1) python3 paint.py

2.1) cd look/
2.2) waitress-serve --port=8000 look:app.api

Pour Linux
2.3) gunicorn look.app.api