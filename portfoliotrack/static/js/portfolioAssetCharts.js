const THEME = 'westeros'
let performanceChart, contributionChart, assetVariationChart

// Elementos do DOM
const elements = {
  equity: document.querySelector("#equity"),
  equityChange: document.querySelector('#equityChange'),
  equityPeriod: document.querySelector('#equityPeriod'),
  contribution: document.querySelector("#contribution"),
  contributionChange: document.querySelector('#contributionChange'),
  contributionPeriod: document.querySelector('#contributionPeriod'),
  result: document.querySelector("#result"),
  resultChange: document.querySelector('#resultChange'),
  resultPeriod: document.querySelector('#resultPeriod'),
  yieldOnCost: document.querySelector("#yieldOnCost"),
  yieldOnCostChange: document.querySelector('#yieldOnCostChange'),
  yieldOnCostPeriod: document.querySelector('#yieldOnCostPeriod'),
  performanceChartStatus: document.querySelector('#performanceChartStatus'),
  categoryChartStatus: document.querySelector('#categoryChartStatus'),
  assetChartStatus: document.querySelector('#assetChartStatus'),
  yield: document.querySelector('#yield'),
  contributionChartStatus: document.querySelector('#contributionChartStatus'),
  assetVariationChartStatus: document.querySelector('#assetVariationChartStatus'),
  dividends: document.querySelector('#dividendsCard'),
}

// Exibir mensagem quando não houver dados
function showNoData() {
  elements.performanceChartStatus.innerHTML = '<h6 class="display-5">Não há dados</h6>'
  elements.contributionChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
}

// Alternar a cor do elemento com base no valor
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

// Atualizar os gráficos e cards
async function updateDashboardData(dataURL) {
  try {
    const data = await getDataFromAPI(dataURL);
    if (data) {
      const { performance_data, cards_data, contribution_data } = data;

      performance_options.xAxis.data = performance_data.date;
      performance_options.series[0].data = performance_data.contribution;
      performance_options.series[1].data = performance_data.equity;
      performance_options.series[2].data = performance_data.dividends;

      contribution_options.xAxis.data = contribution_data.date;
      contribution_options.series[0].data = contribution_data.contribution;
      

      performanceChart = echarts.init(document.getElementById('performanceChart'), THEME);
      contributionChart = echarts.init(document.querySelector('#contributionChart'), THEME);

      performanceChart.setOption(performance_options);
      contributionChart.setOption(contribution_options);

      elements.dividends.innerHTML = cards_data.dividends.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});

      elements.equity.innerHTML = cards_data.equity.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      elements.equityChange.innerHTML = (cards_data.equity.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.equityPeriod.innerHTML = '(' + cards_data.equity.period + ')';
      alternateColor(elements.equityChange, cards_data.equity.change)
      
      elements.contribution.innerHTML = cards_data.contribution.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      elements.contributionChange.innerHTML = (cards_data.contribution.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.contributionPeriod.innerHTML = '(' + cards_data.contribution.period + ')';
      alternateColor(elements.contributionChange, cards_data.contribution.change)

      elements.result.innerHTML = (cards_data.result.value * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.resultChange.innerHTML = (cards_data.result.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.resultPeriod.innerHTML = '(' + cards_data.result.period + ')';
      elements.yield.innerHTML = cards_data.yield.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      alternateColor(elements.resultChange, cards_data.result.change)
      alternateColor(elements.yield, cards_data.yield)

      elements.yieldOnCost.innerHTML = (cards_data.yield_on_cost.value * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.yieldOnCostChange.innerHTML = (cards_data.yield_on_cost.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.yieldOnCostPeriod.innerHTML = '(' + cards_data.yield_on_cost.period + ')';
      alternateColor(elements.yieldOnCostChange, cards_data.yield_on_cost.change)

    }
  } catch (error) {
    console.error(error);
    alert('Erro ao atualizar os dados!')
  }
};

// Redimensionar os gráficos
function resizeDashboardCharts() {
  if (performanceChart && contributionChart) {
    performanceChart.resize();
    contributionChart.resize();
  }
}

setInterval(function () {
  resizeDashboardCharts()
}, 1000);

updateDashboardData(portfolioAssetDataURL)

