const THEME = 'walden'
var assetChart, categoryChart, portfolioPerformanceChart

const getDashboardData = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Erro ao buscar dados do painel');
    }
    return await response.json();
  } catch (ex) {
    alert(ex);
  }
}

(async () => {
  try {
    portfolioPerformanceChart = echarts.init(document.getElementById('performance_chart'), THEME);
    assetChart = echarts.init(document.getElementById('asset_chart'), THEME);
    categoryChart = echarts.init(document.getElementById('category_chart'), THEME);

    const data = await getDashboardData(DashBoardDataURL);
    
    if (data) {
      const { asset_data, category_data, performance_data } = data;
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
