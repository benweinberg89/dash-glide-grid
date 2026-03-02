---
name: release
description: Merge feature branch, tag a release, create GitHub release with notes, and publish to PyPI
disable-model-invocation: true
allowed-tools: Bash(*), Read, Edit, Glob, Grep
argument-hint: "<version>"
---

# Release dash-glide-grid v$ARGUMENTS

## Pre-flight checks

1. If `$ARGUMENTS` is empty, read the current version from `dash_glide_grid/package-info.json` and ask the user what the new version should be.
2. Confirm the working tree is clean (`git status`). If dirty, **stop and tell the user**.
3. Confirm the version in all three version files is still the *previous* version (not already bumped).

## Step 0 — Merge to main (if needed)

If we are NOT on `main`:

1. Determine the current branch name.
2. Collect the commits that will be merged: `git log --oneline main..HEAD`
3. Create a PR targeting `main` using `gh pr create`:
   - Title: `release: v$ARGUMENTS`
   - Body: auto-generated from the commit list, grouped by type (feat/fix/docs/etc.)
4. **Ask the user to confirm** before merging.
5. Merge the PR using `gh pr merge --squash --delete-branch` (squash merge to keep main clean).
6. Switch to main and pull: `git checkout main && git pull origin main`

If already on `main`, just confirm it's up to date with `git pull origin main`.

## Step 1 — Bump version

Update the version string in **all three files**:

- `pyproject.toml` → `version = "$ARGUMENTS"`
- `package.json` → `"version": "$ARGUMENTS"`
- `dash_glide_grid/package-info.json` → `"version": "$ARGUMENTS"`

## Step 2 — Build

Run the full build:

```
npm run build
```

Then build the Python distribution:

```
uv build
```

Verify the new `.whl` and `.tar.gz` in `dist/` have the correct version in their filenames.

## Step 3 — Commit, tag, and push

```
git add -A
git commit -m "release: v$ARGUMENTS"
git tag $ARGUMENTS
git push origin main
git push origin $ARGUMENTS
```

## Step 4 — GitHub Release

Collect commits since the previous tag:

```
git log --oneline <previous_tag>..$ARGUMENTS
```

Create the GitHub release using `gh`:

```
gh release create $ARGUMENTS --title "v$ARGUMENTS" --notes "<release_notes>"
```

Format the release notes with:
- A short summary of what changed
- A list of commits (hash + message)

## Step 5 — Publish to PyPI

First remove any old version artifacts from `dist/` (only the current version's files should remain), then publish:

```
twine upload dist/*
```

If this fails due to missing credentials, tell the user to configure a `~/.pypirc` or set `TWINE_USERNAME`/`TWINE_PASSWORD`.

## Done

Print a summary with links to:
- GitHub release: `https://github.com/benweinberg89/dash-glide-grid/releases/tag/$ARGUMENTS`
- PyPI: `https://pypi.org/project/dash-glide-grid/$ARGUMENTS/`
