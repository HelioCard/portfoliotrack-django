// Elementos do DOM
const elements = {
  targetText: document.querySelector('#targetText'),
  averageDividendsText: document.querySelector('#averageDividendsText'),
  averageYieldText: document.querySelector('#averageYieldText'),
  missingContributionText: document.querySelector('#missingContributionText'),
}

// Obter dados da API
const getTargetData = async (url) => {
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
    var row = `<tr class="align-middle" style="height: 60px;">
      <th><a href="#"> <span class="badge text-bg-primary w-100" style="font-size: 1.0rem;">${tableData[i].ticker}</span> </a></th>
      <td class="text-center">${tableData[i].quantity.toLocaleString('pt-BR', {useGrouping: true})}</td>
      <td class="text-center">${tableData[i].average_dividend}</td>
      <td class="text-center">${tableData[i].yearly_dividend}</td>
      <td class="text-center">${tableData[i].target_yearly_dividend}</td>
      <td class="text-center">${tableData[i].quantity_target.toLocaleString('pt-BR', {useGrouping: true})}</td>
      <td class="text-center">${tableData[i].difference.toLocaleString('pt-BR', {useGrouping: true})}</td>
      <td class="text-center">
      ${tableData[i].accomplished}%
      <div class="progress" role="progressbar" aria-label="progress striped" aria-valuenow="${tableData[i].accomplished}" aria-valuemin="0" aria-valuemax="100">
        <div class="progress-bar progress-bar-striped bg-primary" style="width: ${tableData[i].accomplished}%;"></div>
      </div>
      </td>
      
    </tr>`
    table.innerHTML += row;
  };
}

async function updateTargetTable(URL) {
    try {
        // document.querySelector('#spinner').hidden = false;
        const data = await getTargetData(URL)
        if (data) {
          const {target_data, cards_data} = data
          buildDomTable(target_data) 
          elements.targetText.innerHTML = 'R$ ' + cards_data.total_dividends_target;
          elements.averageDividendsText.innerHTML = 'R$ ' + cards_data.total_average_dividend;
          elements.averageYieldText.innerHTML = cards_data.average_yield.toFixed(2).replace('.', ',') + '%';
          elements.missingContributionText.innerHTML = 'R$ ' + cards_data.missing_contribution;
        };
        // document.querySelector('#spinner').hidden = true;
    } catch (error) {
        alert('Erro: ', error)
    }
};

updateTargetTable(getTargetURL)


var objJson = {}

function updateBalanceValues(inputElement, textID) {
    textID.innerHTML = inputElement.value
    let ticker = inputElement.dataset.asset
    let weight = inputElement.value
    document.querySelector('#btnUpdateURL').classList.remove('disabled')
    objJson[ticker] = parseInt(weight)
}
