// Gráfico de Aportes x Patrimônio//
////////////////////////////////////

const getOptionPortPerf = async () => {
  try {
    const response = await fetch(portfolioPerformanceChartURL);
    return await response.json();
  } catch (ex) {
    alert(ex)
  }
}

const portfolioPerformanceChart = echarts.init(document.getElementById("performance_chart"), 'macarons');
const initPortfolioPerformanceChart = async () => {
  portfolioPerformanceChart.setOption(await getOptionPortPerf());
  portfolioPerformanceChart.resize();
}

window.addEventListener('load', async () => {
  await initPortfolioPerformanceChart();
})




// Gráfico de Divisão por Categorias//
//////////////////////////////////////

const getOptionCategory = async () => {
  try {
    const response = await fetch(categoryChartURL);
    return await response.json();
  } catch (ex) {
    alert(ex)
  }
}

const categoryChart = echarts.init(document.getElementById("category_chart"), 'macarons');
const initCategoryChart = async () => {
  categoryChart.setOption(await getOptionCategory());
  categoryChart.resize();
}

window.addEventListener('load', async () => {
  await initCategoryChart();
})





// Gráfico de Divisão por Ativos//
//////////////////////////////////

const getOptionAsset = async () => {
  try {
    const response = await fetch(assetChartURL);
    return await response.json();
  } catch (ex) {
    alert(ex)
  }
}

const assetChart = echarts.init(document.getElementById("asset_chart"), 'macarons');
const initAssetChart = async () => {
  assetChart.setOption(await getOptionAsset());
  assetChart.resize();
}

window.addEventListener('load', async () => {
  await initAssetChart();
})






// Resize all charts
function resizeAllCharts() {
  portfolioPerformanceChart.resize();
  categoryChart.resize();
  assetChart.resize();
}









