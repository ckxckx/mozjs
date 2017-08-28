// Copyright 2017 Mathias Bynens. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
author: Mathias Bynens
description: >
  Unicode property escapes for `Script=Hiragana`
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
    0x01B001,
    0x01F200
  ],
  ranges: [
    [0x003041, 0x003096],
    [0x00309D, 0x00309F]
  ]
});
testPropertyEscapes(
  /^\p{Script=Hiragana}+$/u,
  matchSymbols,
  "\\p{Script=Hiragana}"
);
testPropertyEscapes(
  /^\p{Script=Hira}+$/u,
  matchSymbols,
  "\\p{Script=Hira}"
);
testPropertyEscapes(
  /^\p{sc=Hiragana}+$/u,
  matchSymbols,
  "\\p{sc=Hiragana}"
);
testPropertyEscapes(
  /^\p{sc=Hira}+$/u,
  matchSymbols,
  "\\p{sc=Hira}"
);

const nonMatchSymbols = buildString({
  loneCodePoints: [],
  ranges: [
    [0x00DC00, 0x00DFFF],
    [0x000000, 0x003040],
    [0x003097, 0x00309C],
    [0x0030A0, 0x00DBFF],
    [0x00E000, 0x01B000],
    [0x01B002, 0x01F1FF],
    [0x01F201, 0x10FFFF]
  ]
});
testPropertyEscapes(
  /^\P{Script=Hiragana}+$/u,
  nonMatchSymbols,
  "\\P{Script=Hiragana}"
);
testPropertyEscapes(
  /^\P{Script=Hira}+$/u,
  nonMatchSymbols,
  "\\P{Script=Hira}"
);
testPropertyEscapes(
  /^\P{sc=Hiragana}+$/u,
  nonMatchSymbols,
  "\\P{sc=Hiragana}"
);
testPropertyEscapes(
  /^\P{sc=Hira}+$/u,
  nonMatchSymbols,
  "\\P{sc=Hira}"
);

reportCompare(0, 0);
