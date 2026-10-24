/* Talk pages: the video is a thumbnail until it is tapped, so nothing is requested from YouTube
   until then (fast on slow Wi-Fi, no third-party scripts or cookies up front).
   Tapping the thumbnail, or any chapter, loads the player (youtube-nocookie.com) and starts it there.
   Without JavaScript these are ordinary links that open the video on YouTube. */
(function () {
  var box = document.getElementById("video");
  if (!box) return;
  var id = box.getAttribute("data-video-id");
  var title = box.getAttribute("data-title") || "Video";
  var frame = null;

  function play(start) {
    var src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0" + (start ? "&start=" + start : "");
    if (!frame) {
      frame = document.createElement("iframe");
      frame.title = title;
      frame.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      frame.referrerPolicy = "strict-origin-when-cross-origin";
      box.innerHTML = "";
      box.appendChild(frame);
      box.classList.add("is-playing");
    }
    frame.src = src;
  }

  box.addEventListener("click", function (e) {
    if (e.target.closest(".video-facade")) {
      e.preventDefault();
      play(0);
    }
  });

  var links = document.querySelectorAll(".chapters a[data-start]");
  Array.prototype.forEach.call(links, function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      play(parseInt(a.getAttribute("data-start"), 10) || 0);
      Array.prototype.forEach.call(links, function (o) { o.removeAttribute("aria-current"); });
      a.setAttribute("aria-current", "true");
      box.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
})();
