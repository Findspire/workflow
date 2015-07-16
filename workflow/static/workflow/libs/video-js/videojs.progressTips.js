/*! videojs-progressTips - v0.1.0 - 2013-09-16
* https://github.com/mickey/videojs-progressTips
* Copyright (c) 2013 Michael Bensoussan; Licensed MIT */

(function() {

  vjs.plugin('progressTips', function(options) {
    var init;
    init = function() {
      var player;
      if (this.techName !== "Html5") {
        return;
      }
      player = this;
      $(".vjs-progress-control").after("<div id='vjs-tip'><div id='vjs-tip-arrow'></div><div id='vjs-tip-inner'></div></div>");
      $(".vjs-progress-control").on("mousemove", function(event) {
        var minutes, seconds, seekBar, timeInSeconds, tip, progressControl, x, y;
        seekBar = player.controlBar.progressControl.seekBar;
        timeInSeconds = seekBar.calculateDistance(event) * seekBar.player_.duration();
        if (timeInSeconds === seekBar.player_.duration()) {
          timeInSeconds = timeInSeconds - 0.1;
        }
        minutes = Math.floor(timeInSeconds / 60);
        seconds = Math.floor(timeInSeconds - minutes * 60);
        if (seconds < 10) {
          seconds = "0" + seconds;
        }
        $('#vjs-tip-inner').html("" + minutes + ":" + seconds);
        tip = $('#vjs-tip');
        progressControl = $('.vjs-progress-control');
        x = event.pageX - (tip.outerWidth() / 2) - (progressControl.offset().left - progressControl.position().left);
        y = -tip.outerHeight();
        $("#vjs-tip").css({
            left: "" + x + "px",
            top: "" + y + "px",
            visibility: "visible"
        });
        return;
      });
      $(".vjs-progress-control, .vjs-play-control").on("mouseout", function() {
        $("#vjs-tip").css("visibility", "hidden");
      });
    };
    this.on("loadedmetadata", init);
  });

}).call(this);
