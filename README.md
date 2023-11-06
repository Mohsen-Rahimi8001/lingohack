# LingoHack
The program is gonna help me store new stuff that I learn in English.

## you should create a .env file and put these information in it
```
SECRET_KEY=<jwt secret key>
ALGORITHM=<"HS256" or "RSA-OAEP" or ...>
```

## you can see the list of algorithms in
https://www.iana.org/assignments/jose/jose.xhtml

## run web application
#### activate virutal environment
```source venv/bin/activate```

#### install required packages
```pip install -r requirements.txt```

#### run the app
```uvicorn main:app --reload --port=<port number>```

#### see the overview of the api
```<domain name>:<port number>/docs```
