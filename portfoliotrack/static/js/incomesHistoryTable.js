
function buildDomTable(tableData) {
    var table = document.querySelector('#tableBody');
    for (var i = 0; i < tableData.length; i++) {
        var row = `<tr class="align-middle" style="height: 60px;">
            <th class="text-center"><a href="#"> <span class="badge text-bg-primary w-75" style="font-size: 1.0rem;">${tableData[i].ticker}</span> </a></th>
            <td class="text-center">${tableData[i].date}</td>
            <td class="text-center">${tableData[i].value}</td>
            <td class="text-center">${tableData[i].dividend_yield.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})} %</td>
        </tr>`
        table.innerHTML += row;
    };
}

async function updateIncomesTable(URL) {
    try {
        document.querySelector('#spinner').hidden = false;
        const data = await getDataFromAPI(URL);
        if (data) {
            buildDomTable(data.incomes_history);
            let table = new DataTable('#incomesTable', {
                responsive: true,
                language: {
                    decimal: ',',
                    thousands: '.',
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
                ordering: true,
                order: [[1, 'desc']],
            
            });
        };
        document.querySelector('#spinner').hidden = true;
    } catch (error) {
        console.error(error)
        alert('Erro ao atualizar os dados!');
    };
};

updateIncomesTable(getIncomesHistoryURL)