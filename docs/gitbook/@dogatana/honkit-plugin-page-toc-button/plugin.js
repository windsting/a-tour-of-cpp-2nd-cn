var gitbook = window.gitbook;
var options = {};

gitbook.events.bind('start', function (e, config) {
    // Save config data
    options = config['page-toc-button'] || {};

});

gitbook.events.on('page.change', function () {
    // Default config values
    let _maxTocDepth = 2;
    let _minTocSize = 2;
    let _icon = '<i class="fa fa-bars" aria-hidden="true"></i>';


    // Read out config data
    if (options) {
        _maxTocDepth = options.maxTocDepth ? options.maxTocDepth : _maxTocDepth;
        _minTocSize = options.minTocSize ? options.minTocSize : _minTocSize;
        _icon = options.icon ? options.icon : _icon;
    }

    // Search for headers
    var headerArray = $(".book .body-inner .markdown-section :header");

    // Init variables
    const tocArray = [];
    let tocSize = 0;

    // For each header...
    for (let i = 0; i < headerArray.length; i++) {

        const headerElement = headerArray[i];
        const header = $(headerElement);
        const headerId = header.attr("id");

        if ((typeof headerId !== typeof undefined) && (headerId !== false)) {

            switch (headerElement.tagName) {
                case "H1":
                    tocArray.push({
                        name: header.text(),
                        url: headerId,
                        children: []
                    });
                    tocSize++;
                    break;
                case "H2":
                    if ((tocArray.length > 0) && (_maxTocDepth >= 1)) {
                        tocArray[tocArray.length - 1].children.push({
                            name: header.text(),
                            url: headerId,
                            children: []
                        });
                        tocSize++;
                    };
                    break;
                case "H3":
                    if ((tocArray.length > 0) && (_maxTocDepth >= 2)) {
                        if (tocArray[tocArray.length - 1].children.length > 0) {
                            tocArray[tocArray.length - 1].children[tocArray[tocArray.length - 1].children.length - 1].children.push({
                                name: header.text(),
                                url: headerId,
                                children: []
                            });
                            tocSize++;
                        };
                    };
                    break;
                default:
                    break;
            }
        }
    }

    // Cancel if not enough headers to show
    if ((tocSize == 0) || (tocSize < _minTocSize)) {
        return;
    }

    // Generate html for button and menu
    let html = '<div class="page-toc-button">' + _icon + '<div class="page-toc-menu"><ul>';
    for (let i = 0; i < tocArray.length; i++) {
        html += "<li><a href='#" + tocArray[i].url + "'>" + tocArray[i].name + "</a></li>";
        if (tocArray[i].children.length > 0) {
            html += "<ul>"
            for (let j = 0; j < tocArray[i].children.length; j++) {
                html += "<li><a href='#" + tocArray[i].children[j].url + "'>" + tocArray[i].children[j].name + "</a></li>";
                if (tocArray[i].children[j].children.length > 0) {
                    html += "<ul>"
                    for (let k = 0; k < tocArray[i].children[j].children.length; k++) {
                        html += "<li><a href='#" + tocArray[i].children[j].children[k].url + "'>" + tocArray[i].children[j].children[k].name + "</a></li>";
                    }
                    html += "</ul>"
                }
            }
            html += "</ul>"
        }
    }
    html += "</ul></div></div>";

    // Append generated html to page
    $(".book").append(html)

});
