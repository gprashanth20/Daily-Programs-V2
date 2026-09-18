# Daily Java Check-in

Automatically commits 2 Java programs a day to this repo using GitHub Actions.
No personal credentials are ever needed - the workflow uses GitHub's own
built-in `GITHUB_TOKEN`, scoped only to this repo, auto-issued for each run.

## What's in here

```
.github/workflows/daily-java.yml   # the schedule + commit logic
scripts/generate_daily.py           # picks 2 topics, writes the .java files
queue.json                          # your topic backlog (edit anytime)
history.json                        # auto-updated log of what's been done
programs/                           # where generated .java files land, by category
```

## One-time setup (5 minutes)

1. Copy this whole folder's contents into the root of your GitHub repo
   (or into a subfolder - just keep the relative structure of
   `.github/workflows/`, `scripts/`, `queue.json`, `history.json` together).
2. Push it once, normally, from your own machine with your own git login -
   this is the only manual push you'll need.
3. On GitHub: go to **Settings → Actions → General → Workflow permissions**
   and make sure **"Read and write permissions"** is selected. Without this,
   the workflow can generate files but won't be able to push the commit.
4. That's it. The workflow runs daily at the time set in the cron line
   (default 9:00 AM IST - edit `.github/workflows/daily-java.yml` to change it).

## Adding your own program list

Open `queue.json` and add entries anywhere in the `queue` array:

```json
{ "title": "Your Program Name", "category": "Whatever Label You Want", "notes": "optional context" }
```

- `title` becomes the Java class name (spaces stripped, each word capitalized).
- `category` becomes the subfolder under `programs/`.
- Entries are consumed **top to bottom**, 2 per run. Put anything urgent at the top.

A starter list of ~44 topics (DSA, design patterns, concurrency, Core Java,
Java 21 features) is already loaded so the queue doesn't run dry while you
add your own.

## Testing it without waiting for the schedule

- Go to the **Actions** tab on GitHub → **Daily Java Check-in** → **Run workflow**.
  This uses the `workflow_dispatch` trigger already wired into the YAML.
- Or run it locally: `python3 scripts/generate_daily.py`, then check the
  `programs/` folder and commit/push yourself to see exactly what it produces
  before trusting it to run unattended.

## What happens when the queue runs out

The script prints a note and simply does nothing that day (no error, no
empty commit). Add more topics to `queue.json` whenever you like - no need
to touch the workflow file again.

## Notes

- Known algorithms (binary search, bubble/merge/quick/heap sort, fibonacci,
  two sum, singleton, stack-using-array, linked-list reversal) generate as
  full, runnable implementations - not stubs.
- Anything else generates as a clean scaffold with a `TODO` marker, so it
  compiles immediately and you can fill in the real logic whenever you get
  to it, without losing the day's check-in.
- If you want more topics turned into full implementations rather than
  scaffolds, tell me which ones and I'll add them to
  `scripts/generate_daily.py`.
