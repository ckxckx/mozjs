// Copyright (c) 2012 Ecma International.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
es5id: 15.2.3.2-2-8
description: >
    Object.getPrototypeOf returns the [[Prototype]] of its parameter
    (Math)
---*/

assert.sameValue(Object.getPrototypeOf(Math), Object.prototype, 'Object.getPrototypeOf(Math)');

reportCompare(0, 0);
