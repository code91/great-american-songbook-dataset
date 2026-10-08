
## A caution on the `category` column

`category` names where a song was first introduced, not what it sounds like and
not what era it belongs to. It was built in two passes and the `category_evidence`
column records how each label was established:

| evidence | meaning | n |
|---|---|---|
| `sourced` | a reference was looked up and names the production | 19 |
| `knowledge` | a well-documented credit, not separately looked up | 20 |
| `attributed` | our judgement from composer, date and title alone | 213 |
| `unresolved` | searched and not determinable | 2 |
| `none` | no composer credit and no findable origin | 9 |

Two cautions follow from that table. Most labels are still `attributed`, so a
study that leans on a fine distinction between `tin_pan_alley`, `film`, `jazz`
and `pop` should check the songs it depends on. The `stage` label is the
exception and is the one we worked hardest on, because it is the one that
partitions the corpus for analysis: every song now in `stage` has a documented
show credit, and the non-stage categories were searched for further show
origins until none were being found.

One distinction decides most of the hard cases. A song **used** in a film or
interpolated into a revue is not a song **introduced** there. Four songs were
originally misfiled on exactly that basis.

`tin_pan_alley` is the weakest label and the name oversells it. It means "a
published standalone song with no show or film origin we could find", not a
claim about the Tin Pan Alley era. Its median year is 1941, but it runs to 1974
and ten of its 64 songs postdate 1955: *Hallelujah I Love Him So*, *This Could
Be The Start Of Something Big*, *I Keep Going Back to Joe's*, *Nothing Ever
Changes*, *The Last Dance*, *Rules of the Road*, *Summer Wind*, *Cinnamon and
Clove*, *Unless It's You* and *The Moon Is Harsh Mistress*. Treat it as a
residual, and read any result broken down by it with that in mind.

`undetermined` exists so that songs with no provenance are excluded from
provenance claims rather than silently counted as Tin Pan Alley, which is what
happened in the first version of this dataset.

One known upstream error: the composer credit for *The Ruby and the Pearl* is
wrong in the source archive. It is Jay Livingston and Ray Evans, not Victor
Young. Others may be.
