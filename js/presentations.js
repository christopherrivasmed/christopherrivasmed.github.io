/* All-presentations page: filter by type (Talks / Posters) and search as you type.
   Without JavaScript the filters and search box stay hidden and everything is listed.
   Every word typed must appear in the title, venue, date, people, keywords or type.
   /presentations/?q=word and /presentations/?type=talks (or posters) pre-fill the controls. */
(function () {
  var wrap = document.getElementById("poster-search-wrap");
  var input = document.getElementById("poster-search");
  var count = document.getElementById("poster-count");
  var empty = document.getElementById("poster-empty");
  var filter = document.getElementById("kind-filter");
  var items = Array.prototype.slice.call(document.querySelectorAll("#poster-list > li"));
  if (!wrap || !input || !items.length) return;

  function norm(s) {
    s = s.toLowerCase();
    return s.normalize ? s.normalize("NFD").replace(/[\u0300-\u036f]/g, "") : s;
  }
  var haystacks = items.map(function (li) { return norm(li.getAttribute("data-search") || ""); });
  var kind = "all";

  function run() {
    var terms = norm(input.value).split(/\s+/).filter(Boolean);
    var shown = 0;
    items.forEach(function (li, i) {
      var ok = (kind === "all" || li.getAttribute("data-kind") === kind) &&
               terms.every(function (t) { return haystacks[i].indexOf(t) !== -1; });
      li.hidden = !ok;
      if (ok) shown++;
    });
    empty.hidden = shown > 0;
    count.hidden = !terms.length && kind === "all";
    count.textContent = "Showing " + shown + " of " + items.length;
  }

  function setKind(k) {
    kind = k;
    if (filter) {
      Array.prototype.forEach.call(filter.querySelectorAll(".chip"), function (b) {
        b.setAttribute("aria-pressed", b.getAttribute("data-kind") === k ? "true" : "false");
      });
    }
    run();
  }

  wrap.hidden = false;
  input.addEventListener("input", run);
  if (filter) {
    filter.hidden = false;
    filter.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (b) setKind(b.getAttribute("data-kind"));
    });
  }

  var params = new URLSearchParams(location.search);
  var q = params.get("q");
  var t = (params.get("type") || "").replace(/s$/, "");
  if (q) input.value = q;
  if (filter && (t === "talk" || t === "poster")) kind = t;
  setKind(kind);
})();
