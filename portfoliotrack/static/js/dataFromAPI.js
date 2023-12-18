// Obter dados da API
const getDataFromAPI = async (url) => {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.Erro === 'No data') {
          alert('Possivelmente ainda não há dados de transações ou posições abertas. Adicione suas transações no menu à esquerda!');
          showNoData()
        } else {
          throw new Error(`Erro: ${errorData.Erro}`);
        }
      } else {
        return await response.json();
      }
    } catch (ex) {
      console.error(ex)
      alert('Erro ao buscar os dados!');
    }
};