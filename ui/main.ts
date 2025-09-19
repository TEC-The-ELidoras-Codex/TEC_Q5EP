const form = document.getElementById('captureForm') as HTMLFormElement | null;
const statusEl = document.getElementById('status') as HTMLElement | null;
const gpsBtn = document.getElementById('gpsBtn') as HTMLButtonElement | null;
const runsUl = document.getElementById('runs') as HTMLUListElement | null;

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const photoInput = document.getElementById('photo') as HTMLInputElement | null;
  const noteInput = document.getElementById('note') as HTMLTextAreaElement | null;
  const tagsInput = document.getElementById('tags') as HTMLInputElement | null;
  const consentInput = document.getElementById('consent') as HTMLInputElement | null;
  const gpsHidden = document.getElementById('gps') as HTMLInputElement | null;

  const photo = photoInput?.files?.[0];
  const note = noteInput?.value || '';
  const tags = tagsInput?.value || '';
  const consent = consentInput?.checked ? 'true' : 'false';
  const gps = gpsHidden?.value || '';

  const fd = new FormData();
  if (photo) fd.append('photo', photo);
  fd.append('note', note);
  fd.append('timestamp', new Date().toISOString());
  fd.append('tags', tags);
  fd.append('consent', consent);
  fd.append('gps', gps);

  try {
    const res = await fetch('http://localhost:8000/submit', { method: 'POST', body: fd });
    const text = await res.text();
    if (statusEl) statusEl.textContent = text;
    await loadRuns();
  } catch (err) {
    if (statusEl) statusEl.textContent = String(err);
  }
});

gpsBtn?.addEventListener('click', async () => {
  const gpsHidden = document.getElementById('gps') as HTMLInputElement | null;
  if (!navigator.geolocation) {
    if (statusEl) statusEl.textContent = 'Geolocation not available.';
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const payload = {
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
        accuracy: pos.coords.accuracy,
      };
      if (gpsHidden) gpsHidden.value = JSON.stringify(payload);
      if (statusEl) statusEl.textContent = 'GPS attached.';
    },
    (err) => {
      if (statusEl) statusEl.textContent = 'GPS error: ' + err.message;
    }
  );
});

async function loadRuns() {
  try {
    const res = await fetch('http://localhost:8000/runs');
    const items = await res.json();
    if (!runsUl) return;
    runsUl.innerHTML = '';
    for (const it of items) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `http://localhost:8000/pack/${it.id}`;
      a.textContent = `${it.id} — ${it.timestamp} — tags: ${it.tags?.join(', ') || '-'}`;
      li.appendChild(a);
      runsUl.appendChild(li);
    }
  } catch (e) {
    // ignore
  }
}

loadRuns();
