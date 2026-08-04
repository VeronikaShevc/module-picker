# St Andrews CS Module Picker

A tool that helps University of St Andrews Computer Science students figure out
which modules they're actually eligible to take next, based on what they've
already passed.

## Why I built this

Choosing modules for my final year, I found myself manually cross-referencing
prerequisite chains across dozens of module catalogue pages, one at a time -
checking whether I'd passed the right combination of earlier modules, whether
a module conflicted with something I'd already taken, and whether something
I wanted required a module I hadn't done yet. It was slow and easy to get
wrong. This tool automates that process.

## What it does

- Scrapes real, current module data directly from the official St Andrews
  module catalogue and CS Student Handbook (name, credits, semester,
  assessment split, exam duration, prerequisites, anti-requisites, SCQF
  level, weekly contact hours)
- Lets you tick which modules you've already passed
- Automatically works out which remaining modules you're eligible for, using
  a boolean logic parser that handles real prerequisite text - AND/OR logic,
  bracketed conditions, undergraduate/postgraduate variants, and
  anti-requisite conflicts
- Distinguishes between genuinely **not eligible**, **pending** (blocked only
  by a module you'd take in the same year), and **unclear** (the
  prerequisite text can't be reliably parsed)
- Filters by year, assessment type, and exam duration
- Remembers your selections across filter changes using local storage

## Tech stack

- **Backend:** Python, FastAPI
- **Templating:** Jinja2
- **Scraping:** BeautifulSoup, requests
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Testing:** pytest

## How to run it locally

git clone https://github.com/VeronikaShevc/module-picker.git
cd module-picker
pip install -r requirements.txt
uvicorn app:app --reload

Then open `http://localhost:8000` in your browser.

## Running the tests

pytest tests/ -v

## Known limitations

- Scoped to single Honours BSc/MSci Computer Science - joint Honours
  combinations and other departments' modules aren't accounted for.
- Direct entry to Year 2 (students who skip Year 1 via the accelerated
  CS2101 module) isn't fully supported yet in the year-selection flow.
- A handful of modules have prerequisite or anti-requisite text that can't
  be reliably parsed - either because it references a module outside this
  dataset, or because it's a subjective/non-module condition (e.g. a grade
  requirement). These are marked **unclear** rather than guessed at.
- The weekly contact hours parser correctly structures around 70% of
  modules' schedule text; the rest fall back to the raw catalogue text.
- No support yet for postgraduate-specific (PGT) prerequisite rules where
  they differ from the undergraduate ones.