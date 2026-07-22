let rowCount = 3;

/*
function index(){

}
*/
function botao_select(){
  const botao = document.querySelector("div-btn");
  if(botao.classList.contains("active")){
    console.log(botao.textContent.trim())
  }
}


// Identificar quais botão foram apertado (DIVISÃO)
function toggle(botao){
      botao.classList.toggle("selecionado");
    }


// Identificar quais botão foram apertado  (Urgência)

function Identificacao(){
  const solicitante = document.getElementById("solicitante").value;
  const departamento = document.getElementById("departamento").value;
  const centro_custo = document.getElementById("centro_custo").value;
  const data = document.getElementById("data").value;
  const justificativa = document.getElementById("solicitante").value;

}

// Itens solicitados

function itens(){
  // Coletando os itens
  const item1 = document.getElementById("item1").value;
  const item2 = document.getElementById("item2").value;
  const item3 = document.getElementById("item3").value;
  // Unidades(sistema de medidas)
  

  // Quantidade
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
