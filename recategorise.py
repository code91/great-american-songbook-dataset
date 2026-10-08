"""Corrections to the category labels, from sources rather than from recall.

The original categories were my own attribution. Checking them turned up two
kinds of error, and the first is consequential: songs introduced in Broadway or
West End productions were sitting in the residual tin_pan_alley bucket, so the
stage corpus the analysis used was incomplete.

Each entry below carries how it was established. `sourced` means a lookup was
done and the reference is named. `knowledge` means a well-documented origin I
am confident of without a lookup. Nothing is marked sourced that was not
actually checked.

The lesson from the lookups is a distinction the first pass missed: a song USED
in a film or interpolated into a revue is not a song INTRODUCED there.
Baltimore Oriole, I Cover the Waterfront and A Hundred Years From Today were
all published first and added later, and all three were misfiled on that basis.
"""

# song -> (corrected category, evidence, note)
CORRECTIONS = {
    # --- introduced in a Broadway or West End production: these belong in `stage`
    "These Foolish Things": ("stage", "sourced",
        "Spread It Abroad, 1936; BBC revue then the Saville Theatre"),
    "You Better Go Now": ("stage", "sourced",
        "written for New Faces of 1936, Broadway; first sung by Katharyn Mayfield"),
    "Alone Together": ("stage", "knowledge", "Flying Colors, 1932 Broadway revue"),
    "Darn That Dream": ("stage", "knowledge", "Swingin' the Dream, 1939 Broadway"),
    "Here's That Rainy Day": ("stage", "knowledge", "Carnival in Flanders, 1953 Broadway"),
    "How Long Has": ("stage", "knowledge",
        "How Long Has This Been Going On?, Funny Face 1927 / Rosalie 1928"),
    "I May Be Wrong": ("stage", "knowledge",
        "John Murray Anderson's Almanac, 1929 Broadway revue"),
    "I'm All Smiles": ("stage", "knowledge", "The Yearling, 1965 Broadway"),
    "Guess I'll Hang My Tears Out to Dry": ("stage", "knowledge",
        "Glad To See You, 1944; closed in tryout before reaching Broadway"),
    "I'll Only Miss Her When I Think Of Her": ("stage", "knowledge",
        "Skyscraper, 1965 Broadway"),

    # --- introduced in a motion picture
    "You're My Thrill": ("film", "sourced", "Jimmy and Sally, 1933"),
    "Can't Get Out Of This Mood": ("film", "sourced",
        "written for Seven Days' Leave, 1942; introduced by Ginny Simms"),
    "The Ruby and the Pearl": ("film", "sourced",
        "Thunder in the East, Paramount 1952. NOTE the composer credit in the "
        "dataset is wrong: Jay Livingston and Ray Evans, not Victor Young"),

    # --- published first, only used or interpolated later: these stay tin_pan_alley
    "Baltimore Oriole": ("tin_pan_alley", "sourced",
        "published 1942; background music only in To Have and Have Not, 1944"),
    "I Cover the Waterfront": ("tin_pan_alley", "sourced",
        "standalone song after the novel; added to the 1933 film late, instrumental only"),
    "A Hundred Years From Today": ("tin_pan_alley", "sourced",
        "published 1933; interpolated into Blackbirds of 1934 afterwards"),
    "Ask Me Again": ("tin_pan_alley", "sourced",
        "unpublished Gershwin trunk song, c.1930; rediscovered 1983"),

    # --- a theatrical origin that is not Broadway or the West End
    "Gypsy In My Soul": ("stage_other", "sourced",
        "written for the 1937 University of Pennsylvania Mask and Wig show"),
}

# songs with no composer credit in the archive and no determinable origin
UNDETERMINED = {
    "Can't Take You Nowhere", "Don't Look Back", "Harold's House of Jazz",
    "Our Love Rolls On", "Reflections", "What Are You Afraid Of",
    "Wheelers and Dealers", "You Can't Rush Spring", "Zanzibar",
}
