import 'ol/ol.css';
import IIIF from 'ol/source/IIIF';
import IIIFInfo from 'ol/format/IIIFInfo';
import Map from 'ol/Map';
import TileLayer from 'ol/layer/Tile';
import View from 'ol/View';
import iro from '@jaames/iro';
import 'normalize.css';
import '@fontsource/open-sans';
import iiifLogo from './assets/iiif.png';

const defaultUrl = 'https://sammlungen.uni-goettingen.de/api/v1/records/record_DE-MUS-062622_kenom_127703/files/images/record_DE-MUS-062622_kenom_127703_vs.jpg/info.json';

const layer = new TileLayer(),
    map = new Map({
        layers: [layer],
        target: 'map'
    }),
    notifyDiv = document.getElementById('iiif-notification'),
    urlInput = document.getElementById('imageInfoUrl'),
    displayButton = document.getElementById('display'),
    selectQuality = document.getElementById('qualitySelect'),
    selectFormat = document.getElementById('formatSelect'),
    hexInput = document.getElementById('hexInput'),
    rewriteBox = document.getElementById('rewriteBox'),
    rewriteInfo = document.getElementById('rewriteInfo'),
    iiifLink = document.getElementById('iiifLink'),
    urlParams = new URLSearchParams(window.location.search),
    params = Object.fromEntries(urlParams.entries());

// Taken from https://millankaul.medium.com/how-to-handle-404-500-and-more-using-fetch-api-in-javascript-f4e301925a51 to get around JS Design flaw.
function manageErrors(response) {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}

function handleLoad() {
    notifyDiv.textContent = '';
    notifyDiv.parentElement.style.display = 'none';
    if (!rewriteBox.checked) {
        refreshMap(urlInput.value, iiifFormat, iiifQuality);
    } else {
        if (typeof window.rewriteURL !== 'undefined') {
            var rewrittenUrl = window.rewriteURL(urlInput.value);
            rewrittenUrl.replace(/\/full\/full\/0\/default.jpg/g, "/info.json")
            rewriteInfo.innerHTML = 'Rewritten URL is: <span class="url">' + rewrittenUrl + '</span>';
            rewriteInfo.style.display = 'block';
            refreshMap(rewrittenUrl, iiifFormat, iiifQuality);
        }
    }
}

function createIiifLink(url) {
    return '<a href="' + url + '"><img src="' + iiifLogo + '" alt="Link to info.json" target="_blank" crossorigin/></a>';
}

function refreshMap(imageInfoUrl, iiifFormat, iiifQuality) {
    fetch(imageInfoUrl)
        .then(manageErrors)
        .then(function(response) {
            response
                .json()
                .then(function(imageInfo) {
                    iiifInfo = new IIIFInfo(imageInfo)
                    var options = iiifInfo.getTileSourceOptions();

                    //TODO this doesn't work yet
                    if (iiifFormat !== undefined) {
                        options['format'] = iiifFormat;
                    }
                    if (iiifQuality !== undefined) {
                        options['quality'] = iiifQuality;
                    }

                    if (options === undefined || options.version === undefined) {
                        notifyDiv.textContent =
                            'Data seems to be no valid IIIF image information.';
                        return;
                    }
                    options.zDirection = -1;
                    const iiifTileSource = new IIIF(options);

                    addTileSouceToMap(iiifTileSource);

                    var availableQualities = imageInfo.profile[1].qualities;
                    if (!availableQualities.includes(options.quality)) {
                        availableQualities.push(options.quality);
                    }
                    var availableFormats = imageInfo.profile[1].formats;

                    selectQuality.innerHTML = '';
                    if (availableQualities.length > 1) {
                        for (let i = 0; i < availableQualities.length; i++) {
                            var opt = document.createElement('option');
                            opt.value = availableQualities[i];
                            opt.innerHTML = availableQualities[i].charAt(0).toUpperCase() + availableQualities[i].slice(1);
                            if (availableQualities[i] == options.quality) {
                                opt.setAttribute('selected', '');
                            }
                            selectQuality.appendChild(opt);
                        }
                        selectQuality.parentElement.style.display = 'block';
                    } else {
                        selectQuality.parentElement.style.display = 'none';
                    }

                    selectFormat.innerHTML = '';
                    for (let i = 0; i < availableFormats.length; i++) {
                        var opt = document.createElement('option');
                        opt.value = availableFormats[i];
                        opt.innerHTML = availableFormats[i].toUpperCase();
                        if (availableFormats[i] == options.format) {
                            opt.setAttribute('selected', 'selected');
                        }
                        selectFormat.appendChild(opt);
                    }

                    map.getView().fit(iiifTileSource.getTileGrid().getExtent());
                    notifyDiv.textContent = '';
                    notifyDiv.parentElement.style.display = 'none';

                    iiifLink.innerHTML = createIiifLink(imageInfoUrl);
                    iiifLink.style.display = 'block';
                })
                .catch(function(body) {
                    notifyDiv.textContent = 'Could not read image info json. ' + body;
                    notifyDiv.parentElement.style.display = 'flex';
                });
        })
        .catch(function() {
            notifyDiv.textContent = 'Could not read data from URL.';
            notifyDiv.parentElement.style.display = 'flex';
        });
}

function addTileSouceToMap(source) {
    layer.setSource(source);
    map.setView(
        new View({
            resolutions: source.getTileGrid().getResolutions(),
            extent: source.getTileGrid().getExtent(),
            constrainOnlyCenter: true
        })
    );
}


function changeFormatQuality(format, quality) {

    var options;
    if (iiifFormat === undefined && iiifQuality === undefined) {
        options = iiifInfo.getTileSourceOptions();
        iiifFormat = options.format;
        iiifQuality = options.quality;
    }

    options = iiifInfo.getTileSourceOptions({
        "format": format,
        "quality": quality
    });
    if (options === undefined || options.version === undefined) {
        notifyDiv.textContent =
            "Data seems to be no valid IIIF image information.";
        return;
    }
    options.zDirection = -1;
    const iiifTileSource = new IIIF(options);

    addTileSouceToMap(iiifTileSource);
    map.getView().fit(iiifTileSource.getTileGrid().getExtent());
}


displayButton.addEventListener('click', function() {
    handleLoad();
});

urlInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        handleLoad();
    }
});

selectFormat.addEventListener('change', function(event) {
    var newFormat = event.target.value;
    changeFormatQuality(newFormat, selectQuality.value);
});

selectQuality.addEventListener('change', function(event) {
    var newQuality = event.target.value;
    changeFormatQuality(selectFormat.value, newQuality);
});

if (Object.keys(params).length && params.format != '' && params.quality != '') {
    iiifFormat = params.format;
    iiifQuality = params.quality;
}

if (typeof window.rewriteURL === 'undefined') {
    rewriteBox.disabled = true;
} else {
    rewriteBox.checked = true;
}

if (urlInput.value == '') {
    if (Object.keys(params).length && (typeof params.url !== 'undefined' || typeof params.id !== 'undefined')) {
        if (typeof params.id !== 'undefined' && params.id != '') {
            urlInput.value = params.id;
        } else {
            urlInput.value = params.url;
        }
        handleLoad();
    } else {
        urlInput.value = defaultUrl;
    }
}

var iiifInfo, iiifQuality, iiifFormat;

refreshMap(urlInput.value);

var colorPicker = new iro.ColorPicker('#picker', {
    color: 'rgb(31, 58, 113)',
    borderWidth: 1,
    borderColor: '#fff',
});
colorPicker.on(['color:init', 'color:change'], function(color) {
    document.body.style.backgroundColor = color.hexString;
    hexInput.value = color.hexString;

})
hexInput.addEventListener('change', function() {
    colorPicker.color.hexString = this.value;
});
