/* Poster search for posters/index.html: filters the tiles as you type.
   Without JavaScript the search box stays hidden and every poster is listed.
   Every word typed must appear in the poster's title, conference, date, authors or keywords. */
(function () {
  var wrap = document.getElementById("poster-search-wrap");
  var input = document.getElementById("poster-search");
  var count = document.getElementById("poster-count");
  var empty = document.getElementById("poster-empty");
  var items = Array.prototype.slice.call(document.querySelectorAll("#poster-list > li"));
  if (!wrap || !input || !items.length) return;

  function norm(s) {
    s = s.toLowerCase();
    return s.normalize ? s.normalize("NFD").replace(/[̀-ͯ]/g, "") : s;
  }
  var haystacks = items.map(function (li) { return norm(li.getAttribute("data-search") || ""); });

  function run() {
    var terms = norm(input.value).split(/\s+/).filter(Boolean);
    var shown = 0;
    items.forEach(function (li, i) {
      var ok = terms.every(function (t) { return haystacks[i].indexOf(t) !== -1; });
      li.hidden = !ok;
      if (ok) shown++;
    });
    empty.hidden = shown > 0;
    count.hidden = !terms.length;
    count.textContent = "Showing " + shown + " of " + items.length + " posters";
  }

  wrap.hidden = false;
  input.addEventListener("input", run);
  var q = new URLSearchParams(location.search).get("q");   // /posters/?q=word pre-fills the search
  if (q) { input.value = q; run(); }
})();
