document.addEventListener("DOMContentLoaded", function () {
    // sidenav initialization
    let sideNav = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sideNav);

    // modal initialization
    let modalElements = document.querySelectorAll('.modal');
    M.Modal.init(modalElements);

    // datapicker initialization
    let datePicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datePicker, {
        format: "dd mmmm, yyyy",
        i18n: {done: "Select"}
    });

    // select initialization
    let selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);

    // collapsibles initialization
    let collapsibles = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsibles);
});
