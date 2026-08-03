# Learn Local AI — build your own, from a blank PC

A free, start-to-finish course in one document: **[GUIDE.md](GUIDE.md)**.

You start with a Windows computer that has nothing installed. You end with a local
AI model running on your own machine, a chat client you wrote yourself in ~25 lines
of standard-library Python, tools ("hands") with a real security boundary, and a
windowed GUI. No account, no API key, no subscription, no cloud — your prompts
never leave your machine.

## What's in here

- **[GUIDE.md](GUIDE.md)** — the whole course. Thirteen parts, every command stating
  its expected output before you run it, every code listing complete and runnable.
- **[samples/](samples/)** — the finished version of each file the course builds
  (`chat1.py` → `gui1.py`), for when you're stuck. You'll learn more typing them.

## Who it's for

Anyone who can open PowerShell and wants to actually understand the thing, not just
use it. No AI background assumed. The course also teaches, on purpose, how to read
code you didn't write and how to think about AI safety as an engineering problem —
the model proposes, your code disposes.

## Highlights

- **Part 3: pick the model that fits YOUR graphics card** — how to find your VRAM,
  the fitting rule, a tier table from CPU-only to 96 GB with example models and
  ballpark speeds, and how to benchmark your own machine instead of trusting tables.
- **Part 4: the flagships** — gpt-oss:120b and GLM-4.5-Air end to end: what each
  really requires, every step to get one running, and how to run any open model
  straight off Hugging Face.
- **Part 9: hands with a jail** — tool calling with a real security boundary you
  build and then attack yourself. The write-side discipline (preview/apply,
  backup-before-write, the typed-YES gate) is the live half: taught free at
  [VetTech Homefront](https://vettechhomefront.com) workshops.
- **Part 12: the safety patterns** — what each guard stops, and why subtraction
  beats supervision.

## License

MIT. Use it, teach with it, fork it.

---

*Built and published by [VetTech Homefront](https://vettechhomefront.com), a
veteran-owned local-first AI business in Ohio.*
