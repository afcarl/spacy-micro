# spaCy parser micro-service wrapper

Small microservice wrapper for spaCy HTTP/HTTPS access from other languages.

## installation
```
pip install -r requirements

# use spacy to download its small model
python -m spacy download en_core_web_sm
```

## run/serve
(see start.sh)
```
gunicorn -k gevent --bind 0.0.0.0:8000 --timeout 120 server:app
```

## docker build and run
```
docker build -t spacy-micro .
```

run locally on port 80
```
docker run -d -p 80:80 --name spacy-micro spacy-micro
```

post some text to the service using curl
```
curl -H "Content-Type: plain/text" -X POST --data "@some-file.txt" http://localhost/parse
```
