async function checkTasksStatus(){
    const response = await fetch(checkTasksStatusURL);
    const data = await response.json();
    
    if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
        window.location.href = redirectURL
    } else {
        setTimeout(
            () => checkTasksStatus(),
            2000,
            );
    }
}

checkTasksStatus()
