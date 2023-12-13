var incomesOptions = {
    legend: {
      data: ['Dividendos', 'Yield on Cost']
    },
    tooltip: {
      trigger: 'axis',
      
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
        position: 'left',
        axisLabel: {
          formatter: 'R$ {value}'
        }
      },
      {
        type: 'value',
        position: 'right',
        axisLabel: {
          formatter: '{value} %'
        }
      }
    ],
    series: [
      {
        name: 'Dividendos',
        type: 'bar',
        yAxisIndex: 0,
        data: [10, 52, 200, 334, 390, 330, 220]
      },
      {
        name: 'Yield on Cost',
        type: 'line',
        yAxisIndex: 1,
        smooth: false,
        data: [0.6, 0.9, 0.5, 0.4, 0.7, 0.6, 0.35]
      },
    ]
  };