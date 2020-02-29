$(document).ready(function () {

    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    if ($('#calendar').length > 0) {
        $('#calendar').fullCalendar({
            header: {
                left: 'prev,next,today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            defaultView: "agendaDay",
            buttonText: {
                today: 'Back today'
            },

        });
    }

});