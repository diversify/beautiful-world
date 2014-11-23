$(document).ready(function() {
    function playHandler(event) {
        var trackPreview = $(this).parent().find('.track-preview')[0];
        // Pause all the other songs
        $('.track-preview').each(function(i, audio) {
            if (audio != trackPreview) {
                audio.pause();
            }
        });

        // Play or pause the song
        if (trackPreview.paused) {
            trackPreview.play();
        } else {
            trackPreview.pause();
        }
        event.stopPropagation();
    }

    $(".submissions.main > li").click(function() {
        var submissionId = $(this).data('submission-id');
        var $photoPanel = $(this).find('.photo_panel');
        var photoPanel = $photoPanel[0];
        // Hide all photo panels except ours
        $('.photo_panel').each(function(i, panel) {
            if (panel != photoPanel) {
                $(panel).hide();
            }
        });
        // Open our photo panel if it's not already open
        if (!$photoPanel.is('visible')) {
            $photoPanel.load('/photo_panel/' + submissionId, function() {
                $photoPanel.show();
                $photoPanel.find('.play-button').click(playHandler);
            });
        }
    });

    $('.play-button').click(playHandler);

    // ...
});