# The Domain Language

This document captures the domain language of the NLP subdomain I'm working with.

When extracting the Morphology from a word in spaCy, we get a MorphAnalysis.
A MorphAnalysis contains a set of Universal Features not covered by the universal Part-of-Speech tags.

A _Feature_ is a property of a word, such as its Gender, its Case or its Number.
Each feature can have an arbitrary amount of _feature instances_,
such as the Nominative for the Case or the Plural for the Number.

From the MorphAnalysis, features come in an _abbreviated_ form, such as "Case=Nom|Gender=Masc|Number=Sing".
There is functionality for converting them to their _legible_ form, such as "Nominative Singular Masculine".

