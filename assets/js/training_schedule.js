/* Trainingsdaten-Lader: liest assets/data/training.json (CMS-pflegbar) und
   stellt die Daten allen Verbraucherseiten bereit (training, team, facilities).
   Konsum: window.rlcTrainingData {meta, groups} bzw. kompatibel weiter:
   window.trainingSchedule (Array) + window.trainingScheduleMeta (Objekt).
   Verbraucherseiten hoeren auf das Event 'rlc:training-data' (oder booten
   sofort, wenn die Daten schon da sind). */
(function () {
    'use strict';
    var script = document.currentScript;
    var src = (script && script.getAttribute('data-training-src')) || '../assets/data/training.json';

    fetch(new URL(src, document.baseURI), { credentials: 'same-origin' })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            return response.json();
        })
        .then(function (data) {
            var groups = Array.isArray(data.groups) ? data.groups : [];
            window.rlcTrainingData = { meta: data.meta || {}, groups: groups };
            window.trainingSchedule = groups;
            window.trainingScheduleMeta = data.meta || {};
            document.dispatchEvent(new CustomEvent('rlc:training-data', { detail: window.rlcTrainingData }));
        })
        .catch(function (error) {
            console.warn('RLC: Trainingsdaten konnten nicht geladen werden.', error);
        });
}());