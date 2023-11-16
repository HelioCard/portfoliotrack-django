let table = new DataTable('#transactionsTable', {
    responsive: true,
    language: {
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
    },
    
});