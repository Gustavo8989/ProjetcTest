let rowCount = 3;

/*
function index(){

}
*/


function toggle(el) {
      el.classList.toggle('active');
    }

function urgencia(el, level) {
      document.querySelectorAll('.urgencia-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
    }
function addRow() {
      rowCount++;
      const tbody = document.getElementById('items-body');
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="num">${rowCount}</td>
        <td><input type="text" placeholder="Descrição do item" /></td>
        <td><input type="text" placeholder="Un, Kg…" /></td>
        <td><input type="number" placeholder="0" min="0" /></td>
      `;
      tbody.appendChild(tr);
    }
function submitForm() {
      const banner = document.getElementById('success');
      banner.style.display = 'flex';
      setTimeout(() => { banner.style.display = 'none'; }, 4000);
    }