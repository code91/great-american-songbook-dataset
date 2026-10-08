"""Derive tonic and mode from the music where the stated key is implausible.

The mode in the manifest was inferred from the final chord symbol, and that
inference has a hole: `_tonic` in the reader skips a trailing dominant or
suspension when looking for a resting chord, testing for a quality that starts
with 7, 9, 11 or 13 or contains "sus", but a MINOR SEVENTH starts with "m". So a
chart that closes on a ii-V turnaround back to the top, ending on Cm7 under a Bb
tonic, has that Cm7 accepted as its resting chord and is read as minor. Twenty-
three charts end on a minor seventh.

The consequence is not cosmetic. `corpus.py` derives harmonic function from the
mode, so a song labelled minor when it is major has every chord's function
mislabelled, and harmonic function is what the paper's surviving design is
stated in.

The test uses the MELODY only, so it is independent of the chord symbols that
caused the problem. For each of the twelve key signatures, score the share of
duration-weighted melodic time spent on its seven pitch classes. Calibration
comes from the corpus itself: among the 154 songs whose stated signature already
matches the best-fitting one, the LOWEST score is .678, so a song scoring below
that against its own stated key is stated wrong. Nothing above the floor is
touched, which deliberately leaves alone the many one-accidental neighbours
where a secondary dominant makes an adjacent signature fit marginally better.

A key signature is shared by a major key and its relative minor, which have
identical pitch content, so the signature cannot choose between them. The tonic
is taken as whichever of the two roots carries more duration-weighted chord
mass, and the mode follows from that choice.
"""
import csv, collections, json, re

PC = {"C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,"F":5,"F#":6,"Gb":6,
      "G":7,"G#":8,"Ab":8,"A":9,"A#":10,"Bb":10,"B":11,"Cb":11}
NAMES = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
MAJ = [0,2,4,5,7,9,11]
SIG = {t: frozenset((t+i) % 12 for i in MAJ) for t in range(12)}
FLOOR = 0.678          # the lowest fit observed among keys that already agree

def norm(n): return (n or "").strip().replace("♭","b").replace("♯","#")
def sig_of(tonic, mode):
    return SIG[tonic if mode == "major" else (tonic + 3) % 12]

rows = list(csv.DictReader(open("dataset/attachments.csv", newline="", encoding="utf-8")))
mrows = list(csv.DictReader(open("dataset/manifest.csv", newline="", encoding="utf-8")))
meta = {m["song"]: m for m in mrows}
by = collections.defaultdict(list)
for r in rows: by[r["song"]].append(r)

def fit(rs, pcs):
    i = t = 0.0
    for r in rs:
        d = float(r["duration_q"]); t += d
        if int(r["midi"]) % 12 in pcs: i += d
    return i / t if t else 0.0

changes = {}
for song, rs in sorted(by.items()):
    m = meta.get(song)
    if not m: continue
    st = PC.get(norm(m["key"]))
    sf = fit(rs, sig_of(st, m["mode"])) if st is not None else 0.0
    if st is not None and sf >= FLOOR:
        continue                                      # plausible as stated
    bt, bf = max(((t, fit(rs, SIG[t])) for t in range(12)), key=lambda x: x[1])
    if bf - sf < 0.08:
        continue                                      # no clearly better option
    majt, mint = bt, (bt + 9) % 12

    # The signature is settled by the melody. It cannot settle major versus
    # relative minor, because those share their pitch content, so that choice is
    # made on chords that can BE a tonic. Raw chord mass will not do: ii and vi
    # are everywhere in this idiom and the relative minor wins on mass in tunes
    # nobody would call minor. A resting chord is a triad, a sixth, a major
    # seventh, a minor sixth or a minor-major seventh. A plain minor seventh is
    # excluded for exactly the reason it broke the original inference.
    #
    # The mode follows the evidence and not the arithmetic. Deciding mode from
    # which root the tiebreak landed on is what produced two wrong answers here,
    # flipping Porter's major-key patter song to F minor because the fitted
    # signature happened to be the one whose relative minor is F.
    REST_MAJ = re.compile(r"^(|6|maj7?|maj9|M7|6/9|2)$")
    REST_MIN = re.compile(r"^(m|m6|m\(maj7\)|mmaj|m6/9)$")

    def resting(root):
        """Duration on resting major and resting minor chords built on `root`."""
        a = b = 0.0
        for r in rs:
            if PC.get(norm(r["chord_root"])) != root: continue
            q = (r["chord_quality"] or "").strip(); d = float(r["duration_q"])
            if REST_MAJ.match(q): a += d
            if REST_MIN.match(q): b += d
        return a, b

    maj_rest, _ = resting(majt)          # major tonic wants a major resting chord
    _, min_rest = resting(mint)          # relative minor wants a minor one

    if maj_rest == 0 and min_rest == 0:
        # Neither candidate ever appears as a resting chord, so this song gives
        # no evidence for the choice. Keep whatever was stated rather than invent
        # a tonic: the signature may well be right, but we cannot say which of
        # its two tonics it is.
        continue

    tonic = majt if maj_rest >= min_rest else mint
    mode  = "major" if tonic == majt else "minor"

    # A key checked against an independent edition outranks this heuristic, so a
    # verified song keeps its tonic letter and is only corrected where the
    # resting chords on that very letter contradict its recorded mode.
    if m["key_verified"] == "yes":
        if st is None: continue
        a, b = resting(st)
        if a == 0 and b == 0: continue
        vmode = "major" if a >= b else "minor"
        if vmode == m["mode"]: continue
        changes[song] = dict(old_key=m["key"], old_mode=m["mode"],
                             new_key=NAMES[st], new_mode=vmode, tonic_pc=st,
                             stated_fit=round(sf,3), fitted_fit=round(bf,3),
                             note="verified letter kept; mode from resting chords")
        continue

    changes[song] = dict(old_key=m["key"], old_mode=m["mode"],
                         new_key=NAMES[tonic], new_mode=mode, tonic_pc=tonic,
                         stated_fit=round(sf,3), fitted_fit=round(bf,3),
                         note="")

print(f"{len(changes)} songs corrected (stated key scores below the {FLOOR} floor)\n")
print(f"{'song':38s} {'from':>10s} {'fit':>5s} {'to':>10s} {'fit':>5s}  what changed   cat")
print("-" * 96)
for s, c in sorted(changes.items(), key=lambda kv: kv[1]["stated_fit"]):
    same_letter = PC.get(norm(c["old_key"])) == c["tonic_pc"]
    what = "mode only" if same_letter else "TONIC + mode"
    print(f"{s[:36]:38s} {c['old_key']+' '+c['old_mode'][:3]:>10s} {c['stated_fit']:5.2f} "
          f"{c['new_key']+' '+c['new_mode'][:3]:>10s} {c['fitted_fit']:5.2f}  {what:13s}  {meta[s]['category']}")
n_mode = sum(1 for s,c in changes.items() if PC.get(norm(c["old_key"])) == c["tonic_pc"])
print(f"\nmode only : {n_mode}")
print(f"tonic too : {len(changes)-n_mode}")
print(f"of which in the Broadway set: {sum(1 for s in changes if meta[s]['category']=='stage')}")
json.dump(changes, open("/tmp/key_changes.json","w"), indent=1)

# ---------------------------------------------------------------- apply
# pc_rel_tonic and chord_root_rel are stored in attachments.csv, computed from
# the tonic at build time, so correcting the manifest alone would leave them
# stale. Both are pure arithmetic on columns that are already there (midi and
# chord_root are absolute), so they are recomputed here without re-reading any
# source. pc_rel_chord is (midi - chord_root) and does not involve the key.
import sys
if "--apply" not in sys.argv:
    print("\nnothing written. re-run with --apply to commit these.")
    raise SystemExit

for r in rows:
    c = changes.get(r["song"])
    if not c: continue
    t = c["tonic_pc"]
    r["pc_rel_tonic"] = str((int(r["midi"]) - t) % 12)
    cr = PC.get(norm(r["chord_root"]))
    r["chord_root_rel"] = "" if cr is None else str((cr - t) % 12)

for m in mrows:
    c = changes.get(m["song"])
    if not c: continue
    m["key"], m["mode"] = c["new_key"], c["new_mode"]
    # `music` is a third provenance alongside `yes` and `no`: not checked against
    # an edition, but derived from the notes rather than taken from a source field.
    m["key_verified"] = "music"

with open("dataset/attachments.csv","w",newline="",encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open("dataset/manifest.csv","w",newline="",encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(mrows[0].keys())); w.writeheader(); w.writerows(mrows)
print(f"\napplied to {len(changes)} songs; "
      f"{sum(1 for r in rows if r['song'] in changes)} event rows recomputed")
