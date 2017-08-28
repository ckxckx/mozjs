// Copyright 2017 Mathias Bynens. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
author: Mathias Bynens
description: >
  Unicode property escapes for `Script_Extensions=Hebrew`
info: |
  Generated by https://github.com/mathiasbynens/unicode-property-escapes-tests
  Unicode v9.0.0
  Emoji v5.0 (UTR51)
esid: sec-static-semantics-unicodematchproperty-p
features: [regexp-unicode-property-escapes]
includes: [regExpUtils.js]
---*/

const matchSymbols = buildString({
  loneCodePoints: [
    0x00FB3E
  ],
  ranges: [
    [0x000591, 0x0005C7],
    [0x0005D0, 0x0005EA],
    [0x0005F0, 0x0005F4],
    [0x00FB1D, 0x00FB36],
    [0x00FB38, 0x00FB3C],
    [0x00FB40, 0x00FB41],
    [0x00FB43, 0x00FB44],
    [0x00FB46, 0x00FB4F]
  ]
});
testPropertyEscapes(
  /^\p{Script_Extensions=Hebrew}+$/u,
  matchSymbols,
  "\\p{Script_Extensions=Hebrew}"
);
testPropertyEscapes(
  /^\p{Script_Extensions=Hebr}+$/u,
  matchSymbols,
  "\\p{Script_Extensions=Hebr}"
);
testPropertyEscapes(
  /^\p{scx=Hebrew}+$/u,
  matchSymbols,
  "\\p{scx=Hebrew}"
);
testPropertyEscapes(
  /^\p{scx=Hebr}+$/u,
  matchSymbols,
  "\\p{scx=Hebr}"
);

const nonMatchSymbols = buildString({
  loneCodePoints: [
    0x00FB37,
    0x00FB3D,
    0x00FB3F,
    0x00FB42,
    0x00FB45
  ],
  ranges: [
    [0x00DC00, 0x00DFFF],
    [0x000000, 0x000590],
    [0x0005C8, 0x0005CF],
    [0x0005EB, 0x0005EF],
    [0x0005F5, 0x00DBFF],
    [0x00E000, 0x00FB1C],
    [0x00FB50, 0x10FFFF]
  ]
});
testPropertyEscapes(
  /^\P{Script_Extensions=Hebrew}+$/u,
  nonMatchSymbols,
  "\\P{Script_Extensions=Hebrew}"
);
testPropertyEscapes(
  /^\P{Script_Extensions=Hebr}+$/u,
  nonMatchSymbols,
  "\\P{Script_Extensions=Hebr}"
);
testPropertyEscapes(
  /^\P{scx=Hebrew}+$/u,
  nonMatchSymbols,
  "\\P{scx=Hebrew}"
);
testPropertyEscapes(
  /^\P{scx=Hebr}+$/u,
  nonMatchSymbols,
  "\\P{scx=Hebr}"
);

reportCompare(0, 0);
