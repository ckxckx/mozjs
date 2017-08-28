// Copyright 2017 Mathias Bynens. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
author: Mathias Bynens
description: >
  Unicode property escapes for `Script=Oriya`
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
    [0x000B01, 0x000B03],
    [0x000B05, 0x000B0C],
    [0x000B0F, 0x000B10],
    [0x000B13, 0x000B28],
    [0x000B2A, 0x000B30],
    [0x000B32, 0x000B33],
    [0x000B35, 0x000B39],
    [0x000B3C, 0x000B44],
    [0x000B47, 0x000B48],
    [0x000B4B, 0x000B4D],
    [0x000B56, 0x000B57],
    [0x000B5C, 0x000B5D],
    [0x000B5F, 0x000B63],
    [0x000B66, 0x000B77]
  ]
});
testPropertyEscapes(
  /^\p{Script=Oriya}+$/u,
  matchSymbols,
  "\\p{Script=Oriya}"
);
testPropertyEscapes(
  /^\p{Script=Orya}+$/u,
  matchSymbols,
  "\\p{Script=Orya}"
);
testPropertyEscapes(
  /^\p{sc=Oriya}+$/u,
  matchSymbols,
  "\\p{sc=Oriya}"
);
testPropertyEscapes(
  /^\p{sc=Orya}+$/u,
  matchSymbols,
  "\\p{sc=Orya}"
);

const nonMatchSymbols = buildString({
  loneCodePoints: [
    0x000B04,
    0x000B29,
    0x000B31,
    0x000B34,
    0x000B5E
  ],
  ranges: [
    [0x00DC00, 0x00DFFF],
    [0x000000, 0x000B00],
    [0x000B0D, 0x000B0E],
    [0x000B11, 0x000B12],
    [0x000B3A, 0x000B3B],
    [0x000B45, 0x000B46],
    [0x000B49, 0x000B4A],
    [0x000B4E, 0x000B55],
    [0x000B58, 0x000B5B],
    [0x000B64, 0x000B65],
    [0x000B78, 0x00DBFF],
    [0x00E000, 0x10FFFF]
  ]
});
testPropertyEscapes(
  /^\P{Script=Oriya}+$/u,
  nonMatchSymbols,
  "\\P{Script=Oriya}"
);
testPropertyEscapes(
  /^\P{Script=Orya}+$/u,
  nonMatchSymbols,
  "\\P{Script=Orya}"
);
testPropertyEscapes(
  /^\P{sc=Oriya}+$/u,
  nonMatchSymbols,
  "\\P{sc=Oriya}"
);
testPropertyEscapes(
  /^\P{sc=Orya}+$/u,
  nonMatchSymbols,
  "\\P{sc=Orya}"
);

reportCompare(0, 0);
