#apufunktioita

import string
import secrets

def generate_random_password(length=12):    #salasanan pituus 12 merkkiä
    characters = string.ascii_letters + string.digits + string.punctuation       #luodaan merkkijono(salasana), jossa on isoja ja pieniä kirjaimia, numeroita ja erikoismerkkejä
    random_password = ''.join(secrets.choice(characters) for _ in range(length))   #luodaan random salasana funktion avulla. toistetaan length(12) kertaa
    return random_password