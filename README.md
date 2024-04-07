# Tehtävälista-sovellus
Sovellus ei ole testattavissa Fly.iossa.

Sovelluksen ominaisuuksia:

- Käyttäjä voi luoda uuden tunnuksen ja kirjautua sisään sovellukseen
- Käyttäjä voi luoda tehtävälistoja/muistiinpanoja, lisätä tehtäviä niihin
- Käyttäjä voi määrittää tehtävien nimen, kuvauksen, määräajan ja mahdollisesti muita tietoja
- Sovellus voi lähettää käyttäjille muistutuksia määräajoista ja push-ilmoituksia
- Käyttäjät voivat asettaa prioriteetit tehtäville ja järjestää ne tärkeysjärjestykseen tai luokitteluun esimerkiksi aiheen tai deadline-päivämäärän mukaan
- Käyttäjä voi hakea tehtäviä nimen, kuvauksen tai muiden kriteerien perusteella
- Mahdollisuus asettaa tehtäville toistuvuus, esim. päivittäin, viikoittain tai kuukausittain
- Käyttäjä voi kirjoittaa jo olemassa olevaan tehtävään
- Käyttäjä voi muokata tehtävänimikettä ja sen sisältöä sekä määräaikaa


Tällä hetkellä:
- Käyttäjä voi luoda uuden tunnuksen ja kirjautua sisään sovellukseen.
- Käyttäjä voi luoda muistiinpanoja/tehtäviä 
- Käyttäjä voi muokata ja poistaa muistiinpanoja
- Sovellus näyttää, onko käyttäjä kirjautuneena sisään, millä käyttäjänimellä


Käynnistysohjeet:

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run
