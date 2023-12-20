
function buildDomTable(tableData) {
  var table = document.getElementById('tableBody');
  for (var i = 0; i < tableData.length; i++){
    var currentPercentage = parseFloat(tableData[i].current_percentage.replace(',', '.'));
    var idealPercentage = parseFloat(tableData[i].ideal_percentage);
    var toBalanceColor = currentPercentage <= idealPercentage ? 'text-success' : 'text-warning';
    var textID = `text${tableData[i].asset}`
    var assetURL = baseURL.replace('PLACEHOLDER', tableData[i].asset)
    var row = `<tr class="align-middle" style="height: 60px;">
      <th><a href="${assetURL}"> <span class="badge text-bg-primary w-100" style="font-size: 1.0rem;">${tableData[i].asset}</span> </a></th>
      <td class="text-end">${tableData[i].quantity}</td>
      <td class="text-end">${tableData[i].last_price}</td>
      <td class="text-end">${tableData[i].equity}</td>
      <td>
        <div class="d-flex align-items-center justify-content-start gap-1">
            <span id="${textID}" class="align-middle badge text-bg-primary" style="min-width: 50px; font-size: 1.0rem">${tableData[i].weight}</span>
            <input
                data-asset="${tableData[i].asset}"
                type="range"
                class="form-range align-middle"
                style="min-width: 100px;" min="0" max="100" value="${tableData[i].weight}"
                oninput="updateBalanceValues(this, ${textID})"
                onblur="updateUpdateURL()"
            >
        </div>
      </td>
      <td class="text-end">${tableData[i].ideal_percentage} %</td>
      <td class="text-end">${tableData[i].current_percentage} %</td>
      <td class="text-center ${toBalanceColor}">${tableData[i].to_balance}</td>
    </tr>`
    table.innerHTML += row;
  };
}

function showNoData() {
  document.getElementById('tableBody').innerHTML = `<tr class="align-middle" style="height: 60px;">
      <th class="text-center"><a href="#"> <span class="badge text-bg-primary w-75" style="font-size: 1.0rem;">---</span> </a></th>
      <td class="text-center">Não há dados</td>
      <td class="text-center">Não há dados</td>
      <td class="text-center">Não há dados</td>
      <td class="text-center">Não há dados</td>
      <td class="text-center">Não há dados</td>
      <td class="text-center">Não há dados</td>
      <td class="text-center">Não há dados</td>
  </tr>`
  
}

async function updateBalanceTable(URL) {
    try {
        document.querySelector('#spinner').hidden = false;
        const data = await getDataFromAPI(URL)
        if (data) {
          buildDomTable(data.balance_data) 
        };
        document.querySelector('#spinner').hidden = true;
    } catch (error) {
      console.error(error)
      alert('Erro ao atualizar os dados!');
    }
};

updateBalanceTable(getBalanceURL)


var objJson = {}

function updateBalanceValues(inputElement, textID) {
    textID.innerHTML = inputElement.value
    let ticker = inputElement.dataset.asset
    let weight = inputElement.value
    document.querySelector('#btnUpdateURL').classList.remove('disabled')
    objJson[ticker] = parseInt(weight)
}
