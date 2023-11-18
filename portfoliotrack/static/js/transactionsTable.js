let table = new DataTable('#transactionsTable', {
    responsive: true,
    language: {
        decimal: ',',
        thousands: '.',
        info: 'Mostrando página _PAGE_ de _PAGES_',
        infoEmpty: 'Não há dados',
        infoFiltered: '(filtrados de _MAX_ registros totais)',
        lengthMenu: 'Mostrar _MENU_ registros por página',
        zeroRecords: 'Não há dados',
        paginate: {
            "first": "Primeiro",
            "last": "Último",
            "next": "Próximo",
            "previous": "Anterior"
        },
        search: "Pesquisar:",
        select: {
            rows: {
                _: '%d linhas selecionadas',
                0: 'Clique para selecionar',
                1: '%d linha selecionada',
            },
        },
        ordering: false,
    },
    select: true,
    

});

// obtem os dados selecionados da tabela
function sendListToDelete() {
    var selectedRows = table.rows({selected: true}).data()
    var arrayOfIDs = [];
    for (let i = 0; i < selectedRows.length; i++) {
        const ID = selectedRows[i][0]; // Posição 0 do array trata-se da coluna do ID da transação
        arrayOfIDs.push(parseInt(ID))
    }
    document.getElementById('idsInput').value = arrayOfIDs
    
}

function sendSingleIDToDelete(button) {
    var arrayOfIDs = []
    arrayOfIDs.push(parseInt(button.dataset.id))
    document.getElementById('idsInput').value = arrayOfIDs
}
