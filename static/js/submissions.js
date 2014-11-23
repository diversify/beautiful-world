$(document).ready(function() {
    console.log("Hejsan!");
    $(".submissions.main > li").click(function() {
        var submissionId = $(this).data('submission-id');
        // Hide all photo panels
        $('.photo_panel').hide();
        // Open our photo panel
        var photoPanel = $(this).find('.photo_panel');
        console.log(photoPanel);
        photoPanel.load('/photo_panel/' + submissionId, function() {
            photoPanel.show();
        });

    });
    // ...
});