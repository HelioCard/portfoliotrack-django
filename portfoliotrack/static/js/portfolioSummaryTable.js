// Obter dados da API
const getPortfolioSummaryData = async (url) => {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.Erro === 'No data') {
          alert('Possivelmente ainda não há dados de transações. Adicione suas transações no menu à esquerda!');
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

function buildDomTable(tableData) {
  var table = document.getElementById('tableBody');
  for (var i = 0; i < tableData.length; i++){
    var yieldColor = parseFloat(tableData[i].yield) >= 0 ? 'text-success' : 'text-danger';
    var resultColor = parseFloat(tableData[i].result) >= 0 ? 'text-success' : 'text-danger';
    var assetColor = parseFloat(tableData[i].result) >= 0 ? 'text-bg-primary' : 'text-bg-danger';
    var row = `<tr class="align-middle" style="height: 60px">
      <td><a href="#"> <span class="badge ${assetColor} w-100" style="font-size: 1.0rem;">${tableData[i].asset}</span> </a></td>
      <td class="text-center">${tableData[i].sort_of}</td>
      <td class="text-end">${tableData[i].quantity}</td>
      <td class="text-end">${tableData[i].average_price}</td>
      <td class="text-end">${tableData[i].last_price}</td>
      <td class="text-end">${tableData[i].contribution}</td>
      <td class="text-end">${tableData[i].equity}</td>
      <td class="text-end">${tableData[i].earnings}</td>
      <td class="text-end ${yieldColor}">${tableData[i].yield}</td>
      <td class="text-end ${resultColor}">${tableData[i].result}%</td>
      <td class="text-end">${tableData[i].yield_on_cost}%</td>
    </tr>`
    table.innerHTML += row;
  };
}


let portfolioSummaryTable

async function updatePortfolioSummary(URL) {
    try {
        document.querySelector('#spinner').hidden = false;
        const data = await getPortfolioSummaryData(URL)
        if (data) {
          buildDomTable(data.summary_data)
          const portfolioSummaryTableElement = document.getElementById('portfolioTable')
          // Confere se a tabela já foi inicializada:
          if (!portfolioSummaryTableElement.hasAttribute('data-datatable-initialized')) {
            portfolioSummaryTable = new DataTable('#portfolioTable', {
              responsive: true,
              language: {
                decimal: ',',
                thousands: '.',
                zeroRecords: 'Não há dados',
                info: 'Mostrando página _PAGE_ de _PAGES_',
                infoEmpty: 'Não há dados',
                infoFiltered: '(dados filtrados de _MAX_ registros totais)',
                lengthMenu: 'Mostrar _MENU_ registros por página',
                paginate: {
                    "first": "Primeiro",
                    "last": "Último",
                    "next": "Próximo",
                    "previous": "Anterior"
                },
                search: "Pesquisar:",
              },
              order: [[0, 'asc']],
            });
            portfolioSummaryTableElement.setAttribute('data-datatable-initialized', 'true'); //Adiciona atributo para indicar que a tabela não foi inicializada
          } 
        };
        document.querySelector('#spinner').hidden = true;
    } catch (error) {
        alert('Erro: ', error)
    }
};

updatePortfolioSummary(getPortfolioSummaryURL)
