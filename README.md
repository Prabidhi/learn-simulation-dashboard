# Learn Dashboards

Interactive, standalone, offline HTML learning dashboards, published with GitLab Pages.

## How it works

Every merge to `main` runs the `pages` job in `.gitlab-ci.yml`, which runs
`scripts/build_site.py`:

1. Everything in `dashboards/` is copied to `public/`.
2. Each **topic repo** listed in `topics.json` is downloaded into its folder, e.g.
   [learn-oracle](https://gitlab.com/Prabidhi/learn-oracle) into `public/oracle/`.
   Its `pages.json` entries are added to the menu.
3. GitLab Pages publishes `public/` at https://learn.prabidhis.com.

A push to a topic repo's `main` triggers this pipeline, so its pages go live too.

## Topic repos

Big topics live in their own repo but share this one website, so the theme, menu,
search and addresses stay the same. Today that's Oracle (`learn-oracle`). To add
another, create the repo with its pages and a `pages.json`, then add it to
`topics.json`. Small topics stay as folders in `dashboards/`.

## Learning dashboards for other projects

[LEARNING_DASHBOARD_GUIDE.md](LEARNING_DASHBOARD_GUIDE.md) is a self-contained guide
to copy into any other project. Ask Claude there to read it and build a learning
dashboard, and it explains how to study the project, the page rules, data and
privacy rules, testing, and how to add the page here. It includes a starter page.

## Adding a dashboard

1. Create a branch and add your `.html` file under `dashboards/`, in folders
   that match its place in the side menu (e.g. `dashboards/devops/git/`).
2. Give the page a meaningful `<title>`.
3. Add an entry to the `DASHBOARDS` list in `dashboards/index.html`.
   Without one the page still deploys, but the home page won't link to it.
4. Run `python3 scripts/update_csp.py` to add or refresh the security policies.
5. Open a merge request and merge it to `main`.
6. When the pipeline finishes, the page is live.

## Rules for dashboard files

- Keep them self-contained: put all CSS and JS inline and draw with inline SVG or canvas.
  The Content-Security-Policy blocks separate files, images, fonts and network calls.
- Run `python3 scripts/update_csp.py` after editing any inline `<script>`, including
  the `DASHBOARDS` list. A page's scripts stop running if its policy is out of date,
  and the `csp-check` pipeline job blocks the deploy until it is fixed.
- A page that needs more can have its policy edited by hand; the script only
  refreshes the hashes.
- Never start links with `/`; the site lives under `/<project-name>/`.

## Site URL

Find it under **Deploy → Pages** in the project sidebar.
Usually `https://<namespace>.gitlab.io/<project-name>/`.

## Run locally

```bash
python3 scripts/build_site.py          # builds public/, downloading topic repos
python3 -m http.server -d public 8000  # open http://localhost:8000
```

Use `python3 scripts/build_site.py --local oracle=../learn-oracle` to preview a
local copy of a topic repo.

## Copies

GitLab is the main copy and runs the website. A copy is kept at
[github.com/Prabidhi/learn-simulation-dashboard](https://github.com/Prabidhi/learn-simulation-dashboard).
