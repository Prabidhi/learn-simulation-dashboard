# Learning Dashboard Guide

Copy this file into the root of any project. It tells Claude (or anyone) how to
turn that project into an interactive learning dashboard for the
**Learning Lab**: one offline HTML page that teaches the project's concepts,
simulates how it works, and walks through how to use it.

To use it, open the project and ask:

> Read `LEARNING_DASHBOARD_GUIDE.md` and build a learning dashboard for this project.

You can narrow it, for example: "…focused on the deploy pipeline", or
"…for someone new to the team".

| | |
|---|---|
| Learning Lab repository | `~/C/MyProjects/learn-simulation-dashboard` (GitLab: `Prabidhi/learn-simulation-dashboard`) |
| Live site | https://learn-simulation-dashboard-38cb3c.gitlab.io/ |
| Good examples to copy from | `dashboards/security/csp-explained.html`, `dashboards/mental-models/pareto-rule.html`, `dashboards/ai/jev-explained.html` |

---

## 1. Study the project before writing anything

The page is only useful if it's true. Work from the code, not from guesses.

1. Read the README, the main entry points, configuration and build files, CI files,
   and any docs folder.
2. Work out:
   - what problem the project solves, and for whom
   - its main parts and how data or requests move between them
   - the 5–10 ideas someone must understand to work on it
   - how to set it up, run it, test it and deploy it
   - the decisions that look odd until explained ("why X instead of Y")
   - what tends to break, and how you'd notice
3. Run harmless read-only commands if they help (listing files, `--help`, tests).
   Never run anything that deploys, deletes, sends data or costs money.
4. Keep a list of anything you couldn't confirm. Either leave it out or label it
   on the page as unconfirmed. Never present a guess as a fact.

## 2. Plan the page

Choose 5–8 numbered sections. A typical page for a software project:

| Section | What it does |
|---|---|
| 1. The big picture | What it's for, in two sentences, plus a clickable diagram of the main parts |
| 2. Key ideas | The core concepts, each with a plain explanation and an everyday analogy |
| 3. Watch it work | An animated or step-through simulation of the main flow (a request, a pipeline run, a calculation) |
| 4. Try it | Controls (sliders, toggles, inputs) that change the simulation, with live results |
| 5. How to use it | Setup, run and deploy steps as a stepper, with commands shown as text to copy |
| 6. Break it on purpose | Common mistakes, what you'd see, and how to fix them |
| 7. Why it's built this way | Trade-offs and decisions, compared side by side |
| 8. Quiz | 6–10 questions, each with an explanation |

Every section should let the reader **do** something, not only read. Prefer real
calculations over fake ones. For example, compute an actual hash, formula or
cost rather than hard-coding the result. When something can't be real (timings,
sample records), make it clearly illustrative.

## 3. The page contract (hard rules)

### One file, fully offline
- Exactly one `.html` file. All CSS goes in one `<style>` block and all JS in `<script>`
  blocks, with no external files.
- No CDNs, libraries, web fonts, external images, `fetch`/XHR, iframes or form
  submissions. Draw with inline SVG or `<canvas>`. Use system fonts.
- It must work when opened straight from disk (`file://`), on the Lab site,
  and inside the Lab's home page frame.
- Never start a link with `/`. The site lives under a sub-path.
- External links to sources are fine. They only use the network when clicked. Add
  `target="_blank" rel="noopener noreferrer"`.

### Content-Security-Policy (CSP)
Every page carries this meta tag, **directly after `<meta charset="utf-8">`**:

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'sha256-…'; style-src 'unsafe-inline'; img-src 'none'; font-src 'none'; connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'">
```

- `script-src` lists one SHA-256 hash per inline `<script>`. Any edit to a script,
  even one space, changes its hash, and the browser then blocks it. There's no
  expiry date: an unedited page keeps working indefinitely.
- In the Lab, don't write the tag by hand. Run `python3 scripts/update_csp.py`,
  which adds or refreshes it. The pipeline job `csp-check` fails if any hash is stale.
- Outside the Lab, compute hashes with the snippet in [section 9](#9-csp-hashes-outside-the-lab).
- Keep `style-src 'unsafe-inline'`. Style attributes and `el.style` are fine.

### Themes (must match the Lab exactly)
- Three themes: `day`, `twilight` and `dark`, set as `data-theme` on `<html>`.
- The first script in `<head>` reads `localStorage['lab-theme']` before the page
  paints. Copy it exactly from the starter page.
- The theme switch lives inside an element with `id="themes"`. The Lab hides it
  when the page is shown inside its frame, because the Lab has its own switch.
- Define `window.onThemeChange`. The Lab calls it after changing `data-theme`, so
  anything drawn in JS colours can redraw. Prefer CSS variables so nothing needs
  redrawing.
- Listen for the `storage` event on `lab-theme`, so other open tabs stay in sync.
- Define every colour as a CSS variable for each theme, plus a
  `prefers-color-scheme: dark` fallback for when no theme is saved. Give `body` an
  explicit background.

### Layout and accessibility
- A header with an `<h1>`, a one-line subtitle and a short **key idea** box.
- A sticky row of numbered section links, holding the theme switch. Under 560px
  wide it stops being sticky.
- Max width about 1180px. It must work at 375px wide with **no sideways scroll**.
  Wide tables go in a scrolling wrapper.
- Every control has a visible label. Toggle buttons use `aria-pressed`. Results
  that change use `aria-live="polite"`. Everything works by keyboard.
- Respect `prefers-reduced-motion`: skip or shorten animations.
- Colour is never the only signal. Pair it with text, an icon or position.
- Wrap every `localStorage` call in `try/catch`, and use it only for conveniences
  such as a remembered tab or draft.

### Charts
- One y-axis per chart, never two. If two measures have different units, use two
  charts or convert both to the same unit, such as % of total.
- A legend whenever there are two or more series. Label only the important points
  directly, never every point.
- Hover and keyboard focus show a tooltip, and every value is also available as
  text, for example in a "Show the numbers" table.
- Thin marks, solid hairline gridlines, and text in text colours (not series colours).
- Size SVGs to their container's real width, redrawing on resize, instead of
  stretching them. Stretched text becomes unreadable on phones.
- Check that series colours can be told apart by colour-blind readers.

## 4. Data, privacy and licences

These follow the owner's global rules and are not optional.

- **Free and open only.** No paid software, libraries, fonts or services. Since the
  page uses no libraries at all, this is usually automatic.
- **Data.** Use invented sample data, clearly labelled as invented, or public data
  whose reuse terms you have confirmed at the source. Free to download isn't
  permission. If terms can't be confirmed, don't use it: say so and suggest a
  public alternative, such as US government data.
- Don't scrape websites, and don't copy another app's numbers, scores, rankings or
  forecasts. If a page seems to need a real-world figure, ask the owner first.
- No private personal data, ever.
- **The Lab is public.** Anyone on the internet can read every page. Never include
  secrets, API keys, passwords, internal hostnames, IP addresses, customer or
  employee data, or confidential code. **Ask the owner before including anything
  that names an employer, client, internal system, colleague or location.** If the
  project is a work project, teach its concepts with generic names.
- If a rule limits a feature, say so plainly rather than quietly dropping it.

## 5. Writing style

- Plain words and short sentences. Explain each technical term the first time it
  appears.
- One everyday analogy per big idea, in an **Analogy:** callout.
- Sentence-case headings. No hype words, such as "revolutionary" or "seamless".
- Be honest about what's simulated. Add a short banner if the page simulates a real
  system, and label illustrative numbers as illustrative.
- When you cite a fact, link the source in a collapsible Sources list and say
  when it was checked.
- Quiz answers explain **why**, for right and wrong picks alike.

## 6. Test before calling it done

- [ ] Opened directly from disk: everything renders and every control works.
- [ ] The browser console shows no errors and no CSP violations.
- [ ] Tried every button, slider, toggle and input, including edge cases: zero,
      empty, maximum, nonsense text. Typed text is shown with `textContent`,
      never `innerHTML`.
- [ ] All three themes look right, and switching theme doesn't break drawn charts.
- [ ] At 375px wide there's no sideways scroll, and labels aren't clipped or
      overlapping.
- [ ] Works by keyboard, and with reduced motion turned on.
- [ ] Quiz scoring works when all answers are right and when all are wrong, and
      Reset works.
- [ ] No network requests other than the page itself.
- [ ] Every fact on the page has been checked against the code or a cited source.

## 7. Add it to the Learning Lab

The page can be built anywhere, but it's published from the Lab repository, or from
a **topic repo** the Lab pulls in when it builds.

> **Oracle pages go in the `learn-oracle` repo, not here.** Put the file in its
> `ords/` or `apex/` folder, add an entry to its `pages.json` (same fields as below,
> with `href` relative to that repo), and run
> `python3 ../learn-simulation-dashboard/scripts/update_csp.py --root .` there.
> The Lab's `topics.json` lists every topic repo. The steps below are for every
> other topic.

1. Put the file in the Lab under `dashboards/`, in folders that **match its place in
   the side menu**:
   - a plain topic: `dashboards/<topic>/<page>.html`, e.g. `dashboards/ai/jev-explained.html`
   - a section with subtopics: `dashboards/<section>/<topic>/<page>.html`, e.g.
     `dashboards/devops/git/git-simulator.html`
2. Add one entry to the `DASHBOARDS` list in `dashboards/index.html`:

   ```js
   {
     title: 'My Project, Explained',
     href: 'devops/my-project/my-project-explained.html', // path from index.html
     section: 'DevOps',          // optional: groups the topic under a heading
     topic: 'my-project',        // the folder name
     added: 'YYYY-MM-DD',        // today; pages under 14 days old show "New"
     desc: 'One sentence on what the reader will learn.',
     points: ['Three short', 'hands-on things', 'to try'],
     tags: ['search', 'words']
   },
   ```

3. Optional: give the topic a nice name and colour in `TOPICS`, adding its CSS
   variable to each of the four theme blocks at the top of `index.html`. Optionally
   add a card illustration in `ART`. Without these, the topic still works with a
   default look.
4. Run `python3 scripts/update_csp.py`. This refreshes the new page and
   `index.html`, whose hash changes whenever `DASHBOARDS` changes.
5. Test locally: `python3 scripts/build_site.py`, which builds the whole site in
   `public/` (downloading topic repos), then `python3 -m http.server -d public 8000`
   and open `http://localhost:8000`. To try a local copy of a topic repo, add
   `--local oracle=../learn-oracle`.
6. Publish with a branch, a commit, a push and a merge to `main`. The pipeline runs
   `csp-check` and then deploys. **Ask the owner before each step: commit, push
   and merge are approved one at a time.**

If you're working in another project and can't write to the Lab folder, save the
page as `learning/<name>.html` in that project and tell the owner where it is.

## 8. Starter page

Copy this into a new file and replace everything marked `TODO`. It already
follows the contract: themes, Lab embedding, CSP-friendly inline code, a small
working simulation and a quiz. The CSP tag is added by `update_csp.py` (or see
section 9).

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>/* Learning Lab: apply the saved Day/Twilight/Dark mode before the page paints */try{var t=localStorage.getItem("lab-theme");if(t==="light")t="day";if(t==="day"||t==="twilight"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TODO Project, Explained</title>
<meta name="description" content="TODO One sentence on what this page teaches.">
<style>
:root{--bg:#f6f7f9;--panel:#fff;--fg:#1f2328;--muted:#656d76;--line:#d8dee4;--chip:#eef1f4;--a:#0f8a6c;--a-soft:#dff4ee;--ok-soft:#e3f5e8;--bad-soft:#fde8e8;--on-a:#fff;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
:root[data-theme="dark"]{--bg:#0d1117;--panel:#161b22;--fg:#e6edf3;--muted:#8b949e;--line:#30363d;--chip:#21262d;--a:#3fcf9e;--a-soft:#10332a;--ok-soft:#10301b;--bad-soft:#3d1518;--on-a:#0d1117}
@media (prefers-color-scheme:dark){:root:not([data-theme]){--bg:#0d1117;--panel:#161b22;--fg:#e6edf3;--muted:#8b949e;--line:#30363d;--chip:#21262d;--a:#3fcf9e;--a-soft:#10332a;--ok-soft:#10301b;--bad-soft:#3d1518;--on-a:#0d1117}}
:root[data-theme="twilight"]{--bg:#231f38;--panel:#2b2544;--fg:#f6ebe6;--muted:#b9aac4;--line:#433a63;--chip:#352e52;--a:#7ee2c0;--a-soft:#24404a;--ok-soft:#24394a;--bad-soft:#4a2b3f;--on-a:#211b33}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 var(--sans)}
header,main,footer{max-width:1180px;margin:0 auto;padding:20px}
header h1{margin:0 0 6px;font-size:1.65rem}
header p{margin:0;color:var(--muted)}
.idea{margin-top:12px;padding:12px 16px;border-radius:10px;background:var(--panel);border:1px solid var(--line)}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
nav>div{max-width:1180px;margin:0 auto;padding:8px 20px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
nav a{font-size:.82rem;text-decoration:none;color:var(--fg);padding:5px 11px;border-radius:999px;border:1px solid var(--line);background:var(--panel)}
.themes{display:flex;gap:2px;margin-left:auto;padding:3px;border:1px solid var(--line);border-radius:999px;background:var(--panel)}
.themes button{font:inherit;font-size:.78rem;border:0;background:none;color:var(--muted);padding:5px 11px;border-radius:999px;cursor:pointer}
.themes button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
section{margin:28px 0;scroll-margin-top:60px}
section>h2{margin:0 0 4px;font-size:1.28rem}
.lead{margin:0 0 12px;color:var(--muted)}
.analogy{border-left:3px solid var(--a);background:var(--a-soft);padding:8px 12px;margin:0 0 14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
label{display:block;font-size:.86rem}
input[type=range]{width:100%;accent-color:var(--a)}
.readout{margin-top:10px;padding:8px 12px;border-radius:8px;background:var(--chip)}
.q{padding:10px 0;border-top:1px solid var(--line)}
.q button{display:block;width:100%;text-align:left;font:inherit;margin:6px 0;padding:7px 10px;border-radius:8px;border:1px solid var(--line);background:var(--chip);color:var(--fg);cursor:pointer}
.q button.right{background:var(--ok-soft)}
.q button.wrong{background:var(--bad-soft)}
button:focus-visible,a:focus-visible,input:focus-visible{outline:2px solid var(--fg);outline-offset:2px}
footer{color:var(--muted);font-size:.8rem}
@media (max-width:560px){nav{position:static}header,main,footer,nav>div{padding-left:14px;padding-right:14px}}
</style>
</head>
<body>
<header>
  <h1>TODO Project, Explained</h1>
  <p>TODO One line on what the project is.</p>
  <div class="idea"><b>Key idea:</b> TODO the one sentence to remember.</div>
</header>
<nav><div>
  <a href="#idea">1. The idea</a>
  <a href="#try">2. Try it</a>
  <a href="#quiz">3. Quiz</a>
  <div class="themes" id="themes" role="group" aria-label="Colour theme"></div>
</div></nav>
<main>
  <section id="idea">
    <h2>1. The idea</h2>
    <p class="lead">TODO Explain the concept in plain words.</p>
    <div class="analogy"><b>Analogy:</b> TODO an everyday comparison.</div>
  </section>
  <section id="try">
    <h2>2. Try it</h2>
    <p class="lead">TODO Replace this example with a simulation of the project.</p>
    <div class="card">
      <label for="n">Items: <b id="nV"></b></label>
      <input type="range" id="n" min="1" max="100" value="10">
      <div class="readout" id="out" aria-live="polite"></div>
    </div>
  </section>
  <section id="quiz">
    <h2>3. Quiz</h2>
    <p class="lead" id="score"></p>
    <div class="card" id="quizBox"></div>
  </section>
</main>
<footer>One file, no network calls. TODO Say what's simulated or invented.</footer>
<script>
const $ = s => document.querySelector(s);

/* ---------- simulation (TODO replace) ---------- */
function draw(){
  const n = +$('#n').value;
  $('#nV').textContent = n;
  $('#out').textContent = `${n} items take ${n * 2} steps one by one, or 2 steps in parallel.`;
}
$('#n').addEventListener('input', draw);
draw();

/* ---------- quiz ---------- */
const QUIZ = [
  {q:'TODO question?', o:['Wrong answer', 'Right answer'], a:1, w:'TODO why the right answer is right.'}
];
let right = 0, done = 0;
$('#quizBox').innerHTML = QUIZ.map((q, i) => `<div class="q" data-i="${i}"><b></b>${q.o.map((_, k) => `<button data-k="${k}"></button>`).join('')}<p class="why" hidden></p></div>`).join('');
document.querySelectorAll('.q').forEach(d => { const q = QUIZ[+d.dataset.i]; d.querySelector('b').textContent = q.q; d.querySelectorAll('button').forEach((b, k) => b.textContent = q.o[k]); });
$('#quizBox').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b || b.disabled) return;
  const d = b.closest('.q'), q = QUIZ[+d.dataset.i], pick = +b.dataset.k, all = d.querySelectorAll('button');
  all.forEach(x => x.disabled = true); all[q.a].classList.add('right'); if (pick !== q.a) b.classList.add('wrong'); else right++;
  done++; const why = d.querySelector('.why'); why.hidden = false; why.textContent = (pick === q.a ? 'Correct. ' : 'Not quite. ') + q.w;
  $('#score').textContent = `${right} of ${done} right`;
});
$('#score').textContent = `Answer all ${QUIZ.length} questions.`;

/* ---------- theme: shared with the Learning Lab through localStorage "lab-theme" ---------- */
window.onThemeChange = () => {};   // TODO redraw anything coloured in JS here
(function(){
  const LIST = [['day', 'Day'], ['twilight', 'Twilight'], ['dark', 'Dark']];
  const root = document.documentElement, box = document.getElementById('themes');
  const cur = () => root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'day');
  function paint(){ const c = cur(); box.innerHTML = LIST.map(([k, l]) => `<button data-k="${k}" aria-pressed="${k === c}">${l}</button>`).join('');
    box.querySelectorAll('button').forEach(b => b.onclick = () => set(b.dataset.k)); }
  function set(t){ root.dataset.theme = t; try { localStorage.setItem('lab-theme', t); } catch (e) {} paint(); window.onThemeChange(); }
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { if (!root.dataset.theme) { paint(); window.onThemeChange(); } });
  window.addEventListener('storage', e => { if (e.key === 'lab-theme' && e.newValue) { root.dataset.theme = e.newValue; paint(); window.onThemeChange(); } });
  paint();
})();
</script>
</body>
</html>
```

## 9. CSP hashes outside the Lab

If the page isn't in the Lab yet, compute the hashes with Python's standard
library, then paste them into the `script-src` part of the meta tag from
[section 3](#content-security-policy-csp):

```bash
python3 - page.html <<'EOF'
import base64, hashlib, re, sys
html = open(sys.argv[1], encoding='utf-8').read()
for script in re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.S):
    print("'sha256-" + base64.b64encode(hashlib.sha256(script.encode('utf-8')).digest()).decode() + "'")
EOF
```

Run it again after every script edit. Once the page moves into the Lab,
`update_csp.py` takes over.
