import os
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from clean import clean_rows

ROOT = Path(__file__).resolve().parent
SAMPLE = (ROOT / "messy.csv").read_text(encoding="utf-8")
app = FastAPI(title="rowclean")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=str(ROOT / "templates"))


def page(request: Request, **extra):
    context = {"draft": "", "kept": None, "rejected": None, "output": ""}
    context.update(extra)
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return page(request)


@app.post("/clean", response_class=HTMLResponse)
def clean(request: Request, text: str = Form(...)):
    kept, rejected, output = clean_rows(text)
    return page(request, draft=text, kept=kept, rejected=rejected, output=output)


@app.post("/sample", response_class=HTMLResponse)
def sample(request: Request):
    kept, rejected, output = clean_rows(SAMPLE)
    return page(request, draft=SAMPLE, kept=kept, rejected=rejected, output=output)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
