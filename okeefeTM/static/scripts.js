$(document).ready(function () {
    let tStats = Object.values($('.task-status'))
    let tPrios = Object.values($('.task-prio'))
    tStats.forEach((tStat) => {
        switch(tStat.innerText){
            case "Unassigned ":
                tStat.classList.add('btn-secondary');
                break;
            case "Complete ":
                tStat.classList.add('btn-success');
                break;
            case "In Progress ":
                tStat.classList.add('btn-warning');
                break;
            case "Not Started ":
                tStat.classList.add('btn-danger');
                break;
        }
    })
    tPrios.forEach((tPrio) => {
        switch(tPrio.textContent){
            case "Low":
                tPrio.classList.add('text-success');
                break;
            case "Medium":
                tPrio.classList.add('text-warning');
                break;
            case "High":
                tPrio.classList.add('text-danger');
                break;
        }
    })
    $('#tasksTable').DataTable(); //This needs to be at the end so that the formatting can be done first before the table is output
});

function showTaskInfo(name, description){
    $('#modal-task-name').text(name);
    $('#task-info').text(description);
}

function changeStatus(newStatus){
    console.log(newStatus)
    // TODO: Make AJAX request to send newStatus as the post
}