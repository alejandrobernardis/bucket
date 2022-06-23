
var _gaq = _gaq || [];
var _ga_loaded = false;
var _domains = [""];

_gaq.push(["_setAccount", "UA-1807788-3"]);
_gaq.push(['_setDomainName', 'none']);
_gaq.push(['_setAllowLinker', true]);
_gaq.push(['_setAllowHash', false]);
_gaq.push(function () {
    _ga_loaded = true;
});
_gaq.push(["_trackPageview"]);

(function () {
    var ga = document.createElement('script');
    ga.type = 'text/javascript';
    ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ga);
})();

$(document).ready(function () {
    var analyticsDomains = _domains;
    $("a").each(function () {
        var linkElement = $(this);
        var domainIndex = analyticsDomains.length;
        while (domainIndex--) {
            if (linkElement.attr("href").indexOf(analyticsDomains[domainIndex]) !== -1) {
                linkElement.click(function (event) {
                    _gaq.push(["_link", linkElement.attr("href")]);
                    if (_ga_loaded) event.preventDefault();
                });
                break;
            }
        }
    });
});

document.onclick = function (event) {
	
    event = event || window.event;
    
	var target = event.target || event.srcElement, 
		targetElement = target.tagName.toLowerCase();

    if (targetElement == "a") {
        var href = target.getAttribute("href"),
            urlHost = document.domain.replace(/^www\./i, "");
        var urlPattern = "^(?:https?:)?\/\/(?:(?:www)\.)?" + urlHost + "\/?";
        eventCheck(href, urlPattern);
    }

    function eventCheck(href, urlPattern) {
		if ((href.match(/^\/#.+/))){
			_gaq.push(['_trackEvent', 'Navegation', 'click', (document.domain + '' + href)]);
		} else if ((href.match(/^#.+/))){
			var u = (document.domain + '/' + location.pathname + '' + href).replace(/\/\//i, "/");
			_gaq.push(['_trackEvent', 'Navegation', 'click', u]);
		} else if ((href.match(/^https?\:/i)) && (!href.match(urlPattern))) {
            if (href.match(/^.*\.(pdf|jpg|png|gif|zip|mp3|txt|doc|rar|js|py)$/i)) {
                _gaq.push(['_trackEvent', 'Download', 'click', href]);
            } else {
                _gaq.push(['_trackEvent', 'External', 'click', href]);
            }
        } else if (href.match(/^mailto\:/i)) {
            _gaq.push(['_trackEvent', 'Email', 'click', href.substr(7)]);
        } else if (href.match(/^.*\.(pdf|jpg|png|gif|zip|mp3|txt|doc|rar|js|py)$/i)) {
            _gaq.push(['_trackEvent', 'Download', 'click', href]);
        }
    }

};