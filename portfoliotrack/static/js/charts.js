const getOption = async (url) => {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (ex) {
    alert(ex);
  }
}

let categoryChart;
let assetChart;
let portfolioPerformanceChart;

const initChart = async (chartID, url) => {
  const chart = echarts.init(document.getElementById(chartID), 'macarons');
  chart.setOption(await getOption(url));
  chart.resize();
  return chart;
}

window.addEventListener('load', async () => {
  assetChart = await initChart('asset_chart', assetChartURL);
  categoryChart = await initChart('category_chart', categoryChartURL);
  portfolioPerformanceChart = await initChart('performance_chart', portfolioPerformanceChartURL);
});

// Resize all charts
function resizeAllCharts() {
  if (portfolioPerformanceChart && categoryChart && assetChart) {
    portfolioPerformanceChart.resize();
    categoryChart.resize();
    assetChart.resize();
  }
}
