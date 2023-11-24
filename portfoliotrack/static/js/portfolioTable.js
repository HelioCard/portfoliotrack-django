// var data = [
//     {
//         asset: "AESB3",
//         sort_of:   "Ações",
//         quantity:     "2000",
//         average_price: "12,00",
//         last_price:     "13,80",
//         contribution:       "50.000,00",
//         equity: "52.800,00",
//         earnings:     "0,00",
//         yield:       "2.800,00",
//         result: "5 %",
//         yield_on_cost:     "0 %",
//     },
//     {
//         asset:       "TRPL4",
//         sort_of:   "Ações",
//         quantity:     "1500",
//         average_price: "22,00",
//         last_price:     "23,63",
//         contribution:       "60.000,00",
//         equity: "65.000,00",
//         earnings:     "3.000,00",
//         yield:       "8.000,00",
//         result: "10 %",
//         yield_on_cost:     "6 %",
//     }
// ]

// Obter dados da API
const getPortfolioSummaryData = async (url) => {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.Erro === 'No data') {
          alert('Possivelmente ainda não há dados de transações. Adicione suas transações no menu à esquerda!');
          showNoData()
        } else {
          throw new Error(`Erro: ${errorData.Erro}`);
        }
      } else {
        return await response.json();
      }
    } catch (ex) {
      alert(ex.message);
    }
  }

async function updatePortfolioSummary(URL) {
    try {
        const data = await getPortfolioSummaryData(URL)
        if (data) {
            console.log(data.summary_data)
            let portfolioTable = new DataTable('#portfolioTable', {
                data: data.summary_data,
                columns: [
                    { data: 'asset' },
                    { data: 'sort_of' },
                    { data: 'quantity' },
                    { data: 'average_price' },
                    { data: 'last_price' },
                    { data: 'contribution' },
                    { data: 'equity' },
                    { data: 'earnings' },
                    { data: 'yield' },
                    { data: 'result' },
                    { data: 'yield_on_cost' },
                ],
                responsive: true,
                language: {
                    decimal: ',',
                    thousands: '.',
                    zeroRecords: 'Não há dados',
                },
                order: [[0, 'desc']],
                info: false,
                searching: false,
                paging: false,
                select: false,
            });            
        }
    } catch (error) {
        alert('Erro: ', error)
    }
};

updatePortfolioSummary(getPortfolioSummaryURL)
