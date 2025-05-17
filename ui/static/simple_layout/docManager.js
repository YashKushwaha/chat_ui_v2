async function fetchDocuments() {
      const res = await fetch('/documents');
      const files = await res.json();
      const container = document.getElementById('document-list');
      container.innerHTML = '';  // Clear existing list

      files.forEach(file => {
        const item = document.createElement('div');
        item.className = 'doc-item';

        const name = document.createElement('span');
        name.textContent = file;

        const delBtn = document.createElement('span');
        delBtn.className = 'delete-btn';
        delBtn.textContent = '🗑️';
        delBtn.onclick = () => deleteDocument(file);

        item.appendChild(name);
        item.appendChild(delBtn);
        container.appendChild(item);
      });
    }

    async function deleteDocument(filename) {
      if (!confirm(`Delete "${filename}"?`)) return;
      const res = await fetch(`/documents/${filename}`, { method: 'DELETE' });
      if (res.ok) {
        fetchDocuments();  // Reload list
      } else {
        alert('Error deleting file');
      }
    }

    // On load
    fetchDocuments();