const DEFAULTS = {
  baseUrl: 'http://127.0.0.1:8000',
  defaultTags: 'web,clip',
};

const PROMPT_TEMPLATES = [
  { name: 'Summarize tightly', text: 'Summarize the following text in 3 bullets. Be faithful and specific:\n\n' },
  { name: 'Extract actions', text: 'Extract clear next actions with owners and due dates if present:\n\n' },
  { name: 'Prompt Goddess seed', text: 'Draft a staged prompt (Observe, Orient, Decide, Act) using this context:\n\n' },
  { name: 'Pantheon archetype card', text: 'Generate an archetype card (name, type, RA/Dec if any, tags, domain, symbols, lore, traits, core prompt) from:\n\n' },
  { name: 'Cosmic Duality brief', text: 'Two-column TEC infographic: Left Unseen (Entropy & Kaznak), Right Manifest (Lumina, EMC, Ferron, Cela). Central lensing seam; portraits, sigils, attributes, heterochromia callouts; deep-space cathedral, glass floor interference; palette-locked, high-contrast.\n\n' },
];

function $(id){ return document.getElementById(id); }

async function getActiveSelection() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) return '';
    const [{ result }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection()?.toString() || ''
    });
    return result || '';
  } catch (e) { return ''; }
}

async function loadSettings() {
  return new Promise(resolve => {
    chrome.storage.sync.get(['baseUrl', 'defaultTags'], (data) => {
      resolve({
        baseUrl: data.baseUrl || DEFAULTS.baseUrl,
        defaultTags: data.defaultTags || DEFAULTS.defaultTags,
      });
    });
  });
}

function renderPromptHelper() {
  const wrap = $('prompts');
  wrap.innerHTML = '';
  PROMPT_TEMPLATES.forEach(p => {
    const span = document.createElement('span');
    span.className = 'pill';
    span.textContent = p.name;
    span.addEventListener('click', () => {
      const t = $('content');
      t.value = p.text + (t.value || '');
      t.focus();
    });
    wrap.appendChild(span);
  });
}

async function saveMemory({ baseUrl, tags, content, note }) {
  const url = baseUrl.replace(/\/$/, '') + '/memory';
  const payload = {
    tags: (tags || '').split(',').map(s => s.trim()).filter(Boolean),
    content: content || '',
    metadata: {
      note: note || '',
      source: 'edge-extension',
      page: await getActivePageMeta(),
    },
  };
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  return await res.json();
}

async function getActivePageMeta() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return { title: tab?.title || '', url: tab?.url || '' };
  } catch { return { title: '', url: '' }; }
}

document.addEventListener('DOMContentLoaded', async () => {
  renderPromptHelper();
  const settings = await loadSettings();
  $('tags').value = settings.defaultTags;
  const sel = await getActiveSelection();
  $('content').value = sel || '';
  $('save').addEventListener('click', async () => {
    $('status').textContent = 'Saving…'; $('status').className = 'small';
    try {
      const out = await saveMemory({
        baseUrl: settings.baseUrl,
        tags: $('tags').value,
        content: $('content').value,
        note: $('note').value,
      });
      $('status').textContent = 'Saved ' + out.id; $('status').className = 'small ok';
    } catch (e) {
      $('status').textContent = 'Error: ' + (e.message || e.toString()); $('status').className = 'small err';
    }
  });
});
