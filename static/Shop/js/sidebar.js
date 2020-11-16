$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {

        // $(body)
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
    });
});
