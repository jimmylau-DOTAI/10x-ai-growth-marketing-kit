# Jimmy GitHub Profile Overview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Jimmy's GitHub Profile Overview with his supplied speaking photo and connect the public 10x Kit back to that profile.

**Architecture:** Create the special public repository `jimmylau-DOTAI/jimmylau-DOTAI` with one Profile README and one canonical photo asset. Then update the existing Kit README and repository description to match the public Jimmy IP positioning.

**Tech Stack:** GitHub Markdown/HTML, `gh`, `git`, `sips`, JPEG, repository-relative and public GitHub links.

## Global Constraints

- Use only Jimmy's accepted title and career path.
- Do not publish unapproved metrics, customer claims, contact details, or credentials.
- Use the supplied photo without generating or retouching Jimmy's appearance.
- Keep the profile repository public and the Kit repository public.
- Do not add a license.
- Do not change GitHub account metadata or avatar.

---

### Task 1: Create the public Profile repository and photo asset

**Files:**
- Create: `/Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile/assets/jimmy-lau-speaking.jpg`

**Interfaces:**
- Consumes: the supplied 1600×1156 PNG.
- Produces: a public special-profile repository checkout and a web-friendly canonical photo asset.

- [x] **Step 1: Create and clone the repository**

Run:

```bash
gh repo create jimmylau-DOTAI/jimmylau-DOTAI \
  --public \
  --description "Jimmy Lau — DotAI Co-Founder / CMO and AI Growth Builder"
gh repo clone jimmylau-DOTAI/jimmylau-DOTAI /Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile
git -C /Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile branch -M main
```

Expected: the remote exists, the local checkout exists, and the active branch is `main`.

- [x] **Step 2: Prepare the photo**

Run:

```bash
mkdir -p /Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile/assets
sips --resampleWidth 1400 \
  -s format jpeg \
  -s formatOptions 88 \
  /var/folders/w2/77qt0sns7f5b775m8btgkv_w0000gn/T/codex-clipboard-ce74cad7-f69d-4f7e-a22a-a6fa18eb1e04.png \
  --out /Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile/assets/jimmy-lau-speaking.jpg
```

Expected: a 1400-pixel-wide JPEG exists with the original aspect ratio.

### Task 2: Write and publish the Profile README

**Files:**
- Create: `/Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile/README.md`

**Interfaces:**
- Consumes: `assets/jimmy-lau-speaking.jpg` and the accepted Jimmy positioning.
- Produces: the public GitHub Overview shown on `https://github.com/jimmylau-DOTAI`.

- [x] **Step 1: Write the README**

Include:

1. centered hero image;
2. Jimmy's title and career path;
3. current 10x Kit project;
4. focus areas;
5. `Context → Evidence → Strategy → Production → Human Review`;
6. career-path explanation;
7. current direction;
8. direct project link.

- [x] **Step 2: Validate**

Check Markdown whitespace, image existence, relative links, required positioning, and absence of private paths, credentials, metrics, client claims, and contact PII.

- [x] **Step 3: Commit and push**

Run:

```bash
git -C /Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile add README.md assets/jimmy-lau-speaking.jpg
git -C /Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile commit -m "feat: add Jimmy GitHub profile overview"
git -C /Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile push -u origin main
```

### Task 3: Connect and correct the 10x Kit

**Files:**
- Modify: `README.md`
- Create: `docs/superpowers/specs/2026-07-30-jimmy-github-profile-design.md`
- Create: `docs/superpowers/plans/2026-07-30-jimmy-github-profile.md`

**Interfaces:**
- Consumes: the live public profile photo and profile URL.
- Produces: a Kit author card, accurate public state, and aligned repository description.

- [x] **Step 1: Update the Kit README**

Replace the private installation sentence and enhance `關於 Jimmy` with:

- the public canonical photo;
- accepted positioning;
- a link to `https://github.com/jimmylau-DOTAI`.

- [x] **Step 2: Update repository description**

Run:

```bash
gh repo edit jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --description "A growing AI marketing skill kit for everyone who wants to grow with AI."
```

- [x] **Step 3: Validate, commit, and push**

Validate README links, heading hierarchy, public state wording, photo URL, profile URL, and description. Then run:

```bash
git add README.md docs/superpowers/specs/2026-07-30-jimmy-github-profile-design.md docs/superpowers/plans/2026-07-30-jimmy-github-profile.md
git commit -m "docs: connect Jimmy profile to growth kit"
git push origin main
```

### Task 4: Verify live GitHub state

**Files:**
- Verify: both public repositories through GitHub.

**Interfaces:**
- Consumes: pushed commits and public GitHub metadata.
- Produces: evidence that the photo, Profile README, Kit README, and description are live.

- [x] **Step 1: Verify Profile repository**

Use GitHub API to confirm:

- public visibility;
- default branch `main`;
- live `README.md`;
- live `assets/jimmy-lau-speaking.jpg`.

- [x] **Step 2: Verify Kit repository**

Use GitHub API to confirm:

- the pushed Kit commit is current on `main`;
- the description matches the approved line;
- the README no longer calls the repository private;
- the Jimmy profile and photo links are present.

- [x] **Step 3: Confirm clean local repositories**

Run `git status --short` in both repositories. Expected: no output.
