async function checkProcessTransactionsStatus(){
    const response = await fetch(checkProcessRawTransactionsStatusURL);
    const data = await response.json();
    
    if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
        window.location.href = redirectDashboardURL
    } else {
        setTimeout(
            () => checkProcessTransactionsStatus(),
            2000,
            );
    }
}

checkProcessTransactionsStatus()
