
let categoryChart, assetChart, portfolioPerformanceChart;
const THEME = 'macarons'

const getDashboardData = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Erro ao buscar dados do painel');
    }
    return await response.json();
  } catch (ex) {
    alert(ex);
    throw ex; // Rejoga o erro para que ele possa ser tratado posteriormente, se necessário
  }
}

(async () => {
  try {
    const data = await getDashboardData(DashBoardDataURL);
    const { asset_data, category_data, performance_data } = data;

    window.addEventListener('load', async () => {
      assetChart = echarts.init(document.getElementById('asset_chart'), THEME);
      assetChart.setOption(asset_data)
      categoryChart = echarts.init(document.getElementById('category_chart'), THEME);
      categoryChart.setOption(category_data)
      portfolioPerformanceChart = echarts.init(document.getElementById('performance_chart'), THEME);
      portfolioPerformanceChart.setOption(performance_data)      
    });
    resizeAllCharts()
  } catch (error) {
    console.error("Ocorreu um erro:", error);
  }
})();

function resizeAllCharts() {
  if (portfolioPerformanceChart && categoryChart && assetChart) {
    portfolioPerformanceChart.resize();
    categoryChart.resize();
    assetChart.resize();
  }
}
