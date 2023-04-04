$(document).ready(function () {
    console.log("DOCUMENT READY");
    // Set colours for task status
    setStatsPrios();

    // on change for is this a recurring task for both create and edit
    $('#formCreateTask').on('change', '#id_create_repeat', function () {
        toggleRepeatOptions($('#id_create_repeat'), 'create');
    })
    $('#formEditTask').on('change', '#id_edit_repeat', function () {
        toggleRepeatOptions($('#id_edit_repeat'), 'edit');
    })

    // if the two passwords do not match, show the error message
    $('#formCreateUser').on('keyup', '#id_create_password1, #id_create_password2', function () {
        let password1 = $("#id_create_password1").val();
        let password2 = $("#id_create_password2").val();
        if (validatePassword(password1)){
            checkPasswordMatch(password1, password2);
        }
    })

    // onclick listener for deleting task
    $('#id_delete_task_button').on('click', function(event){
        event.preventDefault(); // prevent the default behaviour of this element from executing
        let confirmed = confirm("Are you sure you want to delete this task?");
        if (confirmed){
            window.location.href = $(this).attr('href');
        }
    });

    // Custom sorting function to sort the dates
    $.fn.dataTable.ext.type.order['date-string-pre'] = function(date) {
        var parts = date.split(' ');
        var month = parts[0].substring(0, 3);
        var day = parts[1].replace(',', '');
        var year = parts[2];
        var monthIndex = {
          'Jan': 0,
          'Feb': 1,
          'Mar': 2,
          'Apr': 3,
          'May': 4,
          'Jun': 5,
          'Jul': 6,
          'Aug': 7,
          'Sep': 8,
          'Oct': 9,
          'Nov': 10,
          'Dec': 11
        }[month];
        return new Date(year, monthIndex, day).getTime();
      };

    // These instatiate the DataTables. These need to be at the end so that the formatting can be done first before the table is output
    $('#tasksTable').DataTable({
        columnDefs:[
            {type: 'date-string', targets: [5, 6]} // set the 5th and 6th column index to be a date-string type
        ]
    });
    $('#usersTable').DataTable();
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
function showTaskInfo(tID, tName, tStatus, tCat, tUser, tPrio, tCreated, tDue, tDesc, tRepeat, tNote, tInterval, tIntervalLength){
    console.log(tInterval);
    let isSeen = $('#id_task_isSeen');
    $.ajax({
        url: 'mark_as_seen',
        type: 'get',
        data: {
            taskID: tID,
        },
        statusCode: {
            200: (response) => {
                isSeen.html(response['msg']);
            },
            201: (response) => {
                isSeen.html(response['msg']);
            },
            204: (response) => {
                console.log("\nThis task has not yet been seen\n");
                isSeen.html('');
            }
        }
    });
    let due = $('#id_edit_due');
    let repeat = $('#id_edit_repeat');
    let date = new Date(tDue);
    let dueDate = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
    let intervalLength = parseInt(tIntervalLength);
    $('#id_edit_note').val(tNote);
    $('#id_edit_id').val(tID);
    $('#id_edit_status').val(tStatus);
    $('#id_edit_desc').val(tDesc);
    $('#modalHeaderViewTask').html(tName);
    $('#id_edit_assignedTo').val(tUser);
    $('#id_edit_name').val(tName);
    $('#id_edit_category').val(tCat);
    $('#id_edit_priority').val(tPrio);
    due.val(dueDate);
    repeat.val(tRepeat);
    $('#id_delete_task_button').attr('href', 'delete_task?id=' + tID);
    $('#id_edit_interval').val(tInterval);
    $('#id_edit_intervalLength').val(intervalLength);
    $('#id_edit_repeat_interval').removeClass("d-none");
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
    $('#id_edit_interval').prop("disabled", !$('#id_edit_interval').prop("disabled"));
    $('#id_edit_intervalLength').prop("disabled", !$('#id_edit_intervalLength').prop("disabled"));
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
            let taskStatus = $("#task" + taskID + " .task-status");
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

function validatePassword(password){
    // Do something to check password validity
    return true;
}

function checkPasswordMatch(password1, password2){
    let saveButton = $("#id_create_user_save");
    let errorMessage = $("#id_password_error");
    if (password1 === password2){
        errorMessage.addClass("d-none");
        saveButton.removeAttr("disabled");
    } else {
        errorMessage.removeClass("d-none");
        saveButton.attr("disabled", "disabled");
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
