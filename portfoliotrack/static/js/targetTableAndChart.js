const THEME = 'westeros';
let fractionChart

// Elementos do DOM
const elements = {
  targetText: document.querySelector('#targetText'),
  averageDividendsText: document.querySelector('#averageDividendsText'),
  averageYieldText: document.querySelector('#averageYieldText'),
  missingContributionText: document.querySelector('#missingContributionText'),
  fractionChartStatus: document.querySelector('#fractionChartStatus'),
}

function showNoData() {
  elements.fractionChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
}


function buildDomTable(tableData) {
  var table = document.getElementById('tableBody');
  for (var i = 0; i < tableData.length; i++){
    var assetURL = baseURL.replace('PLACEHOLDER', tableData[i].ticker)
    var row = `<tr class="align-middle" style="height: 60px;">
      <th><a href="${assetURL}"> <span class="badge text-bg-primary w-100" style="font-size: 1.0rem;">${tableData[i].ticker}</span> </a></th>
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
        const data = await getDataFromAPI(URL)
        if (data) {
          const {target_data, cards_data} = data
          buildDomTable(target_data) 
          elements.targetText.innerHTML = 'R$ ' + cards_data.total_dividends_target;
          elements.averageDividendsText.innerHTML = 'R$ ' + cards_data.total_average_dividend;
          elements.averageYieldText.innerHTML = cards_data.average_yield.toFixed(2).replace('.', ',') + '%';
          elements.missingContributionText.innerHTML = 'R$ ' + cards_data.missing_contribution;
          
          fractionChart = echarts.init(document.querySelector('#fractionChart'), THEME);
          fractionOptions.series[0].data[0].value = cards_data.concluded
          fractionOptions.series[0].data[1].value = 100 - cards_data.concluded
          fractionChart.setOption(fractionOptions)
        };
        // document.querySelector('#spinner').hidden = true;
    } catch (error) {
      console.error(error)
      alert('Erro ao atualizar os dados!');
    }
};

updateTargetTable(getTargetURL)


function resizeTargetChart() {
if (fractionChart) {
  fractionChart.resize();
}
}

setInterval(function () {
  resizeTargetChart()
}, 1000);
