async function api(path, opts){
  const res = await fetch(path, Object.assign({headers:{'Content-Type':'application/json'}}, opts));
  if (res.status===204) return null;
  return res.json();
}

function el(q){return document.querySelector(q)}

async function load(){
  const items = await api('/api/items');
  const tbody = el('#items-table tbody');
  tbody.innerHTML='';
  items.forEach(it=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${it.id}</td><td>${it.name}</td><td>${it.quantity}</td><td>${it.price.toFixed(2)}</td><td><button data-id="${it.id}" class="sel">Select</button></td>`;
    tbody.appendChild(tr);
  });
  Array.from(document.querySelectorAll('.sel')).forEach(b=>b.addEventListener('click', e=>{
    const id = e.currentTarget.dataset.id; selectItem(id)
  }));
}

function setStatus(t){el('#status').textContent = t}

async function selectItem(id){
  const items = await api('/api/items');
  const it = items.find(x=>x.id==id);
  if(!it) return;
  el('#name').value = it.name;
  el('#quantity').value = it.quantity;
  el('#price').value = it.price;
  el('#status').dataset.selected = id;
}

el('#add').addEventListener('click', async ()=>{
  const name = el('#name').value; const quantity = el('#quantity').value; const price = el('#price').value;
  const res = await api('/api/items',{method:'POST',body:JSON.stringify({name,quantity,price})});
  if(res && res.error) return setStatus(res.error);
  setStatus('Added.'); load();
});

el('#update').addEventListener('click', async ()=>{
  const id = el('#status').dataset.selected; if(!id) return setStatus('Select an item first');
  const name = el('#name').value; const quantity = el('#quantity').value; const price = el('#price').value;
  const res = await api('/api/items/'+id,{method:'PUT',body:JSON.stringify({name,quantity,price})});
  if(res && res.error) return setStatus(res.error);
  setStatus('Updated.'); load();
});

el('#delete').addEventListener('click', async ()=>{
  const id = el('#status').dataset.selected; if(!id) return setStatus('Select an item first');
  if(!confirm('Delete item?')) return;
  const res = await api('/api/items/'+id,{method:'DELETE'});
  setStatus('Deleted.'); load();
});

el('#refresh').addEventListener('click', load);

load();
