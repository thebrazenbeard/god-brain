/* Explicit, anonymous new-thread handoff from GitHub Pages to the private room.
   No background requests, stored credentials, or private-thread API calls. */
(() => {
  "use strict";
  const form = document.getElementById("dialogue-form");
  const name = document.getElementById("sender-name");
  const draft = document.getElementById("draft-message");
  const consent = document.getElementById("privacy-approval");
  const send = document.getElementById("send-message");
  const status = document.getElementById("send-status");
  const csrf = document.getElementById("csrf-value");
  const token = document.getElementById("initial-token");
  const requestKey = document.getElementById("request-key");
  if (!form || !name || !draft || !consent || !send || !status ||
      !csrf || !token || !requestKey) return;

  let busy = false;
  const update = () => {
    send.disabled = busy || !name.value.trim() || !draft.value.trim() ||
      !consent.checked;
  };
  for (const control of [name, draft, consent]) {
    control.addEventListener("input", update);
    control.addEventListener("change", update);
  }
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (busy || send.disabled || !form.reportValidity()) return;
    // An async ticket lookup must never submit edits made after the click.
    const intendedName = name.value;
    const intendedDraft = draft.value;
    busy = true;
    update();
    status.textContent = "Connecting to the private room...";
    try {
      const response = await fetch(
        "https://lappy.tail86ea75.ts.net:10000/pages-handoff-ticket",
        {method: "GET", mode: "cors", credentials: "omit", cache: "no-store"}
      );
      if (!response.ok) throw new Error("Ticket not available");
      const ticket = await response.json();
      if (!ticket ||
          !/^[A-Za-z0-9_-]{32,64}$/.test(ticket.csrf) ||
          !/^[A-Za-z0-9_-]{40,50}$/.test(ticket.initial_token) ||
          !/^[A-Za-z0-9_-]{24,64}$/.test(ticket.request_key)) {
        throw new Error("Invalid anonymous form ticket");
      }
      if (name.value !== intendedName || draft.value !== intendedDraft ||
          !consent.checked) {
        throw new Error("Draft or consent changed before submission");
      }
      csrf.value = ticket.csrf;
      token.value = ticket.initial_token;
      requestKey.value = ticket.request_key;
      status.textContent = "Opening your private conversation...";
      // Native form navigation follows the server's 303 return-link redirect.
      // No fetch, browser storage, or CORS read is used for private threads.
      form.submit();
    } catch {
      status.textContent = "Could not connect to the private room. Nothing was sent; copy your draft and open the private room instead.";
      busy = false;
      update();
    }
  });
  window.addEventListener("pageshow", (event) => {
    if (!event.persisted || !busy) return;
    // BFCache may restore this page after a completed POST. Preserve the
    // draft, but require fresh acknowledgement before another submission.
    busy = false;
    consent.checked = false;
    csrf.value = "";
    token.value = "";
    requestKey.value = "";
    status.textContent = "You returned to your draft. Your previous message may already have been sent; check your private return link before sending again.";
    update();
  });
  update();
})();
