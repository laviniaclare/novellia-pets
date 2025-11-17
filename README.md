# Minimal Flask skeleton

This repository contains a minimal Flask skeleton app with a single home endpoint.

How to run (recommended: inside a virtualenv):

```bash
# install deps
pip install -r requirements.txt

# run the app
python run.py

# or, using the app module directly
python -m app
```

The home endpoint is at: http://127.0.0.1:5000/

Tests

```bash
pip install -r requirements.txt
pytest -q
```
