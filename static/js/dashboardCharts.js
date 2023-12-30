const THEME = 'westeros'
let assetChart, categoryChart, portfolioPerformanceChart, contributionChart, assetVariationChart

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
  highestDividend: document.querySelector('#highestDividend'),
  tickerOfHighestDividend: document.querySelector('#tickerOfHighestDividend'),
  hightestDividendLink: document.querySelector('#hightestDividendLink'),
}

// Exibir mensagem quando não houver dados
function showNoData() {
  elements.performanceChartStatus.innerHTML = '<h6 class="display-5">Não há dados</h6>'
  elements.categoryChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
  elements.assetChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
  elements.assetVariationChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
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
async function updateDashboardData(dashboardDataURL) {
  try {
    const data = await getDataFromAPI(dashboardDataURL);
    if (data) {
      const { asset_data, category_data, performance_data, cards_data, contribution_data, asset_variation_data } = data;

      performance_options.xAxis.data = performance_data.date;
      performance_options.series[0].data = performance_data.contribution;
      performance_options.series[1].data = performance_data.equity;
      performance_options.series[2].data = performance_data.dividends;
      category_options.series[0].data = category_data;
      asset_options.series[0].data = asset_data;
      contribution_options.xAxis.data = contribution_data.date;
      contribution_options.series[0].data = contribution_data.contribution;
      asset_variation_options.xAxis.data = asset_variation_data.ticker;
      asset_variation_options.series[0].data = asset_variation_data.variation

      portfolioPerformanceChart = echarts.init(document.getElementById('performanceChart'), THEME);
      assetChart = echarts.init(document.getElementById('assetChart'), THEME);
      categoryChart = echarts.init(document.getElementById('categoryChart'), THEME);
      contributionChart = echarts.init(document.querySelector('#contributionChart'), THEME);
      assetVariationChart = echarts.init(document.querySelector('#assetVariationChart'), THEME);

      portfolioPerformanceChart.setOption(performance_options);
      assetChart.setOption(asset_options);
      categoryChart.setOption(category_options);
      contributionChart.setOption(contribution_options);
      assetVariationChart.setOption(asset_variation_options);

      elements.dividends.innerHTML = cards_data.dividends.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});

      elements.highestDividend.innerHTML = cards_data.highest_dividend.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});

      elements.tickerOfHighestDividend.innerHTML = cards_data.ticker_of_highest_dividend
      elements.hightestDividendLink.href = baseURL.replace('PLACEHOLDER', cards_data.ticker_of_highest_dividend)

      elements.equity.innerHTML = cards_data.equity.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      elements.equityChange.innerHTML = (cards_data.equity.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.equityPeriod.innerHTML = '(Últimos ' + cards_data.equity.period + ')';
      alternateColor(elements.equityChange, cards_data.equity.change)
      
      elements.contribution.innerHTML = cards_data.contribution.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      elements.contributionChange.innerHTML = (cards_data.contribution.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.contributionPeriod.innerHTML = '(Últimos ' + cards_data.contribution.period + ')';
      alternateColor(elements.contributionChange, cards_data.contribution.change)

      elements.result.innerHTML = (cards_data.result.value * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.resultChange.innerHTML = (cards_data.result.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      elements.resultPeriod.innerHTML = '(Últimos ' + cards_data.result.period + ')';
      elements.yield.innerHTML = cards_data.yield.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      alternateColor(elements.resultChange, cards_data.result.change)
      alternateColor(elements.yield, cards_data.yield)

      elements.yieldOnCost.innerHTML = (cards_data.yield_on_cost.value * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
      elements.yieldOnCostChange.innerHTML = (cards_data.yield_on_cost.change * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      elements.yieldOnCostPeriod.innerHTML = '(Últimos ' + cards_data.yield_on_cost.period + ')';
      alternateColor(elements.yieldOnCostChange, cards_data.yield_on_cost.change)

    }
  } catch (error) {
    console.error(error);
    alert('Erro ao atualizar os dados!')
  }
};

// Redimensionar os gráficos
function resizeDashboardCharts() {
  if (portfolioPerformanceChart && categoryChart && assetChart && contributionChart && assetVariationChart) {
    portfolioPerformanceChart.resize();
    categoryChart.resize();
    assetChart.resize();
    contributionChart.resize();
    assetVariationChart.resize();
  }
}

setInterval(function () {
  resizeDashboardCharts()
}, 1000);

updateDashboardData(DashBoardDataURL)

