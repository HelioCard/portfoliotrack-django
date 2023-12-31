const THEME = 'westeros';
let incomesEvolutionChart
let yieldEvolutionChart

// Elementos do DOM
const elements = {
    dividendsText: document.querySelector('#dividendsText'),
    yieldOnCostText: document.querySelector('#yieldOnCostText'),
    averageDividendsText: document.querySelector('#averageDividendsText'),
    dividendEvolutionChartStatus: document.querySelector('#dividendEvolutionChartStatus'),
    yieldEvolutionChartStatus:document.querySelector('#yieldEvolutionChartStatus'),
}

function showNoData() {
    elements.dividendEvolutionChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
    elements.yieldEvolutionChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
}

async function updateIncomesEvolutionChart(URL) {
    try {
        const data = await getDataFromAPI(URL)
        if (data) {
            const { incomes_evolution, incomes_cards } = data

            incomesOptions.xAxis[0].data = incomes_evolution.date
            incomesOptions.series[0].data = incomes_evolution.dividends

            yieldOptions.xAxis[0].data = incomes_evolution.date
            yieldOptions.series[0].data = incomes_evolution.yield_on_cost

            incomesEvolutionChart = echarts.init(document.querySelector('#dividendEvolutionChart'), THEME);
            incomesEvolutionChart.setOption(incomesOptions);

            yieldEvolutionChart = echarts.init(document.querySelector('#yieldEvolutionChart'), THEME);
            yieldEvolutionChart.setOption(yieldOptions);

            document.querySelector('#dividendsText').innerHTML = `R$ ${incomes_cards.total_dividends}`;
            document.querySelector('#yieldOnCostText').innerHTML = `${incomes_cards.total_yield_on_cost} %`;
            document.querySelector('#averageDividendsText').innerHTML = `R$ ${incomes_cards.average_dividend}`;
            document.querySelector('#calculatedPeriodText').innerHTML = `(Últimos ${incomes_cards.calculated_period})`;
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao atualizar os gráficos e mostrar os dados.');
    }
};

updateIncomesEvolutionChart(getIncomesEvolutiontURL)

function resizeIncomesChart() {
    if (incomesEvolutionChart && yieldEvolutionChart) {
        incomesEvolutionChart.resize();
        yieldEvolutionChart.resize();
    }
};

setInterval(function () {
    resizeIncomesChart()
}, 1000);
