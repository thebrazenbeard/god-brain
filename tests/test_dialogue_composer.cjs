const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const {test} = require("node:test");

const source = fs.readFileSync(path.join(__dirname, "../site/dialogue.js"), "utf8");

function browser(clipboard) {
  const elements = {};
  const ids = ["draft-message", "draft-count", "copy-draft", "draft-status"];
  for (const id of ids) {
    elements[id] = {
      value: "", disabled: true, textContent: "",
      callbacks: {}, focused: false, selected: false,
      addEventListener(type, fn) { this.callbacks[type] = fn; },
      focus() { this.focused = true; },
      select() { this.selected = true; }
    };
  }
  vm.runInNewContext(source, {
    document: {getElementById: id => elements[id]},
    navigator: clipboard ? {clipboard} : {}
  }, {timeout: 1000});
  return elements;
}

test("draft stays local; copy only happens on explicit click", async () => {
  let captured = null;
  const els = browser({writeText: async value => { captured = value; }});
  const draft = els["draft-message"], copy = els["copy-draft"];
  assert.equal(copy.disabled, true);
  assert.equal(els["draft-count"].textContent, "0 / 2000");
  draft.value = "   ";
  draft.callbacks.input();
  assert.equal(copy.disabled, true);
  draft.value = "Hello, world!";
  draft.callbacks.input();
  assert.equal(copy.disabled, false);
  assert.equal(els["draft-count"].textContent, "13 / 2000");
  assert.equal(captured, null);
  await copy.callbacks.click();
  assert.equal(captured, "Hello, world!");
  assert.match(els["draft-status"].textContent, /copied/i);
  assert.match(els["draft-status"].textContent, /paste/i);
});

test("clipboard unavailable selects draft for manual copy", async () => {
  const els = browser(null);
  els["draft-message"].value = "Do not send automatically";
  els["draft-message"].callbacks.input();
  await els["copy-draft"].callbacks.click();
  assert.equal(els["draft-message"].focused, true);
  assert.equal(els["draft-message"].selected, true);
  assert.match(els["draft-status"].textContent, /manually/i);
});

test("clipboard rejected still preserves draft and gives manual fallback", async () => {
  const els = browser({writeText: async () => { throw new Error("Denied"); }});
  els["draft-message"].value = "Message is private";
  els["draft-message"].callbacks.input();
  await els["copy-draft"].callbacks.click();
  assert.equal(els["draft-message"].value, "Message is private");
  assert.equal(els["draft-message"].selected, true);
});
