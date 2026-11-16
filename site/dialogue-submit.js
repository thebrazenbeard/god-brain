/* Explicit, anonymous new-thread handoff from GitHub Pages to the private room.
   No background requests, stored credentials, or private-thread API calls. */
(() => {
  "use strict";
  const origin = "https://lappy.tail86ea75.ts.net:10000";
  const form = document.getElementById("dialogue-form");
  const name = document.getElementById("sender-name");
  const draft = document.getElementById("draft-message");
  const consent = document.getElementById("privacy-approval");
  const send = document.getElementById("send-message");
  const status = document.getElementById("send-status");
  const csrf = document.getElementById("csrf-value");
  const token = document.getElementById("initial-token");
  const requestKey = document.getElementById("request-key");
  const returnPanel = document.getElementById("return-link-panel");
  const returnUrl = document.getElementById("private-return-url");
  const copyReturn = document.getElementById("copy-return-link");
  const saved = document.getElementById("return-link-saved");
  if (!form || !name || !draft || !consent || !send || !status ||
      !csrf || !token || !requestKey || !returnPanel || !returnUrl ||
      !copyReturn || !saved) return;

  // GitHub Pages cannot set frame-ancestors response headers. Prevent direct
  // submission from framed views; the HTML Send button defaults to disabled
  // when scripts are blocked. This is mitigation, not an HTTP framing policy.
  if (window.top !== window.self) {
    status.textContent = "Direct sending is disabled in embedded pages. Open the private room in a separate tab.";
    return;
  }

  let busy = false;
  let prepared = null;
  const clearPrepared = () => {
    prepared = null;
    csrf.value = "";
    token.value = "";
    requestKey.value = "";
    returnUrl.value = "";
    saved.checked = false;
    returnPanel.hidden = true;
  };
  const update = () => {
    if (prepared &&
        (name.value !== prepared.name ||
         draft.value !== prepared.message || !consent.checked)) {
      clearPrepared();
      status.textContent = "Your draft or consent changed. Prepare a new private return link before sending.";
    }
    send.textContent = prepared ? "Send privately" : "Prepare private link";
    send.disabled = busy || !name.value.trim() || !draft.value.trim() ||
      !consent.checked || (prepared !== null && !saved.checked);
  };
  for (const control of [name, draft, consent]) {
    control.addEventListener("input", update);
    control.addEventListener("change", update);
  }
  saved.addEventListener("change", update);

  copyReturn.addEventListener("click", async () => {
    if (!prepared) return;
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) {
        throw new Error("Clipboard unavailable");
      }
      await navigator.clipboard.writeText(returnUrl.value);
      status.textContent = "Private link copied. Save it where you can find it before sending.";
    } catch {
      returnUrl.focus?.();
      returnUrl.select();
      status.textContent = "Link selected. Copy it manually before sending. Anyone with this link may read the conversation.";
    }
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (busy || send.disabled || !form.reportValidity()) return;

    if (prepared) {
      // The only accepted POST is a user-triggered native top-level
      // navigation. It may commit even if the redirect subsequently fails.
      // The visitor already acknowledged saving the private return link.
      busy = true;
      update();
      status.textContent = "Sending to the private room. If navigation fails, check your saved link before trying again.";
      form.submit();
      return;
    }

    // An asynchronous ticket fetch must never submit later edits or consent.
    const intendedName = name.value;
    const intendedDraft = draft.value;
    busy = true;
    update();
    status.textContent = "Preparing your private return link; nothing has been sent.";
    try {
      const response = await fetch(origin + "/pages-handoff-ticket", {
        method: "GET", mode: "cors", credentials: "omit", cache: "no-store"
      });
      if (!response.ok) throw new Error("Ticket unavailable");
      const ticket = await response.json();
      if (!ticket ||
          !/^[A-Za-z0-9_-]{32,64}$/.test(ticket.csrf) ||
          !/^[A-Za-z0-9_-]{40,50}$/.test(ticket.initial_token) ||
          !/^[A-Za-z0-9_-]{24,64}$/.test(ticket.request_key)) {
        throw new Error("Invalid form ticket");
      }
      if (name.value !== intendedName || draft.value !== intendedDraft ||
          !consent.checked) {
        throw new Error("Draft or consent changed during preparation");
      }
      csrf.value = ticket.csrf;
      token.value = ticket.initial_token;
      requestKey.value = ticket.request_key;
      returnUrl.value = origin + "/t/" + ticket.initial_token;
      returnPanel.hidden = false;
      saved.checked = false;
      prepared = {name: intendedName, message: intendedDraft};
      status.textContent = "Your private return link is ready. Save it, check the acknowledgement, then select Send privately. Nothing has been sent yet.";
    } catch {
      clearPrepared();
      status.textContent = "Could not prepare the private link. Nothing was sent; copy your draft and open the private room instead.";
    } finally {
      busy = false;
      update();
    }
  });
  update();
})();
