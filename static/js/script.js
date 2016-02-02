
$(document).ready(function() {
    $('.slider').slider({
        full_width: true
    });
// Initialize collapse button
$('.button-collapse').sideNav({
    menuWidth: 300, // Default is 240
    edge: 'left', // Choose the horizontal origin
    closeOnClick: true // Closes side-nav on <a> clicks, useful for Angular/Meteor
});
// Initialize collapsible (uncomment the line below if you use the dropdown variation)
$('.collapsible').collapsible();

$('.dropdown-button').dropdown({
    inDuration: 300,
    outDuration: 225,
    constrain_width: false, // Does not change width of dropdown to that of the activator
    hover: true, // Activate on hover
    gutter: 0, // Spacing from edge
    belowOrigin: false, // Displays dropdown below the button
    alignment: 'left' // Displays dropdown with edge aligned to the left of button
});
    $('.collapsible').collapsible({
        accordion: true // A setting that changes the collapsible behavior to expandable instead of the default accordion style

    });

    $('.modal-trigger').leanModal();
    $('.carousel').carousel();
    $('.parallax').parallax();
});


function additem(id) {
    document.form_additem.action = "/web/bucketlists/" + id + "/items/"
};

function editbucketlist(id, sname) {
    document.form_editbucketlist.name.value = sname
    document.form_editbucketlist.action = "/web/bucketlists/" + id + "/update"
}

function edititem(id, item, name, done) {
    document.form_edititem.name.value = name
    $('#textarea1').val(name);
    $('#textarea1').trigger('autoresize');
    var checked = false
    if (done == 'True') {
        checked = true
    }
    document.form_edititem.done.checked = checked
    document.form_edititem.action = "/web/bucketlists/" + id + "/items/" + item + "/update"

}

function deletelist(id,sname) {
     $("h5[name='name']").text("Delete: "+ sname +" ?")
    // document.form_deletelist.name.value = sname
    document.form_deletelist.action = "/web/bucketlists/" + id + "/delete"

}
function deleteitem(id,item,sname) {
     $("h5[name='itemname']").text("Delete: "+ sname +" ?")
   
    document.form_deleteitem.action = "/web/bucketlists/" + id + "/items/"+item+"/delete"

}


