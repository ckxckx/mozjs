// Copyright 2017 Mathias Bynens. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
author: Mathias Bynens
description: >
  Unicode property escapes for `Script=Inscriptional_Pahlavi`
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
    [0x010B60, 0x010B72],
    [0x010B78, 0x010B7F]
  ]
});
testPropertyEscapes(
  /^\p{Script=Inscriptional_Pahlavi}+$/u,
  matchSymbols,
  "\\p{Script=Inscriptional_Pahlavi}"
);
testPropertyEscapes(
  /^\p{Script=Phli}+$/u,
  matchSymbols,
  "\\p{Script=Phli}"
);
testPropertyEscapes(
  /^\p{sc=Inscriptional_Pahlavi}+$/u,
  matchSymbols,
  "\\p{sc=Inscriptional_Pahlavi}"
);
testPropertyEscapes(
  /^\p{sc=Phli}+$/u,
  matchSymbols,
  "\\p{sc=Phli}"
);

const nonMatchSymbols = buildString({
  loneCodePoints: [],
  ranges: [
    [0x00DC00, 0x00DFFF],
    [0x000000, 0x00DBFF],
    [0x00E000, 0x010B5F],
    [0x010B73, 0x010B77],
    [0x010B80, 0x10FFFF]
  ]
});
testPropertyEscapes(
  /^\P{Script=Inscriptional_Pahlavi}+$/u,
  nonMatchSymbols,
  "\\P{Script=Inscriptional_Pahlavi}"
);
testPropertyEscapes(
  /^\P{Script=Phli}+$/u,
  nonMatchSymbols,
  "\\P{Script=Phli}"
);
testPropertyEscapes(
  /^\P{sc=Inscriptional_Pahlavi}+$/u,
  nonMatchSymbols,
  "\\P{sc=Inscriptional_Pahlavi}"
);
testPropertyEscapes(
  /^\P{sc=Phli}+$/u,
  nonMatchSymbols,
  "\\P{sc=Phli}"
);

reportCompare(0, 0);
