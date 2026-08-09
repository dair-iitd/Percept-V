/* Percept-V project page — rendering and interaction */
(function () {
  "use strict";

  const $  = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const el = (tag, cls, txt) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  };
  const fmt = v => (typeof v === "number" ? v.toFixed(2) : v);

  /* ── theme ──────────────────────────────────────────── */
  const root = document.documentElement;
  const stored = localStorage.getItem("pv-theme");
  if (stored) root.setAttribute("data-theme", stored);
  $("#theme-toggle").addEventListener("click", () => {
    const dark = getComputedStyle(root).colorScheme === "dark" ||
                 root.getAttribute("data-theme") === "dark";
    const next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("pv-theme", next);
  });

  /* ── links that have no URL yet ─────────────────────── */
  let anyPending = false;
  $$("[data-link]").forEach(a => {
    if (a.getAttribute("href") === "#") {
      a.classList.add("pending");
      a.removeAttribute("href");
      anyPending = true;
    }
  });
  if (anyPending && $("#btn-note")) $("#btn-note").hidden = false;

  $$(".authors a").forEach(a => {
    if (a.getAttribute("href") === "#") {
      const s = el("span", null, a.textContent);
      a.replaceWith(s);
    }
  });

  /* ── lightbox ───────────────────────────────────────── */
  const lb = $("#lightbox"), lbImg = $("#lb-img");
  document.addEventListener("click", e => {
    const img = e.target.closest(".tcard-img img, .dcard-imgs img, .fig img");
    if (img) { lbImg.src = img.src; lbImg.alt = img.alt; lb.hidden = false; return; }
    if (e.target.closest("#lightbox")) lb.hidden = true;
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape") lb.hidden = true; });

  /* ── teaser ─────────────────────────────────────────── */
  const tg = $("#teaser-grid");
  TEASER.forEach(t => {
    const c = el("div", "tcard");
    c.appendChild(el("div", "tcard-skill", t.skill));
    c.appendChild(el("div", "tcard-q", t.prompt));

    const box = el("div", "tcard-img" + (t.tall ? " tall" : ""));
    const img = el("img");
    img.src = t.img; img.alt = t.skill + " example image"; img.loading = "lazy";
    box.appendChild(img);
    c.appendChild(box);

    const gold = el("div", "ans gold");
    gold.innerHTML = "<b>correct:</b> " + t.gold;
    c.appendChild(gold);

    const pred = el("div", "ans " + (t.correct ? "pred-ok" : "pred-bad"));
    pred.innerHTML = "<b>GPT-4o:</b> " + t.pred;
    c.appendChild(pred);

    tg.appendChild(c);
  });

  /* ── skill → domain table ───────────────────────────── */
  const st = $("#skill-table");
  Object.keys(SKILLS).forEach(k => {
    const row = el("div", "srow");
    const left = el("div");
    const name = el("div", "srow-name");
    name.textContent = SKILLS[k].name;
    const ab = el("span", "abbr", k); name.appendChild(ab);
    left.appendChild(name);
    left.appendChild(el("div", "srow-blurb", SKILLS[k].blurb));
    row.appendChild(left);

    const doms = el("div", "srow-doms");
    SKILL_DOMAINS[k].slice().sort().forEach(d => {
      const t = el("button", "dtag", d);
      t.addEventListener("click", () => jumpToDomain(d));
      doms.appendChild(t);
    });
    row.appendChild(doms);
    st.appendChild(row);
  });

  /* ── answer-type + format-error tables ──────────────── */
  const atBody = $("#answer-type-body");
  Object.keys(ANSWER_TYPES).forEach(k => {
    const a = ANSWER_TYPES[k], tr = el("tr");
    tr.appendChild(el("td", null, a.label));
    tr.appendChild(el("td", null, a.desc));
    const td = el("td", "num", String(a.count)); tr.appendChild(td);
    atBody.appendChild(tr);
  });

  const feBody = $("#format-error-body");
  FORMAT_ERRORS.forEach(r => {
    const tr = el("tr");
    tr.appendChild(el("td", null, ANSWER_TYPES[r[0]].label));
    for (let i = 1; i < r.length; i++) tr.appendChild(el("td", "num", r[i].toFixed(2)));
    feBody.appendChild(tr);
  });

  /* ── results table ──────────────────────────────────── */
  const head = $("#results-head"), body = $("#results-body"), foot = $("#results-foot");
  let view = "skill", sortCol = null, sortDir = -1;

  function heatStyle(v) {
    // 0 → neutral, 100 → strong accent. Keeps text legible in both themes.
    const t = Math.max(0, Math.min(100, v)) / 100;
    return `background: color-mix(in srgb, var(--accent) ${(t * 26).toFixed(1)}%, transparent)`;
  }

  function buildHead() {
    head.innerHTML = "";
    const first = el("th", null, view === "skill" ? "Skill" : "Domain");
    first.dataset.col = "0";
    head.appendChild(first);
    MODELS.forEach((m, i) => {
      const th = el("th", "num");
      th.dataset.col = String(i + 1);
      th.appendChild(document.createTextNode(m.label));
      th.appendChild(el("span", "tag-fam", m.family === "open" ? "open" : "proprietary"));
      head.appendChild(th);
    });
    const avg = el("th", "num sep");
    avg.dataset.col = String(MODELS.length + 1);
    avg.textContent = "Avg.";
    head.appendChild(avg);

    $$("th[data-col]", head).forEach(th => {
      const c = Number(th.dataset.col);
      if (c === sortCol) {
        const a = el("span", "arrow", sortDir === 1 ? "▲" : "▼");
        th.appendChild(a);
      }
      th.addEventListener("click", () => {
        if (sortCol === c) sortDir = -sortDir;
        else { sortCol = c; sortDir = c === 0 ? 1 : -1; }
        render();
      });
    });
  }

  function renderRows() {
    const src = view === "skill" ? RESULTS_SKILL : RESULTS_DOMAIN;
    const rows = src.slice();
    if (sortCol !== null) {
      rows.sort((a, b) => {
        const x = a[sortCol], y = b[sortCol];
        if (typeof x === "string") return sortDir * x.localeCompare(y);
        return sortDir * (x - y);
      });
    }
    body.innerHTML = "";
    rows.forEach(r => {
      const tr = el("tr");
      const nameTd = el("td", view === "domain" ? "rowname" : null, r[0]);
      tr.appendChild(nameTd);
      const best = Math.max(...r.slice(1, MODELS.length + 1));
      for (let i = 1; i <= MODELS.length; i++) {
        const td = el("td", "num cell" + (r[i] === best ? " best" : ""), fmt(r[i]));
        td.setAttribute("style", heatStyle(r[i]));
        tr.appendChild(td);
      }
      tr.appendChild(el("td", "num sep", fmt(r[MODELS.length + 1])));
      body.appendChild(tr);
    });
  }

  function renderFoot() {
    const r = view === "skill" ? RESULTS_SKILL_AVG : RESULTS_DOMAIN_AVG;
    foot.innerHTML = "";
    const tr = el("tr");
    tr.appendChild(el("td", null, r[0]));
    const best = Math.max(...r.slice(1, MODELS.length + 1));
    for (let i = 1; i <= MODELS.length; i++) {
      tr.appendChild(el("td", "num" + (r[i] === best ? " best" : ""), fmt(r[i])));
    }
    tr.appendChild(el("td", "num sep", fmt(r[MODELS.length + 1])));
    foot.appendChild(tr);
  }

  function render() { buildHead(); renderRows(); renderFoot(); }
  render();

  $$(".tab").forEach(t => t.addEventListener("click", () => {
    $$(".tab").forEach(x => x.classList.remove("active"));
    t.classList.add("active");
    view = t.dataset.view;
    sortCol = null; sortDir = -1;
    render();
  }));

  /* ── domain explorer ────────────────────────────────── */
  const domainAcc = {};
  RESULTS_DOMAIN.forEach(r => { domainAcc[r[0]] = r[MODELS.length + 1]; });

  const grid = $("#domain-grid"), emptyMsg = $("#domain-empty");
  const activeSkills = new Set(), activeTypes = new Set();

  const skillFilters = $("#skill-filters");
  Object.keys(SKILLS).forEach(k => {
    const b = el("button", "chip", SKILLS[k].name);
    b.title = SKILLS[k].blurb;
    b.addEventListener("click", () => {
      b.classList.toggle("on");
      activeSkills.has(k) ? activeSkills.delete(k) : activeSkills.add(k);
      filter();
    });
    skillFilters.appendChild(b);
  });

  const answerFilters = $("#answer-filters");
  Object.keys(ANSWER_TYPES).forEach(k => {
    const b = el("button", "chip", ANSWER_TYPES[k].label);
    b.title = ANSWER_TYPES[k].desc;
    b.addEventListener("click", () => {
      b.classList.toggle("on");
      activeTypes.has(k) ? activeTypes.delete(k) : activeTypes.add(k);
      filter();
    });
    answerFilters.appendChild(b);
  });

  DOMAINS.forEach(d => {
    const card = el("div", "dcard");
    card.id = "d-" + d.id;
    card.dataset.id = d.id;

    const imgs = el("div", "dcard-imgs" + (d.images.length > 1 ? " two" : ""));
    d.images.forEach(src => {
      const i = el("img");
      i.src = src; i.alt = d.name + " sample image"; i.loading = "lazy";
      imgs.appendChild(i);
    });
    card.appendChild(imgs);

    const b = el("div", "dcard-body");
    b.appendChild(el("div", "dcard-name", d.id));

    const meta = el("div", "dcard-meta");
    d.skills.forEach(s => {
      const p = el("span", "pill", s);
      p.title = SKILLS[s].name;
      meta.appendChild(p);
    });
    const at = el("span", "pill at", ANSWER_TYPES[d.answer].label);
    at.title = ANSWER_TYPES[d.answer].desc;
    meta.appendChild(at);
    b.appendChild(meta);

    const toggle = el("button", "dcard-toggle", "Show prompt ▾");
    const promptBox = el("div", "dcard-prompt");
    const ul = el("ul");
    d.prompt.forEach(line => ul.appendChild(el("li", null, line)));
    promptBox.appendChild(ul);
    promptBox.hidden = true;
    toggle.addEventListener("click", () => {
      promptBox.hidden = !promptBox.hidden;
      toggle.textContent = promptBox.hidden ? "Show prompt ▾" : "Hide prompt ▴";
    });
    b.appendChild(toggle);
    b.appendChild(promptBox);

    const acc = el("div", "dcard-acc");
    acc.innerHTML = "avg. model accuracy <b>" + domainAcc[d.id].toFixed(2) + "%</b>";
    const bar = el("div", "acc-bar");
    const fill = el("span");
    fill.style.width = domainAcc[d.id] + "%";
    bar.appendChild(fill);
    acc.appendChild(bar);
    b.appendChild(acc);

    card.appendChild(b);
    grid.appendChild(card);
  });

  const search = $("#domain-search");
  search.addEventListener("input", filter);

  function filter() {
    const q = search.value.trim().toLowerCase();
    let shown = 0;
    DOMAINS.forEach(d => {
      const card = $("#d-" + d.id);
      const okSkill = activeSkills.size === 0 || d.skills.some(s => activeSkills.has(s));
      const okType  = activeTypes.size  === 0 || activeTypes.has(d.answer);
      const okQuery = !q || d.id.includes(q) || d.name.toLowerCase().includes(q) ||
                      d.prompt.join(" ").toLowerCase().includes(q);
      const ok = okSkill && okType && okQuery;
      card.hidden = !ok;
      if (ok) shown++;
    });
    emptyMsg.hidden = shown > 0;
  }

  function jumpToDomain(id) {
    activeSkills.clear(); activeTypes.clear();
    $$("#skill-filters .chip, #answer-filters .chip").forEach(c => c.classList.remove("on"));
    search.value = "";
    filter();
    const card = $("#d-" + id);
    if (!card) return;
    card.scrollIntoView({ behavior: "smooth", block: "center" });
    card.classList.remove("flash");
    void card.offsetWidth;
    card.classList.add("flash");
  }

  /* ── human study bars ───────────────────────────────── */
  const bars = $("#human-bars");
  HUMAN_STUDY.forEach(([name, val, isHuman]) => {
    const row = el("div", "bar-row" + (isHuman ? " human" : ""));
    row.appendChild(el("div", "bar-name", name));
    const track = el("div", "bar-track");
    const fill = el("div", "bar-fill");
    fill.style.width = val + "%";
    track.appendChild(fill);
    row.appendChild(track);
    row.appendChild(el("div", "bar-val", val.toFixed(2) + "%"));
    bars.appendChild(row);
  });

  /* ── fine-tuning table ──────────────────────────────── */
  const ftBody = $("#ft-body");
  const check = v => (v ? "✓" : "□");

  function ftSection(label, span) {
    const tr = el("tr", "ft-section");
    const td = el("td", null, label);
    td.colSpan = span;
    tr.appendChild(td);
    ftBody.appendChild(tr);
  }

  function ftRow(r, bestSet) {
    const tr = el("tr");
    for (let i = 0; i < 3; i++) tr.appendChild(el("td", null, typeof r[i] === "number" ? check(r[i]) : r[i]));
    for (let i = 3; i < 8; i++) {
      const td = el("td", "num" + (i === 6 ? " sep" : "") + (bestSet && bestSet.has(i) ? " best" : ""), r[i].toFixed(2));
      tr.appendChild(td);
    }
    ftBody.appendChild(tr);
  }

  ftSection("Baseline (no fine-tuning)", 8);
  ftRow(FINETUNE.baseline);

  ftSection("LoRA fine-tuning (rank 8)", 8);
  const loraBest = bestCols(FINETUNE.lora);
  FINETUNE.lora.forEach(r => ftRow(r, bestFor(r, loraBest)));

  ftSection("Full fine-tuning", 8);
  const fullBest = bestCols(FINETUNE.full);
  FINETUNE.full.forEach(r => ftRow(r, bestFor(r, fullBest)));

  function bestCols(rows) {
    const best = {};
    for (let i = 3; i < 8; i++) best[i] = Math.max(...rows.map(r => r[i]));
    return best;
  }
  function bestFor(row, best) {
    const s = new Set();
    for (let i = 3; i < 8; i++) if (row[i] === best[i]) s.add(i);
    return s;
  }

  /* ── appendix tables ────────────────────────────────── */
  function fillTable(bodyId, rows, monoFirst) {
    const tb = $("#" + bodyId);
    if (!tb) return;
    rows.forEach(r => {
      const isTotal = /^(Average|Full)/.test(r[0]);
      const tr = el("tr", isTotal ? "total" : null);
      tr.appendChild(el("td", monoFirst && !isTotal ? "rowname" : null, r[0]));
      for (let i = 1; i < r.length; i++) {
        const cls = "num" + (tb.dataset.sep && Number(tb.dataset.sep.split(",").indexOf(String(i))) > -1 ? " sep" : "");
        tr.appendChild(el("td", cls, r[i].toFixed(2)));
      }
      tb.appendChild(tr);
    });
  }

  $("#oneshot-body") && fillTable("oneshot-body", ONE_SHOT, false);
  $("#res-body")     && (($("#res-body").dataset.sep = "1,4"), fillTable("res-body", RESOLUTION, false));
  $("#threed-body")  && (($("#threed-body").dataset.sep = "1,3"), fillTable("threed-body", THREE_D, true));
  $("#prompt-body")  && (($("#prompt-body").dataset.sep = "1,3"), fillTable("prompt-body", PROMPT_STYLE, false));

  /* ── copy bibtex ────────────────────────────────────── */
  const copyBtn = $("#copy-bib");
  copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText($("#bib").innerText);
      copyBtn.textContent = "Copied";
    } catch (e) {
      copyBtn.textContent = "Press ⌘C";
      const range = document.createRange();
      range.selectNodeContents($("#bib"));
      const sel = window.getSelection();
      sel.removeAllRanges(); sel.addRange(range);
    }
    setTimeout(() => { copyBtn.textContent = "Copy"; }, 1800);
  });
})();
