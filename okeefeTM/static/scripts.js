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

function showTaskInfo(tName, tStatus, tCat, tUser, tPrio, tCreated, tDue, tDesc, tRepeat){
    let desc = $('#id_desc');
    let title = $('#modalHeaderViewTask');
    let user = $('#id_user');
    let status = $('#id_status');
    let name = $('#id_name');
    let category = $('#id_category')
    let prio = $('#id_priority');
    let due = $('#id_date_due');
    let repeat = $('#id_repeat')
    let date = new Date(tDue);
    let dueDate = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
    desc.val(tDesc);
    title.html(tName);
    user.val(tUser);
    name.val(tName);
    category.val(tCat);
    prio.val(tPrio);
    due.val(dueDate);
    repeat.val(tRepeat);
    name.prop("disabled", true);
    user.prop("disabled", true);
    category.prop("disabled", true);
    prio.prop("disabled", true);
    due.prop("disabled", true);
    repeat.prop("disabled", true);
    desc.prop("disabled", true);
}

function enableEdit(){
    $('#id_desc').prop("disabled", false);
    $('#modalHeaderViewTask').prop("disabled", false);
    $('#id_user').prop("disabled", false);
    $('#id_status').prop("disabled", false);
    $('#id_name').prop("disabled", false);
    $('#id_category').prop("disabled", false);
    $('#id_priority').prop("disabled", false);
    $('#id_date_due').prop("disabled", false);
    $('#id_repeat').prop("disabled", false);
}


function changeStatus(taskID, newStatusID, newStatusName){
    // TODO: Make AJAX request to send newStatus as the post
    $.ajax({
        url: 'update_task_status',
        type: 'get',
        data: {
            taskID: taskID,
            newStatusID: newStatusID
        },
        success: (response) => {
            let taskStatus = $("#task" + taskId + " .task-status");
            taskStatus.text(newStatusName + " ");
            setStatusColor(taskStatus);
            console.log(response);
        }
    });
}