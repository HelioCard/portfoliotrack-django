
var fractionOptions = {
    legend: {
        top: '5%',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: function (params) {
            return params.seriesName + '<br/>' + params.name + ': ' + params.value + ' %';
        },
    },  
    
    series: [
        {
            name: 'Andamento',
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
                position: 'center',
                formatter: '{b} {d}%',
            },
            emphasis: {
                label: {
                    show: false,
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false,
            },
            data: [
                { value: 0, name: 'Concluído' },
                { value: 100, name: 'Pendente', itemStyle: {color: '#e2e0e5'} },
            ]
        }
    ]
};
