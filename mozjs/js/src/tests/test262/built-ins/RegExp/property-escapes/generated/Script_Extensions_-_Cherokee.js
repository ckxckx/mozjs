// Copyright 2017 Mathias Bynens. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
author: Mathias Bynens
description: >
  Unicode property escapes for `Script_Extensions=Cherokee`
info: |
  Generated by https://github.com/mathiasbynens/unicode-property-escapes-tests
  Unicode v9.0.0
  Emoji v5.0 (UTR51)
esid: sec-static-semantics-unicodematchproperty-p
features: [regexp-unicode-property-escapes]
includes: [regExpUtils.js]
---*/

const matchSymbols = buildString({
  loneCodePoints: [],
  ranges: [
    [0x0013A0, 0x0013F5],
    [0x0013F8, 0x0013FD],
    [0x00AB70, 0x00ABBF]
  ]
});
testPropertyEscapes(
  /^\p{Script_Extensions=Cherokee}+$/u,
  matchSymbols,
  "\\p{Script_Extensions=Cherokee}"
);
testPropertyEscapes(
  /^\p{Script_Extensions=Cher}+$/u,
  matchSymbols,
  "\\p{Script_Extensions=Cher}"
);
testPropertyEscapes(
  /^\p{scx=Cherokee}+$/u,
  matchSymbols,
  "\\p{scx=Cherokee}"
);
testPropertyEscapes(
  /^\p{scx=Cher}+$/u,
  matchSymbols,
  "\\p{scx=Cher}"
);

const nonMatchSymbols = buildString({
  loneCodePoints: [],
  ranges: [
    [0x00DC00, 0x00DFFF],
    [0x000000, 0x00139F],
    [0x0013F6, 0x0013F7],
    [0x0013FE, 0x00AB6F],
    [0x00ABC0, 0x00DBFF],
    [0x00E000, 0x10FFFF]
  ]
});
testPropertyEscapes(
  /^\P{Script_Extensions=Cherokee}+$/u,
  nonMatchSymbols,
  "\\P{Script_Extensions=Cherokee}"
);
testPropertyEscapes(
  /^\P{Script_Extensions=Cher}+$/u,
  nonMatchSymbols,
  "\\P{Script_Extensions=Cher}"
);
testPropertyEscapes(
  /^\P{scx=Cherokee}+$/u,
  nonMatchSymbols,
  "\\P{scx=Cherokee}"
);
testPropertyEscapes(
  /^\P{scx=Cher}+$/u,
  nonMatchSymbols,
  "\\P{scx=Cher}"
);

reportCompare(0, 0);
