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
          type: 'line',
          step: 'end',
          data: [0,0,0],
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                offset: 0,
                color: 'rgba(0, 102, 150, 0.2)'
                },
                {
                offset: 1,
                color: 'rgba(0, 102, 150, 0.05)'
                }
            ])
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
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
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
      type: 'value',
      name: 'Aportes (R$)',
      position: 'left',
      axisLabel: {
        formatter: function (value) {
          return value.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
        }
      },
      axisTick: {
        show: true,
        lineStyle: {
          color: "#cccccc",
        }
      },
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
            data: [{ type: 'average', name: 'Média' }]
        },
      },
    ],
};





var incomesOptions = {
    title: {
      subtext: 'Histórico dos dividendos ao longo do tempo',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: function (params) {
        const value = params.value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const date = params.name
        const name = 'Dividendos:'
        return name + '<br/>' + date + ': R$ ' + value
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: ['-', '-', '-', '-', '-', '-', '-'],
        axisTick: {
          alignWithLabel: true
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: 'Dividendos (R$)',
        position: 'left',
        axisLabel: {
          formatter: function (value) {
            return value.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
          }
        },
        axisTick: {
          show: true,
          lineStyle: {
            color: "#cccccc",
          }
        },
      },
    ],
    series: [
      {
        name: 'Dividendos',
        type: 'bar',
        yAxisIndex: 0,
        data: [0, 0, 0, 0, 0, 0, 0],
        markLine: {
          data: [{ type: 'average', name: 'Média' }]
        }
      },
    ]
  };
  
  


  
  var yieldOptions = {
    title: {
      subtext: 'Histórico do dividend yeld ao longo do tempo',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: function (params) {
        const value = params.value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const date = params.name
        const name = 'Yield on Cost:'
        return name + '<br/>' + date + ': ' + value + '%'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        axisTick: {
          alignWithLabel: true
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: 'Yield on Cost (%)',
        position: 'left',
        axisLabel: {
          formatter: function (value) {
            return value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
          }
        },
        axisTick: {
          show: true,
          lineStyle: {
            color: "#cccccc",
          }
        },
      }
    ],
    series: [
      {
        name: 'Yield on Cost',
        type: 'line',
        step: 'end',
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
              offset: 0,
              color: 'rgba(0, 102, 150, 0.2)'
              },
              {
              offset: 1,
              color: 'rgba(0, 102, 150, 0.05)'
              }
          ])
        },
        yAxisIndex: 0,
        smooth: false,
        data: [0.6, 0.9, 0.5, 0.4, 0.7, 0.6, 0.35],
        markLine: {
          data: [{type: 'average', name: 'Média' }],
        },
      },
    ]
  };