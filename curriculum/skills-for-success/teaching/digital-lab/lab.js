'use strict';
(() => {
  const KEY = 'access-is4s-digital-practice-v1';
  const topics = ['Material flow', 'Equipment purposes', 'Road users'];
  const labels = { recipient: { reviewer: 'Class reviewer', class: 'Whole class', public: 'Anyone with a link' }, access: { view: 'View', comment: 'Comment', edit: 'Edit' } };
  const el = id => document.getElementById(id);
  let records = [], preview = null, dirty = false;
  const sourceRows = () => [{ prepared: 8, checked: 5 }, { prepared: 6, checked: 4 }, { prepared: 10, checked: 7 }];
  function node(tag, value, parent) { const n = document.createElement(tag); if (value !== undefined) n.textContent = value; if (parent) parent.append(n); return n; }
  function validRecord(r) {
    return r && Number.isSafeInteger(r.version) && r.version > 0 && typeof r.savedAt === 'string' && !Number.isNaN(Date.parse(r.savedAt)) &&
      typeof r.alias === 'string' && r.alias.length <= 32 && typeof r.title === 'string' && r.title.length <= 80 &&
      typeof r.note === 'string' && r.note.length <= 500 && typeof r.reason === 'string' && r.reason.length <= 700 &&
      Object.hasOwn(labels.recipient, r.recipient) && Object.hasOwn(labels.access, r.access) && typeof r.includePhone === 'boolean' &&
      Array.isArray(r.rows) && r.rows.length === 3 && r.rows.every(row => Number.isInteger(row.prepared) && Number.isInteger(row.checked) && row.prepared >= 0 && row.prepared <= 999 && row.checked >= 0 && row.checked <= row.prepared);
  }
  function storageMessage(message) { el('storage-note').textContent = message; el('storage-note').hidden = false; }
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const saved = JSON.parse(raw);
      if (Array.isArray(saved) && saved.length <= 10 && saved.every(validRecord)) records = saved;
      else storageMessage('The saved practice data could not be read. Your existing browser entry has not been removed. Download any needed evidence from another saved copy, then reset this practice desk.');
    }
  } catch (_) { storageMessage('Browser saving is unavailable or the saved practice record could not be read. You can still practise and download a record.'); }
  function buildRows(rows) {
    el('count-rows').replaceChildren();
    rows.forEach((row, i) => {
      const tr = node('tr', undefined, el('count-rows')); const th = node('th', topics[i], tr); th.scope = 'row';
      ['prepared', 'checked'].forEach(key => { const td = node('td', undefined, tr); const input = node('input', undefined, td); input.type = 'number'; input.min = '0'; input.max = '999'; input.step = '1'; input.required = true; input.value = String(row[key]); input.id = `${key}-${i}`; input.setAttribute('aria-label', `${topics[i]} ${key}`); input.addEventListener('input', () => { updateTotals(); markDirty(); }); });
      const td = node('td', undefined, tr); const output = node('output', '', td); output.id = `remaining-${i}`;
    });
    updateTotals();
  }
  function readRows() { return topics.map((_, i) => ({ prepared: el(`prepared-${i}`).value === '' ? NaN : Number(el(`prepared-${i}`).value), checked: el(`checked-${i}`).value === '' ? NaN : Number(el(`checked-${i}`).value) })); }
  function updateTotals() {
    const rows = readRows(); let valid = true, prepared = 0, checked = 0;
    rows.forEach((r, i) => { const okay = Number.isInteger(r.prepared) && Number.isInteger(r.checked) && r.prepared >= 0 && r.prepared <= 999 && r.checked >= 0 && r.checked <= r.prepared;
      el(`remaining-${i}`).textContent = okay ? String(r.prepared - r.checked) : 'Check row'; valid = valid && okay; prepared += r.prepared; checked += r.checked;
    });
    el('count-error').hidden = valid; el('count-error').textContent = valid ? '' : 'Use whole numbers from 0 to 999. Checked sets cannot exceed prepared sets. Check each row before previewing.';
    el('total-prepared').textContent = valid ? prepared : '—'; el('total-checked').textContent = valid ? checked : '—'; el('total-remaining').textContent = valid ? prepared - checked : '—';
    el('equation').textContent = valid ? `${prepared} prepared − ${checked} checked = ${prepared - checked} remaining.` : 'Resolve the highlighted count issue to calculate a total.';
    return valid;
  }
  function markDirty() { dirty = true; if (preview) { el('preview-state').textContent = 'The form has changed since this preview. Preview again before saving or downloading.'; el('save-button').disabled = true; el('download-button').disabled = true; } }
  function current() { return { alias: el('alias').value.trim(), title: el('title').value.trim(), rows: readRows(), includePhone: el('include-phone').checked, recipient: el('recipient').value, access: el('access').value, note: el('note').value.trim(), reason: el('reason').value.trim() }; }
  function validate() {
    el('form-error').hidden = true;
    const validCounts = updateTotals();
    if (!el('practice-form').checkValidity() || !validCounts || !el('alias').value.trim() || !el('title').value.trim()) {
      el('form-error').textContent = 'Check the alias, title and counts. Complete required fields using only fictional information.'; el('form-error').hidden = false;
      el('practice-form').reportValidity();
      if (!validCounts) el('prepared-0').focus();
      return false;
    }
    return true;
  }
  function renderPreview(r, focus = true) {
    preview = JSON.parse(JSON.stringify(r)); dirty = false;
    el('preview-empty').hidden = true; el('preview-content').hidden = false;
    el('copy-title').textContent = r.title; el('copy-alias').textContent = r.alias; el('copy-recipient').textContent = labels.recipient[r.recipient]; el('copy-access').textContent = labels.access[r.access];
    el('copy-note').textContent = r.note || 'No reviewer note entered.'; el('copy-reason').textContent = r.reason || 'No reason recorded yet. Discuss the choices with the observer.';
    el('copy-table').replaceChildren(); const table = node('table', undefined, el('copy-table')); node('caption', 'Fictional classroom data — review copy', table); const head = node('thead', undefined, table), hr = node('tr', undefined, head);
    const headings = ['Topic','Prepared','Checked','Remaining']; if (r.includePhone) headings.push('Personal phone · dummy');
    headings.forEach(h => { const th = node('th', h, hr); th.scope = 'col'; }); const body = node('tbody', undefined, table);
    r.rows.forEach((row, i) => { const tr = node('tr', undefined, body); const th = node('th', topics[i], tr); th.scope = 'row'; [row.prepared,row.checked,row.prepared-row.checked].forEach(v => node('td', String(v), tr)); if (r.includePhone) node('td','sample only',tr); });
    const foot=node('tfoot',undefined,table),fr=node('tr',undefined,foot),th=node('th','Total',fr); th.scope='row'; const sum=r.rows.reduce((s,row)=>({p:s.p+row.prepared,c:s.c+row.checked}),{p:0,c:0}); [sum.p,sum.c,sum.p-sum.c].forEach(v=>node('td',String(v),fr));if(r.includePhone)node('td','—',fr);
    el('copy-dummy-note').textContent = r.includePhone ? 'This copy includes the dummy personal phone column. Check whether it serves the reviewer’s task.' : 'This copy excludes the dummy personal phone column. Check the remaining information against the task.';
    el('preview-state').textContent = r.version ? `Loaded saved version ${String(r.version).padStart(2,'0')}. Inspect the form and make a fresh preview after any change.` : 'Preview matches the current form. Check its facts and choices before saving.';
    el('save-button').disabled = false; el('download-button').disabled = false; if (focus) el('preview-title').focus();
  }
  function load(r) { el('alias').value=r.alias;el('title').value=r.title;el('include-phone').checked=r.includePhone;el('recipient').value=r.recipient;el('access').value=r.access;el('note').value=r.note;el('reason').value=r.reason;buildRows(r.rows);renderPreview(r);el('status').textContent=`Opened local version ${r.version}.`; }
  function renderVersions() {
    el('version-list').replaceChildren(); el('no-versions').hidden = records.length > 0;
    [...records].reverse().forEach(r => {const li=node('li',undefined,el('version-list'));const span=node('span',`Version ${String(r.version).padStart(2,'0')} · ${r.title}`,li);node('small',`${r.alias} · ${new Date(r.savedAt).toLocaleString()}`,span);const button=node('button','Open',li);button.type='button';button.setAttribute('aria-label',`Open version ${r.version}`);button.addEventListener('click',()=>load(r));});
  }
  function save() {
    if (!preview || dirty) return;
    const version = records.reduce((n,r)=>Math.max(n,r.version),0)+1;
    const r = {...preview,version,savedAt:new Date().toISOString()};const next=[...records,r].slice(-10);
    try { localStorage.setItem(KEY,JSON.stringify(next));records=next;renderVersions();renderPreview(r,false);el('status').textContent=`Saved local version ${String(version).padStart(2,'0')}. The latest ten versions are retained on this browser.`; }
    catch (_) { storageMessage('This browser could not save the version. Use Download this practice record to keep a copy. No saved version is being claimed.');el('status').textContent='Local save did not complete. Download the practice record instead.'; }
  }
  function download() {
    if (!preview || dirty) return;
    const r={schema:'access-is4s-local-practice-1',simulation:true,evidence_scope:'Local form/version/copy actions only. Online permission-setting not established.',...preview,exportedAt:new Date().toISOString()};
    const url=URL.createObjectURL(new Blob([JSON.stringify(r,null,2)+'\n'],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`is4s-review-${preview.alias.replace(/[^a-zA-Z0-9_-]/g,'-')||'practice'}-${preview.version ? `v${String(preview.version).padStart(2,'0')}` : 'draft'}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);el('status').textContent='Download prepared. Check your browser’s download location to confirm the file.';
  }
  function reset() {
    try { localStorage.removeItem(KEY); }
    catch (_) { storageMessage('The browser would not clear its saved entry. The visible form has been reset, but browser storage may still contain earlier practice. Use the browser’s site-data controls with your instructor if needed.'); }
    records=[];preview=null;dirty=false;el('practice-form').reset();buildRows(sourceRows());renderVersions();el('preview-content').hidden=true;el('preview-empty').hidden=false;el('form-error').hidden=true;el('status').textContent='Practice desk reset to the fictional starting counts.';el('reset-dialog').close();el('alias').focus();
  }
  el('practice-form').addEventListener('submit',e=>{e.preventDefault();if(validate())renderPreview(current());});
  el('practice-form').addEventListener('input',markDirty);el('practice-form').addEventListener('change',markDirty);
  el('preview-button').addEventListener('click',()=>{if(validate())renderPreview(current());});el('save-button').addEventListener('click',save);el('download-button').addEventListener('click',download);el('edit-button').addEventListener('click',()=>el('include-phone').focus());
  el('reset-button').addEventListener('click',()=>el('reset-dialog').showModal());el('cancel-reset').addEventListener('click',()=>el('reset-dialog').close());el('confirm-reset').addEventListener('click',reset);
  buildRows(sourceRows());renderVersions();
})();
