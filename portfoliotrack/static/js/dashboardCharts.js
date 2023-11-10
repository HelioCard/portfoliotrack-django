const THEME = 'infographic'
var assetChart, categoryChart, portfolioPerformanceChart
var equity = document.querySelector("#equity");
var equity_change = document.querySelector('#equity_change');
var equity_period = document.querySelector('#equity_period');
var contribution = document.querySelector("#contribution");
var contribution_change = document.querySelector('#contribution_change');
var contribution_period = document.querySelector('#contribution_period');
var result = document.querySelector("#result");
var result_change = document.querySelector('#result_change');
var result_period = document.querySelector('#result_period');
var yield_on_cost = document.querySelector("#yield_on_cost");
var yield_on_cost_change = document.querySelector('#yield_on_cost_change');
var yield_on_cost_period = document.querySelector('#yield_on_cost_period');

const getDashboardData = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Possivelmente ainda não há dados de transações. Adicione suas transações no menu à esquerda!');
      } else {
        const errorData = await response.json();
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
    portfolioPerformanceChart = echarts.init(document.getElementById('performance_chart'), THEME);
    assetChart = echarts.init(document.getElementById('asset_chart'), THEME);
    categoryChart = echarts.init(document.getElementById('category_chart'), THEME);

    const data = await getDashboardData(DashBoardDataURL);
    
    if (data) {
      const { asset_data, category_data, performance_data, cards_data } = data;

      equity.innerHTML = cards_data.equity.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      equity_change.innerHTML = (cards_data.equity.change * 100).toFixed(2).replace('.', ',') + '%';
      equity_period.innerHTML = '(' + cards_data.equity.period + ')';
      alternateColor(equity_change, cards_data.equity.change)
      
      contribution.innerHTML = cards_data.contribution.value.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
      contribution_change.innerHTML = (cards_data.contribution.change * 100).toFixed(2).replace('.', ',') + '%';
      contribution_period.innerHTML = '(' + cards_data.contribution.period + ')';
      alternateColor(contribution_change, cards_data.contribution.change)

      result.innerHTML = (cards_data.result.value * 100).toFixed(2).replace('.', ',') + '%';
      result_change.innerHTML = (cards_data.result.change * 100).toFixed(2).replace('.', ',');
      result_period.innerHTML = '(' + cards_data.result.period + ')';
      alternateColor(result_change, cards_data.result.change)

      yield_on_cost.innerHTML = (cards_data.yield_on_cost.value * 100).toFixed(2).replace('.', ',') + '%';
      yield_on_cost_change.innerHTML = (cards_data.yield_on_cost.change * 100).toFixed(2).replace('.', ',');
      yield_on_cost_period.innerHTML = '(' + cards_data.yield_on_cost.period + ')';
      alternateColor(yield_on_cost_change, cards_data.yield_on_cost.change)

      performance_options.xAxis.data = performance_data.date;
      performance_options.series[0].data = performance_data.contribution;
      performance_options.series[1].data = performance_data.equity;
      performance_options.series[2].data = performance_data.dividends;

      category_options.series[0].data = category_data

      asset_options.series[0].data = asset_data

    }
    portfolioPerformanceChart.setOption(performance_options)
    assetChart.setOption(asset_options)
    categoryChart.setOption(category_options)

    resizeDashboardCharts()
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
