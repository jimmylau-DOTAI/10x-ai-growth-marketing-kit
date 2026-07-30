# Jimmy GitHub Profile Overview Design

**Date:** 2026-07-30

## Objective

Create a public GitHub Profile Overview for `jimmylau-DOTAI` that introduces Jimmy's practitioner identity, shows the 10x AI Growth Marketing Kit as a current project, and uses Jimmy's supplied speaking photo as the main visual.

Also connect the existing 10x Kit README back to Jimmy's profile and correct its outdated statement that the public repository is private.

## Verified Current State

- `jimmylau-DOTAI` is a GitHub user account.
- The public profile currently has no name, bio, website, company, or Profile README.
- `jimmylau-DOTAI/jimmylau-DOTAI` does not exist.
- `jimmylau-DOTAI/10x-ai-growth-marketing-kit` is currently public.
- The Kit README still describes the repository as a private team test.
- The supplied photo is a 1600×1156 PNG showing Jimmy speaking at a lectern.

## Reference Use

Raymond Hou's GitHub profile is used only as a structural reference:

- one clear hero visual;
- two-line personal positioning;
- current work and projects;
- an easy-to-scan personal journey;
- links that lead visitors to real work.

Do not copy Raymond's wording, milestones, product structure, social links, badges, or visual assets.

## Public Positioning

Use only these accepted claims:

- Jimmy Lau;
- DotAI Co-Founder / CMO;
- `Designer → Marketer → Growth Marketer → AI Growth Builder`;
- works across research, content, campaigns, growth systems, AI adoption, and practical implementation;
- creator of the 10x AI Growth Marketing Kit.

Do not publish experience years, enterprise counts, learner counts, client names, testimonials, partner names, or results in this version.

## Repository Architecture

Create the public special-profile repository:

```text
jimmylau-DOTAI/jimmylau-DOTAI
├── README.md
└── assets/
    └── jimmy-lau-speaking.jpg
```

Local checkout:

```text
/Users/jimmylau/Documents/Git-Jimmy/jimmylau-DOTAI-profile
```

## Photo Treatment

- Use the exact supplied photo.
- Do not generate, retouch, replace, or alter Jimmy's appearance.
- Convert the PNG to a web-friendly JPEG.
- Resize to a maximum width of 1400 pixels.
- Keep the original aspect ratio.
- Save as `assets/jimmy-lau-speaking.jpg`.
- Display centered at approximately 72% width with descriptive alt text.

## Profile README Structure

### 1. Hero

Centered speaking photo.

### 2. Personal positioning

Opening:

```text
我係 Jimmy Lau，DotAI Co-Founder／CMO。
Designer → Marketer → Growth Marketer → AI Growth Builder。
```

Supporting idea:

Jimmy turns marketing judgment across research, strategy, content, campaigns, and growth into workflows that AI can execute, people can understand, and teams can improve.

### 3. What Jimmy is building

Feature the 10x AI Growth Marketing Kit:

- a growing AI Marketing Skill Kit for anyone who wants to grow with AI;
- four implemented Skills are the starting point;
- future Skills are added only when they solve real work and can be tested;
- direct link to the public repository.

### 4. Areas of focus

Use a concise list:

- AI Marketing Skills and workflows;
- Company Brain and reusable context;
- content research and source discipline;
- Full Funnel campaign planning;
- SEO/GEO and platform-native content;
- AI education and practical adoption.

### 5. Working model

Show:

```text
Context → Evidence → Strategy → Production → Human Review
```

Explain that AI accelerates work while humans own facts, judgment, brand position, and publication.

### 6. Career path

Show the accepted path only:

```text
Designer → Marketer → Growth Marketer → AI Growth Builder
```

Describe the progression without adding dates, numbers, or unverified achievements.

### 7. Current direction

Explain that Jimmy is continuing to turn real marketing work into reusable Skills and teaching non-technical marketers to modify workflows into their own versions.

### 8. Project link

End with a direct link to the 10x AI Growth Marketing Kit. Do not add unverified website, email, or social links.

## 10x Kit README Changes

### Public state

Replace the inaccurate private-repository installation sentence with:

- the repository is public;
- the package remains `v0.1-team-test`;
- people can clone and test it;
- public visibility does not grant redistribution rights without a selected license.

### Jimmy author card

Update the existing `關於 Jimmy` section:

- display the canonical profile photo from the public profile repository;
- retain accepted title and career path;
- connect Jimmy's work to the Skill-builder teaching goal;
- add a direct link to `https://github.com/jimmylau-DOTAI`.

### Repository description

Update the GitHub description to:

```text
A growing AI marketing skill kit for everyone who wants to grow with AI.
```

## Safety and Publishing Rules

- Creating `jimmylau-DOTAI/jimmylau-DOTAI` is an explicitly approved public action.
- The photo is explicitly supplied by Jimmy for upload.
- Do not update GitHub avatar, account name, bio, company, location, website, or email.
- Do not add a license to either repository.
- Do not change the 10x Kit's visibility.
- Do not publish performance claims.
- Verify the Profile README and image through the live GitHub API after push.
- Verify the 10x Kit README and repository description after push.

## Acceptance Checks

1. The public special-profile repository exists under the exact username.
2. Its default branch is `main`.
3. `README.md` and `assets/jimmy-lau-speaking.jpg` are present.
4. GitHub renders the profile README from the public repository.
5. The image is no wider than 1400 pixels and retains the supplied photo content.
6. The profile includes Jimmy's accepted title, path, project, focus, and working model.
7. The profile contains no unapproved metrics, client claims, contact details, or credentials.
8. The 10x Kit README links back to Jimmy's GitHub profile and shows his photo.
9. The 10x Kit no longer claims the repository is private.
10. The public repository description matches the broader audience positioning.
11. Both local repositories are clean after commits and pushes.
