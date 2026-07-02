# Changelog

## v6.8.1 final typography patch for Figure 1

- Increased vertical separation between the `Source layer` title and the `restricted/withheld` body text in Figure 1.
- No data, table, claim or release-boundary content was changed.

## v6.8.1 figure-1 repair public-minimised release

- Rebuilt Figure 1 with additional right-side padding.
- Removed arrow labels that overlapped adjacent architecture panels.
- Replaced ambiguous status/legend squares with an explicit callout: examples of artefacts included in the public-minimised package.
- Added `figure_sources/figure1_public_outputs.csv` as a source file for the callout.
- Kept Figure 1 fully programmatic and non-generative. No AI image model was used.

## v6.8.1 figure-1 repair public-minimised

- Removed Python bytecode caches and cache folders.
- Regenerated manifest, dataset manifest and datapackage metadata.
- Replaced historical metadata with public v6.8.1 metadata and schemas.
- Added public JSON schema checks to the validator.
- Removed residual contextual/symptom labels from public tables.
- Recoded public session identifiers to S001-S052.
- Retained programmatic figure sources and non-generative figure provenance.
