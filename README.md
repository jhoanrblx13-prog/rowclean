# rowclean

Paste a customer CSV. It drops blank names, bad emails, unknown plans, and duplicate emails, then shows the clean file and the rejected lines.

Demo: https://rowclean.onrender.com

Header has to be `name,email,plan`. Plans it keeps: Desk, Bench, Yard, Shed.

## Run

```bash
cd rowclean
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
