export async function fetchDocuments() {
  const res = await fetch('/documents');
  const files = await res.json();
  const container = document.getElementById('document-list');
  container.innerHTML = ''; // Clear existing list

  files.forEach(file => {
    const item = document.createElement('div');
    item.className = 'doc-item';

    const name = document.createElement('span');
    name.className = 'file-name';
    name.textContent = file;
    const spacer = document.createElement('div');
    spacer.style.flex = '1'; // This pushes the buttons to the right

    const delBtn = document.createElement('span');
    delBtn.className = 'delete-btn';
    delBtn.textContent = '🗑️';
    delBtn.onclick = () => deleteDocument(file);

    const addBtn = document.createElement('span');
    addBtn.className = 'add-btn';
    addBtn.textContent = '➕'; // Or use "Add to Context"
    addBtn.onclick = () => addToContext(file);

    item.appendChild(name);    
    item.appendChild(spacer);
    item.appendChild(addBtn);
    item.appendChild(delBtn);
    container.appendChild(item);
  });
}

export async function deleteDocument(filename) {
      if (!confirm(`Delete "${filename}"?`)) return;
      const res = await fetch(`/documents/${filename}`, { method: 'DELETE' });
      if (res.ok) {
        fetchDocuments();  // Reload list
      } else {
        alert('Error deleting file');
      }
    }

    // On load


async function addToContext(filename) {
  const res = await fetch('/add-to-context', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filename })
  });

  if (res.ok) {
    alert(`${filename} added to context!`);
  } else {
    alert(`Failed to add ${filename} to context.`);
  }
}

