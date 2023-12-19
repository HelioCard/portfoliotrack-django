
function buildDomTable(tableData) {
  var table = document.getElementById('tableBody');
  for (var i = 0; i < tableData.length; i++){
    var yieldColor = parseFloat(tableData[i].yield) >= 0 ? 'text-success' : 'text-danger';
    var resultColor = parseFloat(tableData[i].result) >= 0 ? 'text-success' : 'text-danger';
    var assetColor = parseFloat(tableData[i].result) >= 0 ? 'text-bg-primary' : 'text-bg-danger';
    var assetURL = baseURL.replace('PLACEHOLDER', tableData[i].asset);
    var row = `<tr class="align-middle" style="height: 60px">
      <td><a href="${assetURL}"> <span class="badge ${assetColor} w-100" style="font-size: 1.0rem;">${tableData[i].asset}</span> </a></td>
      <td class="text-center">${tableData[i].sort_of}</td>
      <td class="text-end">${tableData[i].quantity}</td>
      <td class="text-end">${tableData[i].average_price}</td>
      <td class="text-end">${tableData[i].last_price}</td>
      <td class="text-end">${tableData[i].contribution}</td>
      <td class="text-end">${tableData[i].equity}</td>
      <td class="text-end">${tableData[i].earnings}</td>
      <td class="text-end ${yieldColor}">${tableData[i].yield}</td>
      <td class="text-end ${resultColor}">${tableData[i].result}%</td>
      <td class="text-end">${tableData[i].yield_on_cost}%</td>
    </tr>`
    table.innerHTML += row;
  };
}


let portfolioSummaryTable

async function updatePortfolioSummary(URL) {
    try {
        document.querySelector('#spinner').hidden = false;
        const data = await getDataFromAPI(URL)
        if (data) {
          buildDomTable(data.summary_data);
        };
        document.querySelector('#spinner').hidden = true;
    } catch (error) {
      console.error(error)
      alert('Erro ao atualizar os dados!');
    }
};

updatePortfolioSummary(getPortfolioSummaryURL)
