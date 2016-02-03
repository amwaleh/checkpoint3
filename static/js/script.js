$(document).ready(function() {
    myApp.init
});
var myApp = {};
myApp = {
    //initialize the dom
    init: (function() {
        $('.slider').slider({
            full_width: true
        });
        // Initialize collapse button
        $('.modal-trigger').leanModal();
        $('.carousel').carousel();
        $('.parallax').parallax();
        // Initialize collapsible (
        $('.button-collapse').sideNav({
            // Default is 240
            menuWidth: 300,
            // Choose the horizontal origin
            edge: 'left',
            // Closes side-nav on <a> clicks, useful for Angular/Meteor
            closeOnClick: true
        });

        $('.collapsible').collapsible();
        $('.dropdown-button').dropdown({
            inDuration: 300,
            outDuration: 225,
            // Does not change width of dropdown to that of the activator
            constrain_width: false,
            // Activate on hover
            hover: true,
            // Spacing from edge
            gutter: 0,
            // Displays dropdown below the button
            belowOrigin: false,
            // Displays dropdown with edge aligned to the left of button
            alignment: 'left'
        });
        $('.collapsible').collapsible({
            accordion: true
        });

    }()),
    // Add items
    additem: function(id) {
        $("[name='form_additem']").prop("action",
            "/bucketlists/" + id + "/items/");
    },
    // edit lists
    editbucketlist: function(id, sname) {
        $("[name='name']").val(sname)
        $("[name='form_editbucketlist']").prop("action",
            "/bucketlists/" + id + "/update");
    },
    // update items
    edititem: function(id, item, name, done) {
        $("[name='form_edititem'] [name='name']").val(name);
        $("#textarea1").val(name);
        $("#textarea1").trigger("autoresize");
        var checked = false
        done = $("#complete").prop("checked");
        if (done == true) {
            checked = true;
        };
        $("[name='done']").prop("checked", checked);
        $("[name='form_edititem']").prop("action",
            "/bucketlists/" + id + "/items/" + item + "/update");

    },
    autoEditItem: function(id, item, name) {
        $("[name='name']").val(name);
        $("#textarea1").val(name);
        $("#textarea1").trigger("autoresize");
        var checked = false
        done = $("#complete").prop("checked");
        if (done == true) {
            checked = true;
        }
        $("[name='done']").prop("checked", checked);
        $("[name='form_edititem']").prop("action",
            "/bucketlists/" + id + "/items/" + item + "/update");
        $("[name='form_edititem']").submit();
    },

    // delete lists
    deletelist: function(id, sname) {
        $("h5[name='name']").text("Delete: " + sname + " ?");
        $("[name='form_deletelist']").prop("action",
            "/bucketlists/" + id + "/delete");

    },
    // deleteitem
    deleteitem: function(id, item, sname) {
        $("h5[name='itemname']").text("Delete: " + sname + " ?");
        $("[name='form_deleteitem']").prop("action",
            "/bucketlists/" + id + "/items/" + item + "/delete");
    },
};
