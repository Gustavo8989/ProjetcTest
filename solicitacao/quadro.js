const board = document.getElementById('board');

function createCardElement(text) {
  const card = document.createElement('div');
  card.className = 'card';
  card.draggable = true;
  card.innerHTML = `<p></p><button class="remove-card" title="Remover card">&times;</button>`;
  card.querySelector('p').textContent = text;
  attachCardEvents(card);
  return card;
}

function attachCardEvents(card) {
  card.addEventListener('dragstart', () => {
    card.classList.add('dragging');
  });
  card.addEventListener('dragend', () => {
    card.classList.remove('dragging');
    updateAllCounts();
  });
  card.querySelector('.remove-card').addEventListener('click', () => {
    card.remove();
    updateAllCounts();
  });
}

function updateAllCounts() {
  document.querySelectorAll('.column').forEach(col => {
    const list = col.querySelector('.card-list');
    const count = list.querySelectorAll('.card').length;
    col.querySelector('.count').textContent = count;
  });
}

function getDragAfterElement(list, y) {
  const cards = [...list.querySelectorAll('.card:not(.dragging)')];
  return cards.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// Drag and drop entre colunas
document.querySelectorAll('.card-list').forEach(list => {
  list.addEventListener('dragover', e => {
    e.preventDefault();
    const column = list.closest('.column');
    column.classList.add('drag-over');
    const dragging = document.querySelector('.dragging');
    const afterElement = getDragAfterElement(list, e.clientY);
    if (!dragging) return;
    if (afterElement == null) {
      list.appendChild(dragging);
    } else {
      list.insertBefore(dragging, afterElement);
    }
  });

  list.addEventListener('dragleave', e => {
    if (!list.contains(e.relatedTarget)) {
      list.closest('.column').classList.remove('drag-over');
    }
  });

  list.addEventListener('drop', () => {
    list.closest('.column').classList.remove('drag-over');
  });
});

// Cards existentes
document.querySelectorAll('.card').forEach(attachCardEvents);

// Formulário de adicionar card
document.querySelectorAll('.column').forEach(col => {
  const addBtn = col.querySelector('.btn-add-card');
  const form = col.querySelector('.add-card-form');
  const textarea = form.querySelector('textarea');
  const confirmBtn = form.querySelector('.btn-confirm');
  const cancelBtn = form.querySelector('.btn-cancel');
  const list = col.querySelector('.card-list');

  addBtn.addEventListener('click', () => {
    addBtn.classList.add('hidden');
    form.classList.add('active');
    textarea.focus();
  });

  function closeForm() {
    form.classList.remove('active');
    addBtn.classList.remove('hidden');
    textarea.value = '';
  }

  cancelBtn.addEventListener('click', closeForm);

  confirmBtn.addEventListener('click', () => {
    const text = textarea.value.trim();
    if (text) {
      list.appendChild(createCardElement(text));
      updateAllCounts();
    }
    closeForm();
  });

  textarea.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      confirmBtn.click();
    }
    if (e.key === 'Escape') {
      closeForm();
    }
  });
});

updateAllCounts();
