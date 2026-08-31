# Vercel Preview and Release

## Detect before changing

Read current project evidence：

- framework and package manager；
- build／install／output settings；
- `.vercel/project.json` when present；
- current Git remote／branch without modifying it；
- Vercel CLI／connector availability and authenticated account metadata；
- environment variable names and presence only；
- current production deployment and domains。

Do not relink a project, create a new Vercel project, change team, domain, build settings or environment variables just because detection failed. Explain the exact missing decision or access.

## Git is optional

Git provides source history and can trigger connected deployments, but Vercel can also deploy a prepared local artifact through an approved CLI／provider route. Do not block a beginner merely because they do not understand Git.

Use existing Git integration when it is already the project convention and the requested release includes the required commit／push. Otherwise prepare local Preview first. Git commit、push 同 Vercel deploy are separate mutations and each must remain inside the user-authorized scope.

## Preview gate

Before Preview：

1. local build and route QA pass；
2. required env names are `PRESENT`；
3. production-only integrations remain disabled or point to test destinations；
4. target Vercel project／team is known；
5. user has approved creating the Preview in the current turn。

After Preview：

- read deployment metadata and final URL；
- request root, Blog index and each new article route；
- inspect rendered Desktop and 390px Mobile behaviour；
- test CTA navigation and no-write form path；
- inspect relevant logs for runtime errors；
- record deployment ID／URL／artifact identity and unproven items。

Status becomes `HUMAN_REVIEW_STOP`, not production ready.

## Production gate

Require a current-turn approval that identifies the exact production target. Before executing, show a concise release summary and any connected side effects.

Prefer one deliberate deployment. If command output is interrupted, unknown or timed out：

1. inspect Vercel deployment list／provider state；
2. match commit／artifact identity and timestamp；
3. inspect logs and live URL；
4. only retry when evidence shows no successful equivalent deployment exists。

## Live read-back

Production success requires evidence from the actual destination：

- production deployment ID and ready state；
- production domain resolves to expected deployment；
- `/`、`/blog` and article routes return expected content；
- canonical URLs point to production host；
- mobile fixed CTA appears only on article pages；
- first-touch UTM survives article navigation into the form payload；
- approved form test has destination read-back when production smoke is in scope；
- analytics／email／CRM results are labelled verified, not tested, or outside scope separately。

HTTP 200 proves availability only. It does not prove correct content, CTA, CRM write, email delivery or analytics attribution.

## Rollback readiness

Before production, identify the last known good deployment or the provider rollback method. Do not execute rollback unless requested or needed to restore a newly broken production release within the authorized release scope. After rollback, read back the live domain and record which release is active.
