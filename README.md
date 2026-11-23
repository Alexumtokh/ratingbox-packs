# RatingBox packs

Question packs for the RatingBox app.

## Adding or updating a pack
Upload the `.json` / `.zip` file into its kind's folder (Add file → Upload files, or `git push`):
- `packs/questions/`: question packs (`kind: "questions"`)
- `packs/books/`: book content (`kind: "book"`)

Files right in `packs/` count as questions (old layout). A file name must be unique across the folders.
To update a pack, upload it again **with the same name** into the same folder. To remove one, delete it.
File names: Latin letters, digits, `.`, `-`, `_` only (no spaces).

The **Publish packs** action then builds `manifest.json` (a version goes up only when the file changed)
and publishes everything to the GitHub release `packs`, Netlify and GitLab. The app sees it on its next start.

Optional `packs/titles.json`: `{"kimyo-7": "Kimyo 7-sinf"}` for display names.

## Secrets (Settings → Secrets and variables → Actions)
`NETLIFY_TOKEN`, `NETLIFY_SITE_ID`, `GITLAB_TOKEN`, `GITLAB_PROJECT_ID`.
