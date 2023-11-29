// Obter dados da API
const getBalanceData = async (url) => {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.Erro === 'No data') {
          alert('Possivelmente ainda não há dados de transações. Adicione suas transações no menu à esquerda!');
        } else {
          throw new Error(`Erro: ${errorData.Erro}`);
        }
      } else {
        return await response.json();
      }
    } catch (ex) {
      alert(ex.message);
    }
  }

function buildDomTable(tableData) {
  var table = document.getElementById('tableBody');
  for (var i = 0; i < tableData.length; i++){
    var toBalanceColor = parseFloat(tableData[i].current_percentage) <= parseFloat(tableData[i].ideal_percentage) ? 'text-success' : 'text-warning';
    var row = `<tr class="align-middle" style="height: 60px;">
      <th><a href="#"> <span class="badge text-bg-primary w-100">${tableData[i].asset}</span> </a></th>
      <td class="text-end">${tableData[i].quantity}</td>
      <td class="text-end">${tableData[i].last_price}</td>
      <td class="text-end">${tableData[i].equity}</td>
      <td>
        <div class="d-flex align-items-center justify-content-start gap-1">
            <span class="align-middle badge text-bg-primary" style="min-width: 50px;">${tableData[i].weight}</span>
            <input type="range" class="form-range" style="min-width: 100px;" min="0" max="100" value="${tableData[i].weight}" class="align-middle">
        </div>
      </td>
      <td class="text-end">${tableData[i].ideal_percentage} %</td>
      <td class="text-end">${tableData[i].current_percentage} %</td>
      <td class="text-center ${toBalanceColor}">${tableData[i].to_balance}</td>
    </tr>`
    table.innerHTML += row;
  };
}

async function updateBalanceTable(URL) {
    try {
        document.querySelector('#spinner').hidden = false;
        const data = await getBalanceData(URL)
        if (data) {
          buildDomTable(data.balance_data) 
        };
        document.querySelector('#spinner').hidden = true;
    } catch (error) {
        alert('Erro: ', error)
    }
};

updateBalanceTable(getBalanceURL)
