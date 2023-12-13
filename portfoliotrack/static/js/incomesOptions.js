
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
        name: 'Dividendos (R$)',
        position: 'left',
        axisLabel: {
          formatter: '{value}'
        },
        axisTick: {
          show: true,
          lineStyle: {
            color: "#cccccc",
          }
        },
      },
      {
        type: 'value',
        name: 'Yield on Cost (%)',
        position: 'right',
        axisLabel: {
          formatter: '{value}'
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
        name: 'Dividendos',
        type: 'bar',
        yAxisIndex: 0,
        data: [10, 52, 200, 334, 390, 330, 220],
        markLine: {
          data: [{ type: 'average', name: 'Média' }]
        }
      },
      {
        name: 'Yield on Cost',
        type: 'line',
        yAxisIndex: 1,
        smooth: false,
        data: [0.6, 0.9, 0.5, 0.4, 0.7, 0.6, 0.35],
        markLine: {
          data: [{ type: 'average', name: 'Média' }]
        }
      },
    ]
  };