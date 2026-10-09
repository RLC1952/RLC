/* RLC CMS-Inhaltslader: laedt Datendateien aus assets/data/ und injiziert sie.
   Einbindung (pro Datendatei ein Tag, mehrfach pro Seite moeglich):
     <script src="../assets/js/cms_content.js?v=1"
             data-cms-src="../assets/data/team.json" data-cms-page="team"></script>
   Ablauf: fetch -> window.rlcCmsData[page] = data -> generische Injektion
   ([data-cms] Text, [data-cms-html] HTML, [data-cms-img] Bild {src,alt,copyright},
   [data-cms-href] Linkziel) -> Event 'rlc:cms-data' {detail:{page,data}}.
   Pfad-Konvention in den JSON-Dateien: root-relativ OHNE fuehrenden Slash
   (z.B. "pages/team.html", "assets/images/x.jpg"); CMS-Uploads liefern "/..."
   -- beides wird zu Domain-Root aufgeloest und funktioniert auf allen Seiten. */
(function () {
    'use strict';
    var script = document.currentScript;
    var src = script && script.getAttribute('data-cms-src');
    var page = script && script.getAttribute('data-cms-page');
    if (!src || !page) {
        return;
    }

    fetch(new URL(src, document.baseURI), { credentials: 'same-origin' })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            return response.json();
        })
        .then(function (data) {
            window.rlcCmsData = window.rlcCmsData || {};
            window.rlcCmsData[page] = data;
            inject(data);
            document.dispatchEvent(new CustomEvent('rlc:cms-data', { detail: { page: page, data: data } }));
        })
        .catch(function (error) {
            console.warn('RLC CMS: Inhalte fuer "' + page + '" konnten nicht geladen werden.', error);
        });

    function resolve(path, root) {
        return path.split('.').reduce(function (node, key) {
            return node === undefined || node === null ? undefined : node[key];
        }, root);
    }

    function rootPath(value) {
        if (typeof value !== 'string' || !value) {
            return value;
        }
        return value.charAt(0) === '/' || value.indexOf('://') > -1 ? value : '/' + value;
    }

    function inject(data) {
        document.querySelectorAll('[data-cms]').forEach(function (el) {
            var value = resolve(el.getAttribute('data-cms'), data);
            if (typeof value === 'string') {
                el.textContent = value;
            }
        });
        document.querySelectorAll('[data-cms-html]').forEach(function (el) {
            var value = resolve(el.getAttribute('data-cms-html'), data);
            if (typeof value === 'string') {
                el.innerHTML = value;
            }
        });
        document.querySelectorAll('[data-cms-img]').forEach(function (el) {
            var value = resolve(el.getAttribute('data-cms-img'), data);
            if (value && typeof value === 'object') {
                if (value.src) {
                    el.setAttribute('src', rootPath(value.src));
                }
                if (value.alt !== undefined) {
                    el.setAttribute('alt', value.alt);
                }
            }
        });
        document.querySelectorAll('[data-cms-href]').forEach(function (el) {
            var value = resolve(el.getAttribute('data-cms-href'), data);
            if (typeof value === 'string' && value) {
                el.setAttribute('href', rootPath(value));
            }
        });
    }
}());