/* BOOTO ScanGrade AI · moteurs purs de capture · aucune donnée d'élève */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.ScanGradeCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const VERSION = 'booto.scangrade.scan.v0';
  function meanDifference(a, b) {
    if (!a || !b || a.length !== b.length || !a.length) return 1;
    let sum = 0;
    for (let i = 0; i < a.length; i++) sum += Math.abs(a[i] - b[i]);
    return sum / (a.length * 255);
  }
  function sampleLuma(rgba) {
    const result = new Uint8Array(rgba.length / 4);
    for (let i = 0, j = 0; i < rgba.length; i += 4, j++) {
      result[j] = Math.round(0.2126 * rgba[i] + 0.7152 * rgba[i + 1] + 0.0722 * rgba[i + 2]);
    }
    return result;
  }
  function captureSide(pageNumber, duplex) {
    if (!Number.isInteger(pageNumber) || pageNumber < 1) throw new Error('Numéro de page invalide');
    return duplex ? {sheet: Math.ceil(pageNumber / 2), side: pageNumber % 2 ? 'recto' : 'verso'} : {sheet: pageNumber, side: 'recto'};
  }
  function anonymousId(n) { return 'C' + String(n).padStart(3, '0'); }
  function safeTrimestre(t) { return ['T1', 'T2', 'T3'].includes(t) ? t : 'T1'; }
  // Déclenchement conservateur : une première photo manuelle est indispensable.
  // Une nouvelle photo automatique nécessite mouvement, stabilisation et changement visible.
  class PageGate {
    constructor(options = {}) {
      this.motion = options.motion ?? 0.034;
      this.still = options.still ?? 0.013;
      this.changed = options.changed ?? 0.018;
      this.stillFor = options.stillFor ?? 1350;
      this.reset();
    }
    reset() {
      this.previous = null;
      this.baseline = null;
      this.sawMotion = false;
      this.stableSince = null;
      this.ready = false;
    }
    onCaptured(sample) {
      this.baseline = new Uint8Array(sample);
      this.previous = new Uint8Array(sample);
      this.sawMotion = false;
      this.stableSince = null;
      this.ready = false;
    }
    update(sample, atMs) {
      if (!sample || !sample.length || !Number.isFinite(atMs)) return false;
      if (!this.baseline) { this.previous = new Uint8Array(sample); return false; }
      const d = meanDifference(this.previous, sample);
      this.previous = new Uint8Array(sample);
      if (d >= this.motion) { this.sawMotion = true; this.stableSince = null; this.ready = false; return false; }
      if (!this.sawMotion) return false;
      if (d > this.still) { this.stableSince = null; return false; }
      if (this.stableSince === null) this.stableSince = atMs;
      if (atMs - this.stableSince < this.stillFor) return false;
      if (meanDifference(this.baseline, sample) < this.changed) return false;
      if (this.ready) return false;
      this.ready = true;
      return true;
    }
  }
  return { VERSION, meanDifference, sampleLuma, captureSide, anonymousId, safeTrimestre, PageGate };
});
