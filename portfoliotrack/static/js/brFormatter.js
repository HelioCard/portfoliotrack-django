function formatNumber(number) {
    return number.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

function formatTooltip(formatter) {
    return function (params) {
      var tooltip = params[0].name + "<br>";
      params.forEach(function (param) {
        tooltip += param.seriesName + ": R$" + formatNumber(param.value) + "<br>";
      });
      return tooltip;
    };
  }