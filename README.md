## MariaDB i Docker (MacOS, Win og Linux)
Skriv dette i Terminal
```
docker pull mariadb
```
Så lager du og kjører en container slik:
```
docker run --name munchbase -e MYSQL_ROOT_PASSWORD=munchies -p 3306:3306 -d mariadb
```
To check if the container is up and running you can use below commands.
For å se om containeren kjører så skriver du først:
```
docker exec -it munchbase mysql -u root -p...
```
Deretter:
```
show databases;
```
####  Tilkobling gjøres med disse parameterne:
Host = **127.0.0.1**
user = **root**
password = **Munchies**
---
## For Windows UTEN Docker
#### Last ned og installer pycharmhttps://www.jetbrains.com/pycharm/download/#section=windows
Registrer deg med uit-epost for å få gratis tilgang 
#### Last ned og installer mariadbhttps://mariadb.org/download/?t=mariadb&p=mariadb&r=10.7.3&os=windows&cpu=x86_64&pkg=msi&m=dotsrc
- Velg passord "munchies"  
- Huk av for UTF8
![mariaDB_install_1](https://user-images.githubusercontent.com/98937880/154868769-7f317a29-1109-45bd-a5e2-23c48ac878d3.png)
Behold alt som default her  
![mariaDB_install_2](https://user-images.githubusercontent.com/98937880/154868776-a0fa6d99-c317-4a4d-8d16-9dbc74a318ad.png)
#### Installer requirements
Installer requirements med pip ved hjelp av requirements.txt
#### Kjør sysut_template
Kjør server.py i backend-modulen
Du får da opp en link som peker til 127.0.0.1:5000/
Klikk på linken og verifiser at du får opp "Hello Munchies" i nettleseren din
#### Opprett database
Opprett database ved å kjøre local_db_create.py
#### Oppdater lokale verdier i database
Oppdater lokale verdier i database ved å kjøre local_db_update.py
Download PyCharm: Python IDE for Professional Developers by JetBrains
Download the latest version of PyCharm for Windows, macOS or Linux.

Download PyCharm: Python IDE for Professional Developers by JetBrains
Download the latest version of PyCharm for Windows, macOS or Linux.

