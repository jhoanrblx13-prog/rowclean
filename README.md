# rowclean

Paste a customer CSV. It drops blank names, bad emails, unknown plans, and duplicate emails, then shows the clean file and the rejected lines.

Header has to be `name,email,plan`. Plans it keeps: Desk, Bench, Yard, Shed.

## Run

```bash
cd rowclean
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open http://127.0.0.1:8000

The command-line version is still there: `python clean.py` is not the server. Use `python main.py`.
