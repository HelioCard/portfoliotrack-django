var data = [
    {
        asset: "AESB3",
        sort_of:   "Ações",
        quantity:     "2000",
        average_price: "12,00",
        last_price:     "13,80",
        contribution:       "50.000,00",
        equity: "52.800,00",
        earnings:     "0,00",
        yield:       "2.800,00",
        result: "5 %",
        yield_on_cost:     "0 %",
    },
    {
        asset:       "TRPL4",
        sort_of:   "Ações",
        quantity:     "1500",
        average_price: "22,00",
        last_price:     "23,63",
        contribution:       "60.000,00",
        equity: "65.000,00",
        earnings:     "3.000,00",
        yield:       "8.000,00",
        result: "10 %",
        yield_on_cost:     "6 %",
    }
]

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

    data: data,
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
});


