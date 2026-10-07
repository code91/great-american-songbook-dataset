# Great American Songbook dataset

Lyrics aligned to notated melody, at the syllable, across the Great American
Songbook: Broadway and Hollywood, Tin Pan Alley, and the jazz repertoire that
grew out of them.

Each row is one note, carrying the syllable sung on it, the chord sounding at
its onset, its pitch and its duration, in absolute terms and in key-invariant
ones. Chord corpora are plentiful and lyric corpora are plentiful; lyrics
aligned to *notated* melody at the syllable are not.

```
song,category,bar,midi,pitch_name,note_type,duration_q,syllable,melisma,chord_root,chord_quality,pc_rel_tonic,chord_root_rel,pc_rel_chord
Night and Day,stage,2,69,A4,quarter,1.0,"beat,",False,D,dim,7,1,6
```

| | |
|---|---|
| songs | **263** |
| note events | **36,595** |
| syllable-to-note attachment points | **29,766** |

Transcribed from engraved editions. The source scores are not redistributed
here.

## The unit of analysis

The atom is the **syllable-to-note attachment point**, with the chord sounding
at onset, not the word.

In sung music one word routinely spans several notes and crosses a chord
change: *love* held four beats through a ii-V. Collapsing that to a single
"word" makes every downstream result an artefact of how multi-note words were
merged. So every note is its own row, and a word held over *k* notes appears
as one attachment plus *k*-1 melisma continuations, flagged in `melisma`
rather than collapsed. Collapsing is a downstream choice and is left
downstream.

## Keys are singer keys, not published keys

Most of this comes from an archive that publishes every song in two keys, one
for a man and one for a woman, described by its own documentation as the
Sinatra or Bennett key and the Ella key. **These are deliberately transposed
vocal editions and are not the published key of the song.**

Use the key-invariant columns, `pc_rel_tonic`, `chord_root_rel` and
`pc_rel_chord`, for anything that must not depend on key. The absolute columns
are kept so the two can be compared and so nothing rests on the key being
right.

**`key_verified`** marks the 24 songs whose key was checked against an
independent edition; they come from a separately curated Cole Porter corpus.
Where a song arrived from both sources, the verified-key version was kept.

## How faithfully it reads

**Not optical music recognition.** The sources are vector output from
engraving software: staff lines are stroked segments with exact coordinates,
every notehead is a glyph with an exact origin, and lyrics and chord symbols
are already text. Nothing is recognised from pixels. Alignment is x-proximity
in a single coordinate space.

Rhythm is the only *inferred* quantity, and it is checked against the one
constraint notation guarantees: **the durations in a measure must sum to the
time signature**. Across 555 encoded charts, **93.9% of 21,490 bars are
length-exact**, and no chart with a music font in it failed to read. The 71
that produced nothing have no music font at all: they are lyric sheets and
song lists, not scores.

### The twin check

Most songs here exist in two singer keys. That is the same song twice, so bars,
note events and syllable counts must agree. Across **241 twin groups**:

| | agree |
|---|---:|
| bars | **99.6%** |
| note events | **97.9%** |
| syllables | 48.1% |

The music reads well. The lyric layer is the weak part, and the twin check is
how you can see it: `twin_syllable_gap` in `manifest.csv` records, per song,
how far the two editions disagreed on syllable count.

In aggregate the disagreement is small: **1.4% of all syllables**, with 78% of
twin groups within 2 and 90% within 5. A handful are badly wrong, and those
are charts printing two stanzas where the reader took a different line in each
edition. Filter on `twin_syllable_gap` if your work depends on the words.

## Columns

**Identity**: `song`, `category`, `year`, `composer`, `lyricist`, `show`, `bar`

**Pitch**: `midi`, `pitch_name`, `dia` (diatonic index, C4 = 0), `alter`

**Rhythm**: `note_type`, `dots`, `tuplet`, `duration_q` (quarter notes, dots
and tuplets applied)

**Words**: `syllable` (empty on a melisma continuation), `word_start`,
`hyphen_after`, `melisma`

**Harmony**: `chord_raw` (as printed), `chord_root`, `chord_quality`

**Key-invariant**: `pc_rel_tonic`, `chord_root_rel`, `pc_rel_chord`

## Files

| | |
|---|---|
| `dataset/attachments.csv` | one row per note event, all songs |
| `dataset/manifest.csv` | per song: key, mode, bars, counts, twin gap |

## Categories

Every song carries a `category`, so the corpus can be filtered to one
tradition. Filtering to `stage` gives a Broadway-only dataset of 69 songs and
8,564 attachment points.

| category | songs | attachments | what it is |
|---|---:|---:|---|
| `tin_pan_alley` | 103 | 11,181 | a published popular song belonging to no show |
| `stage` | 69 | 8,564 | a Broadway or West End musical or revue |
| `film` | 51 | 5,580 | written for a picture |
| `jazz` | 18 | 1,749 | the jazz tradition, including instrumentals that got words later |
| `pop` | 17 | 1,930 | the 1960s onward |
| `bossa` | 5 | 762 | Brazilian, and the chanson that travelled with it |

Nineteen songs carry a `show` from the archive's own index. Everything else,
the categories included, is attribution from general knowledge of the
repertoire: a judgement, not a citation. The well-known entries are not in
doubt; the obscure corners should be checked before anything rests on them,
and the boundary between `tin_pan_alley` and `film` is the softest of all,
since a popular song and a picture often arrived together.

## Composer, lyricist and year

**252 of 263 songs carry both credits and 252 carry a year.** Where
words and music are by one person, both fields hold that name.

The collaborations, which is what the corpus is for:

| composer | lyricist | songs | attachments |
|---|---|---:|---:|
| Richard Rodgers | Lorenz Hart | 14 | 1,555 |
| George Gershwin | Ira Gershwin | 10 | 1,364 |
| Harold Arlen | Johnny Mercer | 7 | 761 |
| Harry Warren | Mack Gordon | 7 | 628 |
| Jimmy Van Heusen | Johnny Burke | 7 | 672 |
| Michel Legrand | Marilyn and Alan Bergman | 7 | 986 |
| Jimmy Van Heusen | Sammy Cahn | 6 | 712 |
| Burt Bacharach | Hal David | 3 | 375 |
| Johnny Mandel | Marilyn and Alan Bergman | 3 | 363 |
| Jerome Kern | Dorothy Fields | 2 | 207 |

And the within-composer contrast, a composer holding still while the lyricist
changes:

| composer | lyricists |
|---|---|
| Duke Ellington | 9: Bob Russell, Carl Sigman, Don George, Johnny Hodges, Eddie DeLange, Irving M |
| Jerome Kern | 7: Buddy DeSylva, Dorothy Fields, Dorothy Fields, Oscar Hammerstein II, Ira Ger |
| Hoagy Carmichael | 7: Frank Loesser, Hoagy Carmichael, Johnny Mercer, Ned Washington, Paul Francis |
| Victor Young | 4: Jack Elliott, Jay Livingston, Ray Evans, Joe Young, Ned Washington, Sam M. L |
| Harold Arlen | 4: Johnny Mercer, Ted Koehler, Truman Capote, Yip Harburg |
| Jimmy Van Heusen | 4: Carl Sigman, Eddie DeLange, Johnny Burke, Sammy Cahn |
| Johnny Mandel | 4: Johnny Mercer, Marilyn and Alan Bergman, Paul Williams, Peggy Lee |
| Harry Warren | 3: Al Dubin, Arthur Freed, Mack Gordon |

Ten songs have no credit at all. They are obscure enough that the archive may
have written them itself.

## Keys are singer keys, not published keys

Most of this comes from an archive that publishes every song in two keys, one
for a man and one for a woman, described by its own documentation as the
Sinatra or Bennett key and the Ella key. **These are deliberately transposed
vocal editions and are not the published key of the song.**

Use the key-invariant columns, `pc_rel_tonic`, `chord_root_rel` and
`pc_rel_chord`, for anything that must not depend on key. The absolute columns
are kept so the two can be compared and so nothing rests on the key being
right.

**`key_verified`** marks the 24 songs whose key was checked against an
independent edition; they come from a separately curated Cole Porter corpus.
Where a song arrived from both sources, the verified-key version was kept.

## How faithfully it reads

**Not optical music recognition.** The sources are vector output from
engraving software: staff lines are stroked segments with exact coordinates,
every notehead is a glyph with an exact origin, and lyrics and chord symbols
are already text. Nothing is recognised from pixels. Alignment is x-proximity
in a single coordinate space.

Rhythm is the only *inferred* quantity, and it is checked against the one
constraint notation guarantees: **the durations in a measure must sum to the
time signature**. Across 555 encoded charts, **93.9% of 21,490 bars are
length-exact**, and no chart with a music font in it failed to read. The 71
that produced nothing have no music font at all: they are lyric sheets and
song lists, not scores.

### The twin check

Most songs here exist in two singer keys. That is the same song twice, so bars,
note events and syllable counts must agree. Across **241 twin groups**:

| | agree |
|---|---:|
| bars | **99.6%** |
| note events | **97.9%** |
| syllables | 48.1% |

The music reads well. The lyric layer is the weak part, and the twin check is
how you can see it: `twin_syllable_gap` in `manifest.csv` records, per song,
how far the two editions disagreed on syllable count.

In aggregate the disagreement is small: **1.4% of all syllables**, with 78% of
twin groups within 2 and 90% within 5. A handful are badly wrong, and those
are charts printing two stanzas where the reader took a different line in each
edition. Filter on `twin_syllable_gap` if your work depends on the words.

## Columns

**Identity**: `song`, `category`, `year`, `composer`, `lyricist`, `show`, `bar`

**Pitch**: `midi`, `pitch_name`, `dia` (diatonic index, C4 = 0), `alter`

**Rhythm**: `note_type`, `dots`, `tuplet`, `duration_q` (quarter notes, dots
and tuplets applied)

**Words**: `syllable` (empty on a melisma continuation), `word_start`,
`hyphen_after`, `melisma`

**Harmony**: `chord_raw` (as printed), `chord_root`, `chord_quality`

**Key-invariant**: `pc_rel_tonic`, `chord_root_rel`, `pc_rel_chord`

## Files

| | |
|---|---|
| `dataset/attachments.csv` | one row per note event, all songs |
| `dataset/manifest.csv` | per song: key, mode, bars, counts, twin gap |

## Categories

Every song carries a `category`, so the corpus can be filtered to one
tradition. Filtering to `stage` gives a Broadway-only dataset of 69 songs and
8,564 attachment points.

| category | songs | attachments | what it is |
|---|---:|---:|---|
| `tin_pan_alley` | 103 | 11,181 | a published popular song belonging to no show |
| `stage` | 69 | 8,564 | a Broadway or West End musical or revue |
| `film` | 51 | 5,580 | written for a picture |
| `jazz` | 18 | 1,749 | the jazz tradition, including instrumentals that got words later |
| `pop` | 17 | 1,930 | the 1960s onward |
| `bossa` | 5 | 762 | Brazilian, and the chanson that travelled with it |

Nineteen songs carry a `show` from the archive's own index. Everything else,
the categories included, is attribution from general knowledge of the
repertoire: a judgement, not a citation. The well-known entries are not in
doubt; the obscure corners should be checked before anything rests on them,
and the boundary between `tin_pan_alley` and `film` is the softest of all,
since a popular song and a picture often arrived together.

## Composer and lyricist

`composer` and `lyricist` are filled in where the source archive documents
them: a table of Arlen songs against their lyricists, a Rodgers and Hart song
list, and collections named after a songwriting pair. **56 of 234 songs carry both credits, 54 carry one.**

What is there is enough to see the crossed design that motivates this corpus,
a composer holding still while the lyricist changes:

| composer | lyricist | songs | attachments |
|---|---|---:|---:|
| Cole Porter | Cole Porter | 24 | 3,042 |
| Richard Rodgers | Lorenz Hart | 12 | 1,280 |
| George Gershwin | Ira Gershwin | 9 | 1,144 |
| Harold Arlen | Johnny Mercer | 6 | 639 |
| Harold Arlen | Truman Capote | 2 | 333 |
| Harold Arlen | Ted Koehler | 2 | 230 |
| Harold Arlen | Yip Harburg | 1 | 124 |

Arlen across four lyricists is the one real within-composer contrast here, and
it is thin. Rodgers with Hammerstein, which would be the other half of the
best instrument, is not in the archive at all.

The remaining 124 songs have no credit. They are standards whose attribution
is a lookup by title, and filling them in is a worthwhile job that has not
been done rather than an impossible one.

## Known limitations

- **Chord symbols are kept exactly as printed**, so one harmony appears under
  several spellings. Normalising is left to the user; a worked taxonomy is in
  the companion analysis repository.
- **Verse 2 is not captured.** Where a chart prints a second stanza under the
  first, only the first is read. This is also the main source of the large
  twin-gap outliers.
- **Section boundaries are not marked.** Verse and chorus often differ in
  mode, and the key is song-level.
- A word engraved with no space glyph before the next comes through joined.
  The space is absent from the file, not dropped in reading.

## Licence

The MIT licence covers any code here. It does not and cannot grant rights in
these songs, most of which remain in copyright. These rows are published as
research data, counts, features and alignments for text and data mining, and
are not a substitute for the works. If you hold rights in this material and
want something removed, open an issue and it will be taken down.
