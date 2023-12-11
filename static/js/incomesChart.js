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
            if (erroData.Erro === 'No data') {
                alert('Possivelmente ainda não há dados de transações. Adicion suas transações no menu à esquerda!');
                showNoData()
            } else {
                throw new Error(`Erro: ${errorData.Erro}`);
            };
        } else {
            return await response.json();
        }
    } catch (ex) {
        alert(ex);
    }
}

async function updateIncomesEvolutionChart(URL) {
    try {
        const data = await getIncomesData(URL)
        if (data) {
            const { incomes_evolution_chart_data, incomes_cards_data } = data
            console.log(incomes_evolution_chart_data)
            console.log(incomes_cards_data)

            incomesEvolutionChart = echarts.init(document.querySelector('#dividendEvolutionChart'), THEME);
            incomesEvolutionChart.setOption(incomesOptions);
        }
    } catch (error) {
        alert('Erro: ', error);
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
