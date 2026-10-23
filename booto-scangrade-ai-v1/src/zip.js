/* ZIP sans dépendance (méthode STORE) : fichiers privés assemblés côté navigateur. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.ScanGradeZip = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const encoder = new TextEncoder();
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let j = 0; j < 8; j++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    table[n] = c >>> 0;
  }
  function crc32(bytes) { let c = -1; for (const b of bytes) c = table[(c ^ b) & 255] ^ (c >>> 8); return (c ^ -1) >>> 0; }
  function u16(view, p, x) { view.setUint16(p, x, true); }
  function u32(view, p, x) { view.setUint32(p, x >>> 0, true); }
  function le(size) { return new DataView(new ArrayBuffer(size)); }
  function zip(files) {
    if (!Array.isArray(files) || files.length > 2000) throw Error('Trop de fichiers');
    const locals = [], centrals = [];
    let offset = 0, dirLength = 0;
    for (const file of files) {
      if (!/^[A-Za-z0-9._/\[\]-]{1,140}$/.test(file.name) || file.name.includes('..') || file.name.startsWith('/')) throw Error('Nom de fichier non autorisé');
      const name = encoder.encode(file.name);
      const bytes = file.bytes instanceof Uint8Array ? file.bytes : encoder.encode(String(file.bytes));
      if (bytes.length > 0xffffffff) throw Error('Fichier trop grand');
      const crc = crc32(bytes);
      const local = le(30);
      u32(local, 0, 0x04034b50); u16(local, 4, 20); u16(local, 6, 0x0800); u16(local, 8, 0);
      u32(local, 14, crc); u32(local, 18, bytes.length); u32(local, 22, bytes.length); u16(local, 26, name.length);
      locals.push(new Uint8Array(local.buffer), name, bytes);
      const central = le(46);
      u32(central, 0, 0x02014b50); u16(central, 4, 20); u16(central, 6, 20); u16(central, 8, 0x0800);
      u32(central, 16, crc); u32(central, 20, bytes.length); u32(central, 24, bytes.length); u16(central, 28, name.length);
      u32(central, 42, offset);
      centrals.push(new Uint8Array(central.buffer), name);
      offset += 30 + name.length + bytes.length;
      dirLength += 46 + name.length;
    }
    const end = le(22);
    u32(end, 0, 0x06054b50); u16(end, 8, files.length); u16(end, 10, files.length);
    u32(end, 12, dirLength); u32(end, 16, offset);
    return new Blob([...locals, ...centrals, new Uint8Array(end.buffer)], {type: 'application/zip'});
  }
  return {crc32, zip};
});
