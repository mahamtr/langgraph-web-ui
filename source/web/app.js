const form = document.getElementById('form');
const input = document.getElementById('input');
const log = document.getElementById('log');

function addBubble(text, cls){
  const d = document.createElement('div');
  d.className = 'bubble ' + cls;
  d.textContent = text;
  log.appendChild(d);
  window.scrollTo(0, document.body.scrollHeight);
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if(!text) return;
  addBubble(text, 'user');
  input.value='';

  try{
    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ messages: [{ role: 'user', content: text }] })
    });
    const data = await res.json();
    addBubble(data.reply || JSON.stringify(data), 'agent');
  }catch(err){
    addBubble('Error contacting agent: '+err.message, 'agent');
  }
});
