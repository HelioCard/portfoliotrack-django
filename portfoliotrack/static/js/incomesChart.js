const THEME = 'westeros';
let incomesEvolutionChart

// Elementos do DOM
const elements = {
    dividendsText: document.querySelector('#dividendsText'),
    yieldOnCostText: document.querySelector('#yieldOnCostText'),
    averageDividendsText: document.querySelector('#averageDividendsText'),
    dividendEvolutionChartStatus: document.querySelector('#dividendEvolutionChartStatus'),
}

function showNoData() {
    elements.dividendEvolutionChartStatus.innerHTML = '<h6 class="display-6">Não há dados</h6>'
}

// Obter dados do endpoint
const getIncomesData = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errorData = await response.json();
            if (errorData.Erro === 'No data') {
                alert('Possivelmente ainda não há dados de transações. Adicion suas transações no menu à esquerda!');
                showNoData()
            } else {
                throw new Error(`Erro: ${errorData.Erro}`);
            };
        } else {
            return await response.json();
        }
    } catch (ex) {
        console.error(ex)
        alert('Ocorreu um erro ao buscar os dados!');
    }
}

async function updateIncomesEvolutionChart(URL) {
    try {
        const data = await getIncomesData(URL)
        if (data) {
            const { incomes_evolution, incomes_cards } = data

            incomesOptions.xAxis[0].data = incomes_evolution.date
            incomesOptions.series[0].data = incomes_evolution.dividends
            incomesOptions.series[1].data = incomes_evolution.yield_on_cost

            incomesEvolutionChart = echarts.init(document.querySelector('#dividendEvolutionChart'), THEME);
            incomesEvolutionChart.setOption(incomesOptions);

            document.querySelector('#dividendsText').innerHTML = `R$ ${incomes_cards.total_dividends}`;
            document.querySelector('#yieldOnCostText').innerHTML = `${incomes_cards.total_yield_on_cost} %`;
            document.querySelector('#averageDividendsText').innerHTML = `R$ ${incomes_cards.average_dividend}`;
            document.querySelector('#calculatedPeriodText').innerHTML = `(${incomes_cards.calculated_period})`;
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao atualizar o gráfico.');
    }
};

updateIncomesEvolutionChart(getIncomesEvolutiontURL)

function resizeIncomesChart() {
    if (incomesEvolutionChart) {
        incomesEvolutionChart.resize();
    }
};

setInterval(function () {
    resizeIncomesChart()
}, 1000);
