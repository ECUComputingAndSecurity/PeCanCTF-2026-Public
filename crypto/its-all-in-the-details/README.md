### Writeup

This challenge consists of three email artefacts provided as .txt files. Each email contains embedded information that forms part of a broader narrative describing an attempted attack plan.

Participants are expected to analyse each email using progressively more advanced techniques, ranging from simple pattern recognition to basic digital forensics and encoding analysis.

### The first email is designed as an introductory step to establish the core concept of hidden information within natural language text.

Participants can extract the solution by taking the first letter of each sentence, which resolves cleanly to:

PERTH

This stage is intended to ensure familiarity with the format and encourage attention to structural patterns in otherwise normal prose.

### The second email introduces deliberate misdirection.

At first glance, the text appears natural and unremarkable. However, closer inspection reveals two embedded signals:

Certain letters within words are randomly capitalised, for example:

Half the books we read seem to enD up being set there for some reason

Participants familiar with CTF conventions may attempt to concatenate these anomalous capital letters. This leads to a deliberate red herring message:

DIDYOUTHINKITWOULDBETHATEASY

This path is intentionally misleading.

The actual solution is encoded via intentional spelling errors dispersed throughout the text.

Each error contains a single incorrect or substituted character. Extracting these anomalous characters in order yields:

BUNNINGSWAREHOUSE (which obviously would be separated as **bunnings_warehouse** for the flag)

This stage reinforces the importance of distinguishing signal from noise in layered encodings.

### The third emails contains 2 clues.

The first being that the text repeatedly mentions paying attention to something that could be easily overlooked. In this case that is the following section:

```text
AUSTRALIAN REGIONAL FOOD ARCHIVE — DIGITISATION RECORD
Recipe ID: LMB-SC-0044
Archive region: Joondalup
File last updated: 18/01/2026
Source collection digitisation batch ref: 535550504C595F434841494E
Scan quality: good, original handwritten card, minor foxing on edges
Original held: Rosa family collection
```

You may or may not notice that there is something suspicious about that batch reference number. It is hex, and decodes to `SUPPLY_CHAIN`.

That reveals that the attack will be a **supply_chain** attack.

Lastly every single email had some additional information attached in the form of system tags, but only one contains the actual date-encoding numbers (11, 11, 20, 26) so the solver has to identify which message is relevant.

```flag
pecan{perth_bunnings_warehouse_supply_chain_11112026}
```
