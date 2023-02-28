$(document).ready(function () {
    $('#tasksTable').DataTable();


});

function showTaskInfo(name, description){
    $('#modal-task-name').text(name);
    $('#task-info').text(description);
}