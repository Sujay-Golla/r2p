# R2P

Coursework, coding assignments, and capstone challenges for IBM Quantum Road to Practitioner Program.
<img width="1060" height="1060" alt="image" src="https://github.com/user-attachments/assets/d14a30da-09ac-43f4-9c55-059f193c6d7a" />


## Layout

- `Capstone Project/` — capstone challenges (QMOO, SKQD, Hadron–Schwinger), helpers, and environment files
- `Assignment 3/` — Unit 3 coding assignment
- `Lectures/` — unit slides
- Root notebooks — Units 1, 2, and 4 coding assignments plus workshop/lab notebooks

## Local setup

Use the Windows requirements file on this machine:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r "Capstone Project/requirements-windows.txt"
```

On other platforms, use `Capstone Project/requirements.txt`.

IBM Quantum API keys belong in local files only. Do not commit `apikey.json` or similar credential files — they are gitignored.

## Capstone notes

Open and run `Capstone Project/Guide_and_install.ipynb` first. For each challenge, keep the helper modules and data files alongside the notebook; the notebooks depend on them.
