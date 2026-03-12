const output = document.getElementById('output');

async function runAction(action) {
  const strategy = document.getElementById('strategy').value.trim();
  const timerange = document.getElementById('timerange').value.trim();
  const epochs = Number(document.getElementById('epochs').value || '20');

  output.textContent = `运行中: ${action} ...`;

  const resp = await fetch('/api/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action, strategy, timerange, epochs })
  });

  const data = await resp.json();
  if (!resp.ok) {
    output.textContent = `错误: ${JSON.stringify(data, null, 2)}`;
    return;
  }

  output.textContent = JSON.stringify(data, null, 2);
}

document.querySelectorAll('button[data-action]').forEach((btn) => {
  btn.addEventListener('click', () => runAction(btn.dataset.action));
});
