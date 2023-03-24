$(document).ready(function () {
    console.log("DOCUMENT READY");
    // Set colours for task status
    setStatsPrios();


    // on change for is this a recurring task for both create and edit
    $('#formCreateTask').on('change', '#id_create_repeat', function() {
        toggleRepeatOptions($('#id_create_repeat'), 'create');
    })

    $('#formEditTask').on('change', '#id_edit_repeat', function() {
        toggleRepeatOptions($('#id_edit_repeat'), 'edit');
    })

    $('#tasksTable').DataTable(); //This needs to be at the end so that the formatting can be done first before the table is output
    $('#usersTable').DataTable(); //This needs to be at the end so that the formatting can be done first before the table is output
});


function setStatsPrios(){
    // Set colours for task status
    let tStats = $("#tasksTable .task-status");
    for (let i = 0; i < tStats.length; i++){
        setStatusColor($(tStats[i]));
    }

    let tPrios = $('#tasksTable .task-prio');
    for (let i = 0; i < tPrios.length; i++){
        setPrioColor($(tPrios[i]));
    }
}


function toggleRepeatOptions(repeatObj, actionType){
    intervalLength = $('#id_' + actionType + '_intervalLength');
    interval = $('#id_' + actionType + '_interval');
    divInterval = $('#id_' + actionType + '_repeat_interval');
    repeat = repeatObj;
    if(repeat.val() == "True"){
        console.log("Toggling")
        interval.prop('disabled', false);
        intervalLength.prop('disabled', false);
        divInterval.removeClass('d-none');
    } else{
        interval.prop('disabled', true);
        intervalLength.prop('disabled', true);
        divInterval.addClass('d-none');
    }
}

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

    // We will need to change the ID for these selectors because they are the same as the create_task form. We cannot have 2 elements with the same id
function showTaskInfo(tID, tName, tStatus, tCat, tUser, tPrio, tCreated, tDue, tDesc, tRepeat, tNote){
    $.ajax({
        url: 'mark_as_seen',
        type: 'get',
        data: {
            taskID: tID,
            tUID: tUser
        },
        success: (response) => {
            console.log(response);
        }
    });
    let note = $('#id_edit_note');
    let id = $('#id_edit_id');
    let desc = $('#id_edit_desc');
    let title = $('#modalHeaderViewTask');
    let user = $('#id_edit_assignedTo');
    let status = $('#id_edit_status');
    let name = $('#id_edit_name');
    let category = $('#id_edit_category')
    let prio = $('#id_edit_priority');
    let due = $('#id_edit_due');
    let repeat = $('#id_edit_repeat')
    let date = new Date(tDue);
    let dueDate = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
    note.val(tNote);
    id.val(tID);
    status.val(tStatus);
    desc.val(tDesc);
    title.html(tName);
    user.val(tUser);
    name.val(tName);
    category.val(tCat);
    prio.val(tPrio);
    due.val(dueDate);
    repeat.val(tRepeat);
}

function toggleEdit(){
    console.log("Toggling Edit");
    $('#id_edit_desc').prop("readonly", !$('#id_edit_desc').prop("readonly"));
    $('#id_edit_note').prop("readonly", !$('#id_edit_note').prop("readonly"));
    $('#id_edit_assignedTo').prop("disabled", !$('#id_edit_assignedTo').prop("disabled"));
    $('#id_edit_status').prop("disabled", !$('#id_edit_status').prop("disabled"));
    $('#id_edit_name').prop("disabled", !$('#id_edit_name').prop("disabled"));
    $('#id_edit_category').prop("disabled", !$('#id_edit_category').prop("disabled"));
    $('#id_edit_priority').prop("disabled", !$('#id_edit_priority').prop("disabled"));
    $('#id_edit_due').prop("disabled", !$('#id_edit_due').prop("disabled"));
    $('#id_edit_repeat').prop("disabled", !$('#id_edit_repeat').prop("disabled"));
    $('#save_edit').prop("disabled", !$('#save_edit').prop("disabled"));
}

function changeStatus(taskID, newStatusID, newStatusName){
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

// toggle being able to see password
var togglePassword = document.querySelector('#togglePassword');
var password = document.querySelector('#id_password');
togglePassword.addEventListener('click', function (e) {
    var type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.querySelector('i').classList.toggle('fa-eye');
    this.querySelector('i').classList.toggle('fa-eye-slash');
});

function enableEdit(){
    $("#id_first_name").removeAttr("disabled");
    $("#id_last_name").removeAttr("disabled");
    $("#id_email").removeAttr("disabled");
    $("#edit_user_save_button").removeAttr("disabled");
}

// function confirmDelete(username, url) {
//     if (window.confirm("Are you sure you want to delete user " + username + "?")) {
//         window.location.href = url;
//     } else {
//         alert("Delete action cancelled.");
//     }
// }
function confirmDelete(event, username, url) {
    event.preventDefault(); // prevent default link behavior
    if (window.confirm("Are you sure you want to delete user " + username + "?")) {
        window.location.href = url;
    } else {
        alert("Delete action cancelled.");
    }
}

function confirmSetManager(event, username, url) {
    event.preventDefault(); // prevent default link behavior
    if (window.confirm("Are you sure you want to set " + username + "as a manager?")) {
        window.location.href = url;
    } else {
        alert("Set manager cancelled.");
    }
}

// THIS FUNCTION IS NOT BEING USED. It is for ajax version of task nav menu
// function getTasks(filter){
//     $.ajax({
//         url: 'get_tasks',
//         type: 'get',
//         data: {
//             filter: filter
//         },
//         success: (response) => {
//             taskTable.clear();
//             $('#taskTable').html(response);
//             setStatsPrios();
//             taskTable.add(['Test Task', 'Complete', 'Programming', 'kevin', 'low', 'March 31, 2023', 'March 31, 2023', '']);
//             taskTable.draw();
//         }
//     });
// }