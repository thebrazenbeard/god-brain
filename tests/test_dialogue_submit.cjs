const {test} = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "../site/dialogue-submit.js"), "utf8");
const TICKET = {csrf: "c".repeat(43), initial_token: "t".repeat(43),
                request_key: "r".repeat(32)};

function browser(fetcher, embedded=false) {
  const elements = {};
  for (const id of ["dialogue-form", "sender-name", "draft-message",
                    "privacy-approval", "send-message", "send-status",
                    "csrf-value", "initial-token", "request-key", "return-link-panel",
                    "private-return-url", "copy-return-link", "return-link-saved"]) {
    elements[id] = {
      value: "", checked: false, disabled: true, textContent: "",
      callbacks: {}, posted: false,
      addEventListener(type, fn) { this.callbacks[type] = fn; },
      reportValidity() { return true; },
      select() { this.selected = true; },
      focus() { this.focused = true; },
      submit() { this.posted = true; }
    };
  }
  let calls = [];
  const clock = {now: 1_000_000};
  const BrowserDate = class extends Date {
    static now() { return clock.now; }
  };
  const windowEvents = {};
  const win = {addEventListener(type, fn) {windowEvents[type] = fn;}};
  win.self = win;
  win.top = embedded ? {} : win;
  const context = {
    window: win,
    navigator: {},
    Date: BrowserDate,
    performance: {now() { return clock.now; }},
    document: {getElementById: id => elements[id]},
    fetch: async (url, options) => {
      calls.push({url, options});
      return fetcher ? fetcher(url, options) : {ok: true, json: async () => TICKET};
    }
  };
  vm.runInNewContext(source, context, {timeout: 1000});
  return {elements, calls, windowEvents, clock};
}
function fill(els, consent=true) {
  els["sender-name"].value = "Visitor";
  els["draft-message"].value = "A real dialogue request";
  els["privacy-approval"].checked = consent;
  for (const id of ["sender-name", "draft-message", "privacy-approval"]) {
    els[id].callbacks.input?.();
    els[id].callbacks.change?.();
  }
}
const event = {preventDefault() {}};

test("cannot submit before consent or through passive page load", async () => {
  const b = browser();
  assert.equal(b.elements["send-message"].disabled, true);
  assert.equal(b.calls.length, 0);
  fill(b.elements, false);
  assert.equal(b.elements["send-message"].disabled, true);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.calls.length, 0);
  assert.equal(b.elements["dialogue-form"].posted, false);
});

test("prepares a recovery link but never POSTs until user saves it", async () => {
  const b = browser();
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.calls.length, 1);
  assert.equal(b.calls[0].url,
    "https://lappy.tail86ea75.ts.net:10000/pages-handoff-ticket");
  assert.equal(b.calls[0].options.credentials, "omit");
  assert.equal(b.elements["dialogue-form"].posted, false);
  assert.equal(b.elements["return-link-panel"].hidden, false);
  assert.equal(b.elements["private-return-url"].focused, true,
               "Newly revealed link receives keyboard focus");
  assert.equal(b.elements["private-return-url"].value,
    "https://lappy.tail86ea75.ts.net:10000/t/" + TICKET.initial_token);
  assert.equal(b.elements["send-message"].disabled, true);
  b.elements["return-link-saved"].checked = true;
  b.elements["return-link-saved"].callbacks.change();
  assert.equal(b.elements["send-message"].disabled, false);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.calls.length, 1);
  assert.equal(b.elements["dialogue-form"].posted, true);
  assert.equal(b.elements["csrf-value"].value, TICKET.csrf);
  assert.equal(b.elements["initial-token"].value, TICKET.initial_token);
  assert.equal(b.elements["request-key"].value, TICKET.request_key);
});

test("framed Pages cannot enable direct submit even with consent", async () => {
  const b = browser(undefined, true);
  fill(b.elements);
  assert.equal(b.elements["send-message"].disabled, true);
  assert.equal(b.calls.length, 0);
  assert.equal(b.elements["dialogue-form"].posted, false);
  assert.match(b.elements["send-status"].textContent, /embedded/i);
});

test("changing a prepared message invalidates its private link ticket", async () => {
  const b = browser();
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  b.elements["return-link-saved"].checked = true;
  b.elements["return-link-saved"].callbacks.change();
  b.elements["draft-message"].value = "Changed after preparation";
  b.elements["draft-message"].callbacks.input();
  assert.equal(b.elements["return-link-panel"].hidden, true);
  assert.equal(b.elements["initial-token"].value, "");
  assert.equal(b.elements["send-message"].disabled, false);
  assert.equal(b.elements["dialogue-form"].posted, false);
});

test("ticket errors never send or destroy the local draft", async () => {
  const b = browser(async () => {throw new Error("Network unavailable");});
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.elements["dialogue-form"].posted, false);
  assert.equal(b.elements["draft-message"].value, "A real dialogue request");
  assert.match(b.elements["send-status"].textContent, /nothing was sent/i);
  assert.equal(b.elements["send-message"].disabled, false);
});

test("malformed ticket cannot cause a POST", async () => {
  const b = browser(async () => ({ok: true, json: async () => ({csrf: "x"})}));
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.elements["dialogue-form"].posted, false);
  assert.match(b.elements["send-status"].textContent, /nothing was sent/i);
});
test("editing the message during ticket retrieval aborts the old submission", async () => {
  let releaseTicket;
  const b = browser(async () => new Promise(resolve => { releaseTicket = resolve; }));
  fill(b.elements);
  const pending = b.elements["dialogue-form"].callbacks.submit(event);
  b.elements["draft-message"].value = "This is not the version I submitted";
  releaseTicket({ok: true, json: async () => TICKET});
  await pending;
  assert.equal(b.elements["dialogue-form"].posted, false);
  assert.equal(b.elements["draft-message"].value,
               "This is not the version I submitted");
  assert.match(b.elements["send-status"].textContent, /nothing was sent/i);
});

test("native submission stays latched after prepared link is confirmed", async () => {
  const b = browser();
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  b.elements["return-link-saved"].checked = true;
  b.elements["return-link-saved"].callbacks.change();
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.elements["dialogue-form"].posted, true);
  assert.equal(b.elements["send-message"].disabled, true);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.calls.length, 1, "Only one anonymous ticket may be requested");
});

test("return link copy is never automatic and manual fallback works", async () => {
  const b = browser();
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.elements["private-return-url"].selected, undefined);
  await b.elements["copy-return-link"].callbacks.click();
  assert.equal(b.elements["private-return-url"].selected, true);
});

test("BFCache return preserves draft but clears old ticket and consent", async () => {
  const b = browser();
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  b.elements["return-link-saved"].checked = true;
  b.elements["return-link-saved"].callbacks.change();
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.elements["dialogue-form"].posted, true);
  assert.equal(b.elements["send-message"].disabled, true);
  assert.equal(typeof b.windowEvents.pageshow, "function");
  b.windowEvents.pageshow({persisted: true});
  assert.equal(b.elements["privacy-approval"].checked, false);
  assert.equal(b.elements["csrf-value"].value, "");
  assert.equal(b.elements["initial-token"].value, "");
  assert.equal(b.elements["request-key"].value, "");
  assert.equal(b.elements["return-link-panel"].hidden, true);
  assert.equal(b.elements["private-return-url"].value, "");
  assert.equal(b.elements["send-message"].disabled, true);
  assert.match(b.elements["send-status"].textContent, /may already have been sent/i);
  assert.equal(b.elements["draft-message"].value, "A real dialogue request");
  b.elements["privacy-approval"].checked = true;
  b.elements["privacy-approval"].callbacks.change();
  assert.equal(b.elements["send-message"].disabled, false);
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.calls.length, 2);
  assert.equal(b.elements["dialogue-form"].posted, true);
  assert.equal(b.elements["send-message"].disabled, true,
               "Another acknowledgement is required before another POST");
  b.elements["return-link-saved"].checked = true;
  b.elements["return-link-saved"].callbacks.change();
  assert.equal(b.elements["send-message"].disabled, false);
});

test("an aged prepared ticket cannot POST without fresh preparation", async () => {
  const b = browser();
  fill(b.elements);
  await b.elements["dialogue-form"].callbacks.submit(event);
  b.elements["return-link-saved"].checked = true;
  b.elements["return-link-saved"].callbacks.change();
  b.clock.now += 11 * 60 * 1000;
  await b.elements["dialogue-form"].callbacks.submit(event);
  assert.equal(b.elements["dialogue-form"].posted, false);
  assert.equal(b.elements["return-link-panel"].hidden, true);
  assert.equal(b.elements["initial-token"].value, "");
  assert.equal(b.elements["send-message"].focused, true,
               "Expired preflight returns focus to visible Prepare button");
  assert.equal(b.calls.length, 1, "No automatic second ticket or POST");
  assert.match(b.elements["send-status"].textContent, /prepare a new|too old/i);
});
