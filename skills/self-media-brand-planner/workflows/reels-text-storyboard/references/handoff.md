# Text versions, selection and optional handoff

Use the existing Project record when one exists. Otherwise the candidate header and comparison index are enough for ordinary text review; do not create sidecars just to fill a schema.

Keep these meanings distinct:

- `candidate`: an unselected proposal.
- `selected_for_revision`: the user chose a direction; the revised wording still needs review.
- `draft`: current text awaiting review.
- `user_approved`: explicit approval exists for this exact text version.

Record the chosen candidate and actual selection/approval message when available. Do not infer either from a filename containing “final”, assistant recommendations, silence or the mere existence of three candidates. If provenance is unknown, say so rather than claiming the draft followed an A/B/C review.

For revisions, keep prior content recoverable without overwriting earlier backups. Preserve unchanged candidates. A content change returns the new text to draft. A format-only change may preserve approval only when unchanged semantic text is verified.

Only when the user requests downstream production, provide or update the existing handoff with:

- exact storyboard path and SHA-256; selected candidate and version;
- storyboard status and actual approval evidence, or null;
- audience, language, story pattern, spoken/visual style and its provenance;
- sources and claim limits; CTA and destination status;
- target duration, timing status (`estimated`, `user_accepted_preview_timing`, `scratch_read_verified`) and any actual timing evidence;
- scene ids/times, full narration, screen text, visual intent and asset gaps, or links to the complete scene table;
- downstream request and separate render/publish authorization state.

Accept an equivalent approved script with other filenames or no sidecar. Metadata must describe existing evidence, not create approval. A changed script makes earlier derived previews stale. For compatibility with an existing HTML consumer, preserve its `html_requested` field, true only with an explicit request for that version; this never starts production automatically.
