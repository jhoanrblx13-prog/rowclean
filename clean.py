import csv
import io
import re
from pathlib import Path

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PLANS = {"desk", "bench", "yard", "shed"}
FIELDS = ["name", "email", "plan"]


def clean_rows(text: str) -> tuple[list[dict], list[dict], str]:
    kept = []
    rejected = []
    seen = set()
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or any(name not in reader.fieldnames for name in FIELDS):
        return [], [{"line": 1, "reason": "header must be name,email,plan", "value": ""}], ""
    for line_no, row in enumerate(reader, start=2):
        name = (row.get("name") or "").strip()
        email = (row.get("email") or "").strip().lower()
        plan = (row.get("plan") or "").strip()
        if not name:
            rejected.append({"line": line_no, "reason": "blank name", "value": email})
            continue
        if not EMAIL.match(email):
            rejected.append({"line": line_no, "reason": "bad email", "value": email or (row.get("email") or "")})
            continue
        if plan.lower() not in PLANS:
            rejected.append({"line": line_no, "reason": "unknown plan", "value": plan})
            continue
        if email in seen:
            rejected.append({"line": line_no, "reason": "duplicate email", "value": email})
            continue
        seen.add(email)
        kept.append({"name": name, "email": email, "plan": plan})
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(kept)
    return kept, rejected, output.getvalue()


def clean_file(source: Path, dest: Path) -> tuple[list[dict], list[dict]]:
    kept, rejected, output = clean_rows(source.read_text(encoding="utf-8"))
    dest.write_text(output, encoding="utf-8")
    return kept, rejected
