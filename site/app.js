/* God Brain static interface. No network calls, cookies, or persistent storage. */
(() => {
  "use strict";
  const modules = {
    evidence: {
      code: "LAYER 01 / FOUNDATION", title: "Evidence & provenance",
      description: "Distinguish what was independently observed from what a system inferred, predicted, or simulated. Preserve the source and limits of every claim.",
      tags: ["OBSERVATION ≠ INFERENCE", "PROVENANCE"]
    },
    models: {
      code: "LAYER 02 / EXPLANATION", title: "Competing world models",
      description: "Retain rival explanations and testable forecasts without turning a model's fit into causal proof. Prefer independent feedback over self-grading.",
      tags: ["MODEL_FIT ≠ CAUSAL_PROOF", "ALTERNATIVES"]
    },
    memory: {
      code: "LAYER 03 / CONTINUITY", title: "Memory & revision",
      description: "Keep source-bound memory, correction history, contradiction and recovery visible. A stored prediction is never retroactively an observation.",
      tags: ["SUPERSESSION", "RESTART RECOVERY"]
    },
    metacognition: {
      code: "LAYER 04 / SELF-CORRECTION", title: "Metacognition",
      description: "Monitor uncertainty, model conflict, stale evidence and failed strategies. Report what remains unknown instead of silently raising confidence.",
      tags: ["UNCERTAINTY", "ERROR AWARENESS"]
    },
    social: {
      code: "LAYER 05 / RELATIONAL", title: "Social interpretation",
      description: "Keep hypotheses about another participant's intentions revisable. Neither simulated responses nor inferred private states authenticate a speaker.",
      tags: ["PRIVATE STATE ≠ KNOWN", "DIRECT CORRECTION"]
    },
    initiative: {
      code: "LAYER 06 / BOUNDED ACTION", title: "Bounded initiative",
      description: "Generate candidate actions, but require independent effect authority and current consent before real-world execution. A candidate is not a permission.",
      tags: ["CANDIDATE ≠ AUTHORITY", "SCOPED EFFECTS"]
    }
  };

  const buttons = document.querySelectorAll("[data-module]");
  const code = document.getElementById("module-code");
  const title = document.getElementById("module-title");
  const description = document.getElementById("module-description");
  const tags = document.getElementById("module-tags");

  function activateModule(key) {
    const data = modules[key];
    if (!data) return;
    code.textContent = data.code;
    title.textContent = data.title;
    description.textContent = data.description;
    tags.replaceChildren();
    data.tags.forEach((tag) => {
      const label = document.createElement("span");
      label.textContent = tag;
      tags.append(label);
    });
    buttons.forEach((button) => {
      const active = button.dataset.module === key;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
  }
  buttons.forEach((button) => {
    button.addEventListener("click", () => activateModule(button.dataset.module));
  });

  const records = [];
  const form = document.getElementById("evidence-form");
  const kind = document.getElementById("record-kind");
  const input = document.getElementById("record-text");
  const list = document.getElementById("record-list");
  const counter = document.getElementById("record-count");
  const exportButton = document.getElementById("export-records");
  const clearButton = document.getElementById("clear-records");

  function renderEntries() {
    list.replaceChildren();
    counter.textContent = String(records.length).padStart(2, "0") +
      (records.length === 1 ? " entry" : " entries");
    exportButton.disabled = records.length === 0;
    clearButton.disabled = records.length === 0;
    if (!records.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      const symbol = document.createElement("span");
      symbol.className = "empty-symbol";
      symbol.textContent = "⟡";
      symbol.setAttribute("aria-hidden", "true");
      const heading = document.createElement("strong");
      heading.textContent = "No entries yet.";
      const help = document.createElement("p");
      help.textContent = "Begin with evidence. Keep unknowns visible.";
      empty.append(symbol, heading, help);
      list.append(empty);
      return;
    }
    records.forEach((record) => {
      const item = document.createElement("article");
      item.className = "record";
      const head = document.createElement("div");
      head.className = "record-head";
      const badge = document.createElement("span");
      badge.className = "record-kind";
      badge.textContent = record.kind;
      const stamp = document.createElement("time");
      stamp.className = "record-time";
      stamp.dateTime = record.at;
      stamp.textContent = new Date(record.at).toLocaleTimeString([], {
        hour: "2-digit", minute: "2-digit"
      });
      head.append(badge, stamp);
      const body = document.createElement("p");
      body.className = "record-body";
      body.textContent = record.statement;
      item.append(head, body);
      list.append(item);
    });
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const statement = input.value.trim();
    if (!statement || statement.length > 500) return;
    if (!["OBSERVATION", "INFERENCE", "PREDICTION", "HYPOTHESIS", "UNKNOWN"].includes(kind.value)) return;
    records.unshift({kind: kind.value, statement, at: new Date().toISOString()});
    input.value = "";
    renderEntries();
    input.focus();
  });

  exportButton.addEventListener("click", () => {
    if (!records.length) return;
    const documentData = {
      format: "god-brain-evidence-desk/1",
      exportedAt: new Date().toISOString(),
      note: "User-authored local session; entries have not been independently verified.",
      records: records.slice().reverse()
    };
    const blob = new Blob([JSON.stringify(documentData, null, 2)], {type: "application/json"});
    const address = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = address;
    link.download = "god-brain-evidence-session.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(address), 0);
  });

  clearButton.addEventListener("click", () => {
    if (records.length && window.confirm("Discard all unexported entries in this tab?")) {
      records.length = 0;
      renderEntries();
      input.focus();
    }
  });
})();
