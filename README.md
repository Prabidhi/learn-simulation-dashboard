# Learn Dashboards

Interactive, standalone, offline HTML learning dashboards, published with GitLab Pages.

## How it works

Every merge to `main` runs the `pages` job in `.gitlab-ci.yml`:

1. Everything in `dashboards/` is copied to `public/`.
2. If `dashboards/index.html` exists, it is used as the home page.
   Otherwise the `pages` job generates a plain searchable list
   linking to every dashboard (using each file's path).
3. GitLab Pages publishes `public/`.

## Adding a dashboard

1. Create a branch and add your `.html` file under `dashboards/`
   (subfolders are fine).
2. Give the page a meaningful `<title>`.
3. Add an entry to the `DASHBOARDS` list in `dashboards/index.html`.
   Without one the page still deploys, but the home page won't link to it.
4. Open a merge request and merge it to `main`.
5. When the pipeline finishes, the page is live.

## Rules for dashboard files

- Keep them self-contained, or keep assets next to them and use **relative paths**.
- Never start links with `/`; the site lives under `/<project-name>/`.

## Site URL

Find it under **Deploy → Pages** in the project sidebar.
Usually `https://<namespace>.gitlab.io/<project-name>/`.

## Run locally

```bash
python3 -m http.server -d dashboards 8000
# open http://localhost:8000
```
