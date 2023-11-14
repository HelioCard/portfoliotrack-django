var performance_options = {
    title: {
        text: 'Aportes Acum. x Patrimônio x Dividendos Acum.',
        left: 'center',
    },
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
        'data': ['Aportes Acumulados', 'Patrimônio', 'Dividendos Acumulados'],
        'top': 30,
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
            name: 'Aportes Acumulados',
            type: 'line',
            data: [0,0,0],
            smooth: false,
            step: 'end',
        },
    
        {
            name: 'Patrimônio',
            type: 'line',
            yAxisIndex: 0,
            data: [0,0,0],
            smooth: true,  
        },
        {
            name: 'Dividendos Acumulados',
            type: 'line',
            step: 'end',
            yAxisIndex: 0,
            data: [0,0,0],
            smooth: false,  
        }
    ]
}



var category_options = {
    title: {
        text: 'Exposição por Categorias',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: function (params) {
            var value = params.value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            return params.seriesName + '<br/>' + params.name + ': R$' + value + ' (' + params.percent + '%)';
        },
    },
    
    series: [
        {
            name: 'Portifolio por Categoria',
            type: 'pie',
            radius: ['40%', '60%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderJoin: 'round',
                borderRadius: '5%',
                borderCap: 'round',
                borderWidth: 2,
                borderColor: '#ffffff',
            },
            label: {
                show: true,
                position: 'outside',
                formatter: '{b}: {d}%',
            },
            emphasis: {
                label: {
                    show: true,
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: true,
            },
            data: {
                name: 'Não há dados',
                value: 100,
            },
        }
    ]
}




var asset_options = {
    title: {
        text: 'Exposição por Ativos',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: function (params) {
            var value = params.value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            return params.seriesName + '<br/>' + params.name + ': R$' + value + ' (' + params.percent + '%)';
        },
    },
    
    
    series: [
        {
            name: 'Portifolio por Ativos',
            type: 'pie',
            radius: ['40%', '60%'],
            avoidLabelOverlap: true,
            itemStyle: {
                borderJoin: 'round',
                borderRadius: '5%',
                borderCap: 'round',
                borderWidth: 2,
                borderColor: '#ffffff',
            },
            label: {
                show: true,
                position: 'outside',
                formatter: '{b}: {d}%',
            },
            emphasis: {
                label: {
                    show: true,
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: true,
            },
            data: {
                name: 'Não há dados',
                value: 100,
            },
        }
    ]
}

var contribution_options = {
    tooltip: {
        trigger: 'axis'
    },
    title: {
        text: 'Variação dos Ativos',
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
        colorBy: 'data',
        itemStyle: {
          opacity: 0.7,
          
        },
        emphasis: {
            itemStyle: {
                opacity: 1,
            },
        },
        markLine: {
            data: [{ type: 'average', name: 'Avg' }]
        },
      },
    ],
  };

  var asset_variation_options = {
    tooltip: {
        trigger: 'axis'
    },
    title: {
        text: 'Aportes Mensais',
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
        data: [100, 200, 150, 180, 70, 110, 195],
        type: 'bar',
        colorBy: 'series',
        itemStyle: {
          opacity: 0.7,
          
        },
        emphasis: {
            itemStyle: {
                opacity: 1,
            },
        },
        markLine: {
            data: [{ type: 'average', name: 'Avg' }]
        },
      },
    ],
  };
