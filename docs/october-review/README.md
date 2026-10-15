# October 13 specification implementation

Source: Jason_Shapiro_Website_Revision_Specifications.docx.md, supplied by Justin. Implementation date: October 15, 2026.

Baseline: 36c6f06cf34cf191f6ac527af17b08f5b8a792fd on codex/implement-approved-copy-stepwise.

The new codex/jason-october-revisions branch is a separate preview. Neither the prior preview branch nor main is updated. No changes to the firm's production website.

## Scope

- English homepage: all actionable items in sections 01 through 09.
- All existing pages: shared header and footer design and corrections, including translated footer labels on Spanish pages.
- English pages: shared consultation copy.
- Existing English attorney biographies and book description: corresponding requested corrections.
- New dedicated Jason Shapiro and Ernest Buonocore profile URLs use existing approved biography material with the explicit October updates. No unprovided credentials or biographical facts were invented.
- Five existing licensed practice photographs reused; credits remain in images/IMAGE-CREDITS.md.
- Photography, courthouse overlay and complete results page outcomes remain unchanged.

## Pending and limitations

1. Jason must supply the real back-cover photograph with spine. Justin confirmed on October 15 that it is not available. The current front-cover mockup remains on the right of the book section. No fabricated back cover.
2. Jason must provide revised copy for the three homepage featured-case cards. Existing descriptions are interim; Jury Verdict wording was removed as specifically requested.
3. Other page feedback is pending. Spanish main copy is not newly translated as part of this English specification.
4. The Zoom-meeting question is recorded but no scheduling action was requested or performed.
5. Contact forms remain preview-only. WhatsApp account ownership is not newly verified by this visual pass.

## Evidence

- Before screenshots: captured directly from the existing Cloudflare preview, desktop 1440 and mobile 390 pixels, before implementation.
- After screenshots: captured from the revised code using the same viewport sizes.
- The comparison page offers full homepage, ten major sections, attorneys and contact page comparisons.
- New profile pages are shown as new pages rather than fabricated before images.
- Exact supplied copy and punctuation are preserved in replacement passages. Existing interior and result copy is otherwise preserved except the shared blocks listed above.

## Reproduction

1. Run python3 scripts/october-revisions.py after source generation, or run scripts/refine-design.py which invokes it last.
2. Run python3 scripts/verify-october.py and python3 scripts/verify-september.py.
3. Serve the repository on port 8135.
4. Run node scripts/check-october.mjs after and node scripts/check-october-interactions.mjs.

The migration is idempotent. Older September screenshot tests describe their original baseline, while the October acceptance checks cover the new approved copy exceptions.
