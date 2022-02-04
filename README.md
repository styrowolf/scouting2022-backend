# scouting2022-backend

Installing dependencies: 
```sh
pip3 install -r requirements.txt
```

to-do:
- [] add export to spreadsheet function
    - probably generate the xlsx server-side, upload it unto deta drive
    and serve it using an one-time link via FastAPI
- [] add registration check via mail
    - send a mail containing a link that has the key of the new registration in a new database
    - when that link is clicked move that registration to the auth database
- [] have an easy way for team owners to add their teammates to their team

