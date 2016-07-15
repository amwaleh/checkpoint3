$(document).ready(function () {
    myApp.init();
});
var myApp = {};
myApp = {
    //initialize the dom
    init: function () {
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
        $(document).ready(function () {

            scaleVideoContainer();

            initBannerVideoSize('.video-container .poster img');
            initBannerVideoSize('.video-container .filter');
            initBannerVideoSize('.video-container video');

            $(window).on('resize', function () {
                scaleVideoContainer();
                scaleBannerVideoSize('.video-container .poster img');
                scaleBannerVideoSize('.video-container .filter');
                scaleBannerVideoSize('.video-container video');
            });

        });

        function scaleVideoContainer() {

            var height = $(window).height() + 5;
            var unitHeight = parseInt(height) + 'px';
            $('.homepage-hero-module').css('height', unitHeight);

        }

        function initBannerVideoSize(element) {

            $(element).each(function () {
                $(this).data('height', $(this).height());
                $(this).data('width', $(this).width());
            });

            scaleBannerVideoSize(element);

        }

        function scaleBannerVideoSize(element) {

            var windowWidth = $(window).width(),
                windowHeight = $(window).height() + 5,
                videoWidth,
                videoHeight;


            $(element).each(function () {
                var videoAspectRatio = $(this).data('height') / $(this).data('width');

                $(this).width(windowWidth);

                if (windowWidth < 1000) {
                    videoHeight = windowHeight;
                    videoWidth = videoHeight / videoAspectRatio;
                    $(this).css({
                        'margin-top': 0,
                        'margin-left': -(videoWidth - windowWidth) / 2 + 'px'
                    });

                    $(this).width(videoWidth).height(videoHeight);
                }

                $('.homepage-hero-module .video-container video').addClass('fadeIn animated');

            });
        }

    },
    // Add items
    addItem: function (id) {
        $("[name='form_additem']").prop("action",
            "/bucketlists/" + id + "/items/");
    },
    // edit lists
    editBucketlist: function (id, sname) {
        $("[name='name']").val(sname)
        $("[name='form_editbucketlist']").prop("action",
            "/bucketlists/" + id + "/update");
    },
    // update items
    editItem: function (id, item, name, done) {
        $("[name='form_edititem'] [name='name']").val(name);
        $("#textarea1").val(name);
        $("#textarea1").trigger("autoresize");
        var checked = false
        console.log(done)
        if (done == 'True') {
            checked = true;
        }
        ;
        $("[name='done']").prop("checked", checked);
        $("[name='form_edititem']").prop("action",
            "/bucketlists/" + id + "/items/" + item + "/update");

    },
    autoEditItem: function (id, item, name, done) {
        var lid = id
        $("[name='form_edititem'] [name='name']").val(name);
        $("[name='name']").val(name);
        $("#textarea1").val(name);

        var checked = false

        if (done === 'False') {
            checked = true;
        }
        console.log(lid)
        $("[name='done']").prop("checked", checked);
        $("[name='form_edititem']").prop("action",
            "/bucketlists/" + lid + "/items/" + item + "/update");
        $("[name='form_edititem']").submit();

    },

    // delete lists
    deleteList: function (id, sname) {
        $("h5[name='name']").text("Delete: " + sname + " ?");
        $("[name='form_deletelist']").prop("action",
            "/bucketlists/" + id + "/delete");

    },
    // deleteitem
    deleteItem: function (id, item, sname) {
        $("h5[name='itemname']").text("Delete: " + sname + " ?");
        $("[name='form_deleteitem']").prop("action",
            "/bucketlists/" + id + "/items/" + item + "/delete");
    },
};
