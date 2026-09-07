# Redactions

This archive aims to preserve cited sources in their original form. Every deviation
from the byte-for-byte capture is recorded here.

## fn23_cms_health_tech_pledge.html

- **Line 750** — the value of `"mapboxToken"` in the page's inline Drupal settings JSON
  was replaced with `REDACTED-BY-ARCHIVER-cms-public-mapbox-token`.
- **Why:** GitHub push protection flags the string as a Mapbox access token. It is a
  *publishable* (`pk.`) token belonging to CMS and served to every visitor of the live
  page, not a secret — but there is no archival reason to rehost another organization's
  credential.
- **Effect on the citation:** none. The token drives an unrelated map widget in the page
  chrome; the pledge text being cited is unaffected.

## Excluded from this repository

`archive/paywalled_screenshots/` is gitignored. Those captures are paywalled,
copyrighted articles retained locally for research use and not redistributable.
The open-access and public-domain material in this archive is complete.
