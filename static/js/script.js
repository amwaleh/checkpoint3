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

// Add items
function additem(id) {
  $("[name='form_additem']").prop('action',
    "/web/bucketlists/" + id + "/items/")
};
// edit lists
function editbucketlist(id, sname) {

  $("[name='name']").val(sname)
  $("[name='form_editbucketlist']").prop('action',
    "/web/bucketlists/" + id + "/update")
}
// update items
function edititem(id, item, name, done) {
  $("[name='name']").val(name)
  $('#textarea1').val(name);
  $('#textarea1').trigger('autoresize');
  var checked = false
  done = $("#complete").prop('checked')
  if (done == true) {
    checked = true
  }
  $("[name='done']").prop('checked', checked);
  $("[name='form_edititem']").prop('action',
    "/web/bucketlists/" + id + "/items/" + item + "/update")
}

function autoEditItem(id, item, name) {
  $("[name='name']").val(name)
  $('#textarea1').val(name);
  $('#textarea1').trigger('autoresize');
  var checked = false
  done = $("#complete").prop('checked')
  if (done == true) {
    checked = true
  }
  $("[name='done']").prop('checked', checked);
  $("[name='form_edititem']").prop('action',
    "/web/bucketlists/" + id + "/items/" + item + "/update")
  $("[name='form_edititem']").submit()
}

// delete lists
function deletelist(id, sname) {
  $("h5[name='name']").text("Delete: " + sname + " ?")
  $("[name='form_deletelist']").prop('action',
    "/web/bucketlists/" + id + "/delete")

}
// deleteitem
function deleteitem(id, item, sname) {
  $("h5[name='itemname']").text("Delete: " + sname + " ?")
  $("[name='form_deleteitem']").prop('action',
    "/web/bucketlists/" + id + "/items/" + item + "/delete")
}
