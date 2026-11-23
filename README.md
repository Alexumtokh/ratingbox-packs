# RatingBox packs

Question packs for the RatingBox app.

## Adding or updating a pack
Upload the `.json` / `.zip` file into the `packs/` folder (Add file → Upload files, or `git push`).
To update a pack, upload it again **with the same name**. To remove one, delete it from `packs/`.
File names: Latin letters, digits, `.`, `-`, `_` only (no spaces).

The **Publish packs** action then builds `manifest.json` (a version goes up only when the file changed)
and publishes everything to the GitHub release `packs`, Netlify and GitLab. The app sees it on its next start.

Optional `packs/titles.json`: `{"kimyo-7": "Kimyo 7-sinf"}` for display names.

## Secrets (Settings → Secrets and variables → Actions)
`NETLIFY_TOKEN`, `NETLIFY_SITE_ID`, `GITLAB_TOKEN`, `GITLAB_PROJECT_ID`.
