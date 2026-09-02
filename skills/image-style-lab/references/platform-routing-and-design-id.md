# Platform routing and Design ID

Use this stage when the user wants the Style placed in the correct content platform, asks for a Design ID, or wants one portable Style adapted across formats.

## Ownership boundary

Image Style Lab owns the evidence-backed Style pack and platform adaptation proposal. The active Vault／brand-system owner controls the canonical index and final write. Runtime should route to that capability when available; otherwise stop with a validated dry-run receipt. Never treat a request to analyse images as permission to modify a Vault.

## Discover the destination

Before proposing a path:

1. Read the user-chosen Vault root rules and nearest platform／format index.
2. Resolve the exact Style selector, shared Design System, reference-image area and Design ID namespace.
3. Duplicate-check existing Style IDs, Design IDs and equivalent visual grammar.
4. Record the evidence in `PLATFORM-ROUTE.md`; do not hard-code a private Vault path into this public Skill.

If the Vault has no discoverable platform contract, stop `PLATFORM_CONTRACT_CONFLICT` and ask for the destination or an approved contract. Do not invent folders because a platform name sounds familiar.

## Portable master versus platform adaptation

The portable master uses:

```yaml
design_id: unassigned
platform_scope: portable
```

A destination candidate receives a new Design ID and scope in both `STYLE.md` and `DESIGN.md`, for example:

```yaml
design_id: IG-C-011
platform_scope: instagram-carousel
```

Cross-platform reuse borrows only abstract mechanisms. Refit canvas、reading behaviour／rhythm、typography、safe areas、Logo、CTA、accessibility、proof modality and medium constraints. Never reuse another platform's Design ID or copy its operational `STYLE.md`／`DESIGN.md` unchanged.

## Required platform route receipt

Create `styles/<style-id>/PLATFORM-ROUTE.md` from the template and record:

- target platform、format and primary job;
- exact selector／Style index and shared Design System inspected;
- Design ID namespace、existing IDs checked and proposed free ID;
- destination-ready `STYLE.md` and `DESIGN.md` paths;
- the distinct reference／visual-assets destination;
- every image source、rights、hash and destination;
- dry-run diff and Human Review decision.

Validate it with:

```bash
python3 scripts/validate_platform_route.py <experiment> <experiment>/styles/<style-id>/PLATFORM-ROUTE.md
```

Validation proves receipt consistency only. It does not write, register or publish anything.

## Reference-image filing

- Workbench／portable pack: keep 1–6 permitted anchors in `assets/reference-images/` and embed them in `REFERENCE.md` with relative paths.
- Managed platform Vault: copy approved evidence into the Vault's discovered reference／visual-assets area, then link it from the platform `REFERENCE.md`.
- Keep source URL／path, rights status, SHA-256, evidence role, mechanism and exclusions together.
- Do not replace the actual permitted images with URLs only. If copying is not permitted, keep an explicit external-reference receipt and do not claim portability.

The platform Style destination must receive `REFERENCE.md`、`STYLE.md` and `DESIGN.md`. If its current filing contract would omit `DESIGN.md`, return `PLATFORM_CONTRACT_CONFLICT`; the user must approve the contract change before registration.

## Approval gate

Default state is `PLATFORM_ROUTE_REVIEW_STOP` with `registration_authorized: false`. Show the exact proposed Design ID, Style destination, reference destination and files. Only the user's explicit approval of that route allows the active Vault owner to register it and change the receipt to `PLATFORM_ROUTE_APPROVED`.
