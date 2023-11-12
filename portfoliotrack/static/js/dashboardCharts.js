const THEME = 'infographic'
let assetChart, categoryChart, portfolioPerformanceChart
const equity = document.querySelector("#equity");
const equityChange = document.querySelector('#equityChange');
const equityPeriod = document.querySelector('#equityPeriod');
const contribution = document.querySelector("#contribution");
const contributionChange = document.querySelector('#contributionChange');
const contributionPeriod = document.querySelector('#contributionPeriod');
const result = document.querySelector("#result");
const resultChange = document.querySelector('#resultChange');
const resultPeriod = document.querySelector('#resultPeriod');
const yieldOnCost = document.querySelector("#yieldOnCost");
const yieldOnCostChange = document.querySelector('#yieldOnCostChange');
const yieldOnCostPeriod = document.querySelector('#yieldOnCostPeriod');

function showNoData() {
  document.querySelector('#performanceChartStatus').innerHTML = '<h6 class="display-5">Não há dados</h6>'
  document.querySelector('#categoryChartStatus').innerHTML = '<h6 class="display-6">Não há dados</h6>'
  document.querySelector('#assetChartStatus').innerHTML = '<h6 class="display-6">Não há dados</h6>'
}

const getDashboardData = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      const errorData = await response.json();
      if (errorData.Erro === 'No data') {
        alert('Possivelmente ainda não há dados de transações. Adicione suas transações no menu à esquerda!');
        showNoData()
      } else {
        throw new Error(`Erro: ${errorData.Erro}`);
      }
    }
    return await response.json();
  } catch (ex) {
    alert(ex.message);
  }
}

function alternateColor(element, value) {
  if (value > 0) {
    element.style.color = 'green';
    element.innerHTML = '+' + element.innerHTML;
  } else if (value < 0) {
    element.style.color = 'red';
  } else {
    element.style.color = '';
  }
}

(async () => {
  try {
    const data = await getDashboardData(DashBoardDataURL);

    if (data) {
      const { asset_data, category_data, performance_data, cards_data } = data;

      equity.innerHTML = cards_data.equity.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      equityChange.innerHTML = (cards_data.equity.change * 100).toFixed(2).replace('.', ',') + '%';
      equityPeriod.innerHTML = '(' + cards_data.equity.period + ')';
      alternateColor(equityChange, cards_data.equity.change)
      
      contribution.innerHTML = cards_data.contribution.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      contributionChange.innerHTML = (cards_data.contribution.change * 100).toFixed(2).replace('.', ',') + '%';
      contributionPeriod.innerHTML = '(' + cards_data.contribution.period + ')';
      alternateColor(contributionChange, cards_data.contribution.change)

      result.innerHTML = (cards_data.result.value * 100).toFixed(2).replace('.', ',') + '%';
      resultChange.innerHTML = (cards_data.result.change * 100).toFixed(2).replace('.', ',');
      resultPeriod.innerHTML = '(' + cards_data.result.period + ')';
      alternateColor(resultChange, cards_data.result.change)

      yieldOnCost.innerHTML = (cards_data.yield_on_cost.value * 100).toFixed(2).replace('.', ',') + '%';
      yieldOnCostChange.innerHTML = (cards_data.yield_on_cost.change * 100).toFixed(2).replace('.', ',');
      yieldOnCostPeriod.innerHTML = '(' + cards_data.yield_on_cost.period + ')';
      alternateColor(yieldOnCostChange, cards_data.yield_on_cost.change)

      portfolioPerformanceChart = echarts.init(document.getElementById('performanceChart'), THEME);
      assetChart = echarts.init(document.getElementById('assetChart'), THEME);
      categoryChart = echarts.init(document.getElementById('categoryChart'), THEME);

      performance_options.xAxis.data = performance_data.date;
      performance_options.series[0].data = performance_data.contribution;
      performance_options.series[1].data = performance_data.equity;
      performance_options.series[2].data = performance_data.dividends;
      category_options.series[0].data = category_data
      asset_options.series[0].data = asset_data

      portfolioPerformanceChart.setOption(performance_options)
      assetChart.setOption(asset_options)
      categoryChart.setOption(category_options)

      resizeDashboardCharts()
    }
  } catch (error) {
    console.error("Ocorreu um erro:", error);
  }
})();


function resizeDashboardCharts() {
  if (portfolioPerformanceChart && categoryChart && assetChart) {
    portfolioPerformanceChart.resize();
    categoryChart.resize();
    assetChart.resize();
  }
}
