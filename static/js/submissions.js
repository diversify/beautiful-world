$(document).ready(function() {
    function playHandler(event) {
        var $button = $(this);
        var trackPreview = $button.parent().find('.track-preview')[0];
        // Pause all the other songs
        $('.track-preview').each(function(i, audio) {
            if (audio != trackPreview) {
                audio.pause();
            }
        });

        $('.track-preview').parent().find('.play-button').removeClass('glyphicon-pause');
        $('.track-preview').parent().find('.play-button').addClass('glyphicon-start');

        // Play or pause the song
        if (trackPreview.paused) {
            $button.removeClass('glyphicon-start');
            $button.addClass('glyphicon-pause');
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
        if ($photoPanel.is('visible')) {
            $photoPanel.hide();
        } else {
            $photoPanel.load('/photo_panel/' + submissionId, function() {
                $photoPanel.show();
                $photoPanel.find('.play-button').click(playHandler);
            });
        }
    });

    $('.play-button').click(playHandler);

    // ...
});