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