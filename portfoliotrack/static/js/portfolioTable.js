let portfolioTable = new DataTable('#portfolioTable', {
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
        select: {
            rows: {
                _: '%d linhas selecionadas',
                0: 'Clique para selecionar. Segure Ctrl ou Shift para selecionar várias.',
                1: '%d linha selecionada',
            },
        },
    },
    order: [[0, 'desc']],
    info: false,
    searching: false,
    paging: false,
    select: false,

});


