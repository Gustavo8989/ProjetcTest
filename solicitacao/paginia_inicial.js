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

function get_dados(){
  const dados = {
  solicitante = document.getElementById("solicitante").value,
  departamento = document.getElementById("departamento").value,
  centro_custo = document.getElementById("centro_custo").value,
  data = document.getElementById("data").value,
  justificativa = document.getElementById("solicitante").value,
  item1 = document.getElementById("item1").value,
  item2 = document.getElementById("item2").value,
  item3 = document.getElementById("item3").value,
  item_a_mais = document.getElementById("mais_item").value,

  }
  // Mandando informações para o servidor
    fetch("/salvar",{
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(resultado => {
      console.log(resultado)
      alert("Dados enviado com sucesso!! ");
    })
    .catch(erro =>{
      console.erro("Erro:", erro);
      alert("Erro ao enviar o fomulario")
    });
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
        <td><input type="number" placeholder="0" min="0" /></td>`;
      tbody.appendChild(tr);
    }

