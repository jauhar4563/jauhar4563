# Profile artwork

The README uses repository-hosted original SVGs for the header, project cards,
technology badges, and contribution cards. It intentionally uses no custom README
CSS. Each technology badge is a separate image so rows can wrap on small screens.
Project cards use a fixed 280px width and flow inline: multiple columns where space
allows, one column on phones. Avoid tables or percentage widths that shrink text.

## Editing

- Edit the introduction, project links, and experience text in `README.md`.
- Edit the original artwork and badge groups in `scripts/design.py`, then run
  `python scripts/design.py`. Keep README badge references and the `ICONS` mapping in sync when adding a
  technology. Icon sources and licenses are recorded in `assets/icons/`; badges
  embed the vendored SVGs, so rendering needs no external icon service. Listing a technology describes experience, not a proficiency score.
- Project summaries describe public personal repositories. Do not add company,
  customer, or private repository details.

## Daily activity refresh

The `Refresh profile artwork` workflow runs daily at 03:17 UTC (08:47 in India)
and can be run manually. Its initial implementation branch also triggers it on
source changes, so the workflow can be checked before merging.

The generator requests only dates and counts from the account-level contribution
calendar. It does not request repository details. It includes private activity only
to the extent GitHub exposes it to the workflow token. Do not add a personal or
company access token to increase its access.

The cards cover 365 UTC dates including today. The longest streak is restricted to
that window. A current streak can end today or yesterday; if both have no activity,
it is zero. Contributions and commits are different metrics. Unavailable PR,
commit, review, and comment counts are deliberately omitted.

Generation checks calendar completeness and compares the daily sum with GitHub's
reported total. Both cards and both snk animations must succeed before the separate
publish job commits anything. A failed refresh leaves the previous assets and
their period labels unchanged. The card refresh date is the final date in its
displayed period. Workflow failures are visible in the repository's Actions tab.

The generation job has read-only repository access. Only the publish job can write
the generated files. All external actions are pinned to commit SHAs. The workflow
pushes without force and fails on concurrent conflicting changes.

## Checks

```sh
python -m unittest discover -s tests -v
python scripts/design.py
git diff --check
```

Use GitHub's rendered README to check dark and light appearances, mobile wrapping,
all links, and animation loading. The external typing line and profile-hit badge
are decorative; the text introduction remains readable without them. Profile hits
are third-party image requests, not unique visitors or historical GitHub traffic.
