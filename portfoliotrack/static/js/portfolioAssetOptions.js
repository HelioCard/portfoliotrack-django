var performance_options = {
    // title: {
    //     text: 'Aportes x Patrimônio x Dividendos',
    //     left: 'center',
    // },
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
            var formattedTooltip = '<strong>' + params[0].name + '</strong>' + '<br>';
            params.forEach(function (param) {
                var color = param.color; // Obtém a cor da série
                var value = param.value.toLocaleString('pt-BR'); // Formata o valor
                formattedTooltip += '<span style="color:' + color + ';">●</span> ' + param.seriesName + ': ' + '<strong>' + 'R$'+  value + '</strong>' + '<br>';
            });
            return formattedTooltip;
        },
    },
    legend: {
        'data': ['Aportes', 'Patrimônio', 'Dividendos'],
        'top': 10,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },

    xAxis: {
        type: 'category',
        data: ['-','-','-'],
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            formatter: function (value) {
                return value.toLocaleString('pt-BR');
            }
        },
    },
    series: [    
        {
            name: 'Aportes',
            type: 'bar',
            data: [0,0,0],
            itemStyle: {
                opacity: 1,
                },
            emphasis: {
                itemStyle: {
                    opacity: 0.6,
                },
            },
        },
    
        {
            name: 'Patrimônio',
            type: 'line',
            yAxisIndex: 0,
            data: [0,0,0],
            smooth: true,  
        },
        {
            name: 'Dividendos',
            type: 'line',
            step: 'end',
            yAxisIndex: 0,
            data: [0,0,0],
            smooth: false,  
        }
    ]
};





var contribution_options = {
    tooltip: {
        trigger: 'item',
        formatter: function (params) {
            var value = params.value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            return 'Mês ' + params.name + '<br/>' + 'Aporte: R$' + value;
        },
    },
    title: {
        subtext: 'Valor dos aportes mensais ao longo do tempo',
        left: 'center',
    },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [120, 200, 150, -100, 70, 110, 130],
        type: 'bar',
        colorBy: 'series',
        itemStyle: {
          opacity: 1,
          
        },
        emphasis: {
            itemStyle: {
                opacity: 0.6,
            },
        },
        markLine: {
            data: [{ type: 'average', name: 'Avg' }]
        },
      },
    ],
};


