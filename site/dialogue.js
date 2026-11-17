/* Browser-only draft helper. No network, storage, credentials or messaging. */
(() => {
  "use strict";
  const draft = document.getElementById("draft-message");
  const count = document.getElementById("draft-count");
  const copy = document.getElementById("copy-draft");
  const status = document.getElementById("draft-status");
  if (!draft || !count || !copy || !status) return;

  const refresh = () => {
    count.textContent = draft.value.length + " / 2000";
    copy.disabled = !draft.value.trim();
    status.textContent = "Draft only. Nothing has been sent.";
  };
  const manualCopy = () => {
    draft.focus();
    draft.select();
    status.textContent = "Clipboard unavailable. Copy the selected text manually, then paste in the private room.";
  };

  draft.addEventListener("input", refresh);
  copy.addEventListener("click", async () => {
    if (!draft.value.trim()) return;
    if (!navigator.clipboard || typeof navigator.clipboard.writeText !== "function") {
      manualCopy();
      return;
    }
    try {
      await navigator.clipboard.writeText(draft.value);
      status.textContent = "Copied. Open the private room, paste the draft, and submit it there.";
    } catch {
      manualCopy();
    }
  });
  refresh();
})();
