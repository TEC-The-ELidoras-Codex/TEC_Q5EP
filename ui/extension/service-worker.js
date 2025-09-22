const MENU_ID = 'tec-memory-clip';

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({ id: MENU_ID, title: 'Save selection to TEC Memory', contexts: ['selection'] });
});

async function getSettings() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['baseUrl', 'defaultTags'], (d) => resolve({ baseUrl: d.baseUrl || 'http://127.0.0.1:8000', defaultTags: d.defaultTags || 'web,clip' }));
  });
}

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== MENU_ID) return;
  const settings = await getSettings();
  const tags = settings.defaultTags.split(',').map(s => s.trim()).filter(Boolean);
  const content = info.selectionText || '';
  const meta = { note: 'context-menu', source: 'edge-extension', page: { title: tab?.title || '', url: info.pageUrl || '' } };
  try {
    const res = await fetch(settings.baseUrl.replace(/\/$/, '') + '/memory', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ tags, content, metadata: meta }) });
    if (!res.ok) throw new Error('HTTP ' + res.status);
  } catch (e) {
    console.error('Failed to save selection:', e);
  }
});
