
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
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
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
        data: [10, 52, 200, 334, 390, 330, 220],
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
      yAxisIndex: 0,
      smooth: false,
      data: [0.6, 0.9, 0.5, 0.4, 0.7, 0.6, 0.35],
      markLine: {
        data: [{type: 'average', name: 'Média' }],
      },
      smooth: true,
    },
  ]
};