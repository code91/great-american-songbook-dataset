"""Drop songs whose chart carries no lyric at all.

The corpus exists to study words against music at the syllable. A chart with no
words in it cannot contribute to that question: every word design requires a
syllable, so these songs reach none of them. What they do reach is the
music-only designs, which never ask for a syllable and so never notice that
there is nothing to sing.

Two songs qualify, both instrumental editions:

  Ask Me Again        162 notes, an unpublished Gershwin trunk song whose
                      chart carries the tune alone
  Don't Be That Way    88 notes, an Edgar Sampson instrumental for Chick Webb;
                      Parish wrote words later but not in this edition

Removing them is a decision on principle rather than on effect, and it is worth
recording which way the effect runs: the held-out replication of the surviving
design goes from z = -7.57 to -7.13, slightly WEAKER. A corpus assembled to
study text set to music should not contain songs with no text, whichever way
that moves a number.
"""
import csv

DROP = {"Ask Me Again", "Don't Be That Way"}

for path, key in (("dataset/manifest.csv", "song"), ("dataset/attachments.csv", "song")):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    keep = [r for r in rows if r[key] not in DROP]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(keep)
    print(f"{path}: {len(rows)} -> {len(keep)} rows ({len(rows)-len(keep)} dropped)")
