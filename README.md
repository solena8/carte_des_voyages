# Deploy
## Deploy All

```bash
firebase deploy
```

## Deploy hosting

```bash
firebase deploy --only hosting
```

## Deploy functions

```bash
firebase deploy --only functions
```

# Run locally

Install dependencies
```bash
pip install -r functions/requirements.txt
```

Run firebase emulator
```bash
firebase emulators:start
```

Create a fake place:
```
http://127.0.0.1:5001/carte-des-voyages-tug-solena/us-central1/create_fake
```


List places:
```
http://127.0.0.1:5001/carte-des-voyages-tug-solena/us-central1/list
```

a