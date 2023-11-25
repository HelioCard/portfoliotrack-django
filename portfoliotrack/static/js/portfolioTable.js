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

function buildTable(tableData) {
  var table = document.getElementById('tableBody');
  for (var i = 0; i < tableData.length; i++){
    var row = `<tr class="align-middle" style="height: 60px">
      <td><a href="#">${tableData[i].asset}</a></td>
      <td>${tableData[i].sort_of}</td>
      <td class="text-end">${tableData[i].quantity}</td>
      <td class="text-end">${tableData[i].average_price}</td>
      <td class="text-end">${tableData[i].last_price}</td>
      <td class="text-end">${tableData[i].contribution}</td>
      <td class="text-end">${tableData[i].equity}</td>
      <td class="text-end">${tableData[i].earnings}</td>
      <td class="text-end">${tableData[i].yield}</td>
      <td class="text-end">${tableData[i].result} %</td>
      <td class="text-end">${tableData[i].yield_on_cost} %</td>
    </tr>`
    table.innerHTML += row;
  };
}

async function updatePortfolioSummary(URL) {
    try {
        const data = await getPortfolioSummaryData(URL)
        if (data) {
          buildTable(data.summary_data)
          let portfolioTable = new DataTable('#portfolioTable', {
              responsive: true,
              language: {
                decimal: ',',
                thousands: '.',
                zeroRecords: 'Não há dados',
                info: 'Mostrando página _PAGE_ de _PAGES_',
                infoEmpty: 'Não há dados',
                infoFiltered: '(dados filtrados de _MAX_ registros totais)',
                lengthMenu: 'Mostrar _MENU_ registros por página',
                zeroRecords: 'Não há dados',
                paginate: {
                    "first": "Primeiro",
                    "last": "Último",
                    "next": "Próximo",
                    "previous": "Anterior"
                },
                search: "Pesquisar:",
              },
              order: [[0, 'desc']],
              
          });       
        }
    } catch (error) {
        alert('Erro: ', error)
    }
};

updatePortfolioSummary(getPortfolioSummaryURL)
