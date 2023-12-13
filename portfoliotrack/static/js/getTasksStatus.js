async function checkTasksStatus(){
    try {
        const response = await fetch(checkTasksStatusURL);
        const data = await response.json();
        
        if (data.status !== 'PENDING') {
            window.location.href = redirectURL
        } else {
            setTimeout(
                () => checkTasksStatus(),
                2000,
                );
        }
    } catch (ex) {
        console.error(ex)
        alert('Erro ao verificar o status de processamento de transações!')
    }
}

checkTasksStatus()
