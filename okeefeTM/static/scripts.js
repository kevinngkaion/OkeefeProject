$(document).ready(function () {
    // Set colours for task status
    let tStats = $("#tasksTable .task-status");
    for (let i = 0; i < tStats.length; i++){
        setStatusColor($(tStats[i]));
    }

    let tPrios = $('#tasksTable .task-prio');
    for (let i = 0; i < tPrios.length; i++){
        setPrioColor($(tPrios[i]));
    }

    $('#tasksTable').DataTable(); //This needs to be at the end so that the formatting can be done first before the table is output
});

function setStatusColor(tStat){// tStat is a jQuery obj
    // remove all btn colour styling first
    tStat.removeClass("btn-secondary btn-success btn-warning btn-danger");
    // remove all spaces in the text
    let statusTxt = tStat.text().replace(/\s+/g, "");
    switch(statusTxt){
        case "Unassigned":
            tStat.addClass('btn-secondary');
            break;
        case "Complete":
            tStat.addClass('btn-success');
            break;
        case "InProgress":
            tStat.addClass('btn-warning');
            break;
        case "NotStarted":
            tStat.addClass('btn-danger');
            break;
    }
}

function setPrioColor(tPrio){ //tPrio is a jQuery object
    // remove all the text color styling first
    tPrio.removeClass("text-success text-warning text-danger");
    switch(tPrio.text()){
        case "Low":
            tPrio.addClass('text-success');
            break;
        case "Medium":
            tPrio.addClass('text-warning');
            break;
        case "High":
            tPrio.addClass('text-danger');
            break;
    }
}

function showTaskInfo(name, description){
    let desc = $('#id_desc');
    $('#modalHeaderViewTask').text(name);
    $('#id_user').val(2); // 2 is kevin
    $('#id_user').prop("disabled", true);
    desc.val(description);
    desc.prop("disabled", true);

    // $('#task-info').text(description);
}

function enableEdit(){
    let desc = $('#id_desc');
    let assignedTo = $('#id_user');
    desc.prop("disabled", false);
    assignedTo.prop("disabled", false);
}

function changeStatus(taskId, newStatus){
    $.ajax({
        url: 'update_task_status',
        type: 'get',
        data: {
            taskId: taskId,
            newStatus: newStatus
        },
        success: (response) => {
            let taskStatus = $("#task" + taskId + " .task-status");
            taskStatus.text(newStatus + " ");
            setStatusColor(taskStatus);
            console.log(response);
        }
    });
}