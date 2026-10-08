"""Second pass: the film/jazz boundary inside the standalone-song bucket.

The first pass settled the question that affects the analysis, namely which
songs belong to `stage`. Searching the remainder found no further stage songs,
so the Broadway corpus and the held-out corpus are now stable. What it did find
is a set of songs introduced in motion pictures that had been sitting in
`tin_pan_alley`, which affects the by-tradition table and nothing else.

`sourced` means a lookup was done and the production is named below.
`knowledge` means a well-documented film credit not separately looked up here.
"""

CORRECTIONS = {
    # --- introduced in a motion picture, verified by lookup
    "At Last": ("film", "sourced",
        "written for Sun Valley Serenade, 1941; the vocal was cut and appeared "
        "in Orchestra Wives, 1942, sung by Ray Eberle"),
    "I Should Care": ("film", "sourced",
        "published 1944; first appeared in MGM's Thrill of a Romance"),
    "The Nearness Of You": ("film", "sourced",
        "featured in Paramount's Romance in the Dark, 1938. Sources disagree: "
        "one account has it written for an unproduced Paramount picture and "
        "republished in 1940. Labelled film on the produced-film appearance, "
        "but this one is genuinely contested"),

    # --- introduced in a motion picture, well-documented credits
    "Boulevard Of Broken Dreams": ("film", "knowledge", "Moulin Rouge, 1934"),
    "I Fall in Love Too Easily": ("film", "knowledge", "Anchors Aweigh, 1945"),
    "It Could Happen to You": ("film", "knowledge", "And the Angels Sing, 1944"),
    "There Will Never Be Another You": ("film", "knowledge", "Iceland, 1942"),
    "Two Sleepy People": ("film", "knowledge", "Thanks for the Memory, 1938"),
    "Just You, Just Me": ("film", "knowledge", "Marianne, 1929"),
    "How Little We Know": ("film", "knowledge", "To Have and Have Not, 1944"),
    "Do You Know What It Means To Miss New Orleans": ("film", "knowledge",
        "New Orleans, 1947"),
    "In love In Vain": ("film", "knowledge", "Centennial Summer, 1946"),
    "Close Enough For Love": ("film", "knowledge", "Agatha, 1979"),
    "Don't Misunderstand": ("film", "knowledge", "Shaft's Big Score, 1972"),

    # --- jazz instrumentals that acquired lyrics later, not published songs
    "Early Autumn": ("jazz", "sourced",
        "Ralph Burns's Summer Sequence for Woody Herman, 1946 to 1947; "
        "reworked as Early Autumn in 1949, Mercer lyrics added 1952"),
    "Don't Be That Way": ("jazz", "knowledge",
        "Edgar Sampson instrumental for Chick Webb, 1934; Parish lyrics later"),
}

# Checked and left where they were, so the work is not repeated.
CONFIRMED_UNCHANGED = {
    "A Sinner Kissed An Angel": "popular song, 1941; Harry James and Dorsey hits, no show or film",
    "A Weaver Of Dreams":       "popular song, 1951; first recorded Nat Cole, released Bing Crosby",
    "Please Don't Talk About Me When I'm Gone": "published 1930 as a popular song, no revue origin found",
    "Then I'll Be Tired of You": "1934, first recorded Freddy Martin; not from Revenge with Music",
    "Cinnamon and Clove":       "standalone, first recorded Sergio Mendes & Brasil '66, 1967",
}

# Not resolvable from available sources.
UNRESOLVED = {"Unless It's You", "Love Makes the Changes"}
