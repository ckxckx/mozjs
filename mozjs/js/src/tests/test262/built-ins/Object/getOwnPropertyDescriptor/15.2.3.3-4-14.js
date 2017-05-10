// Copyright (c) 2012 Ecma International.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
es5id: 15.2.3.3-4-14
description: >
    Object.getOwnPropertyDescriptor returns data desc for functions on
    built-ins (Object.getPrototypeOf)
---*/

  var desc = Object.getOwnPropertyDescriptor(Object, "getPrototypeOf");

assert.sameValue(desc.value, Object.getPrototypeOf, 'desc.value');
assert.sameValue(desc.writable, true, 'desc.writable');
assert.sameValue(desc.enumerable, false, 'desc.enumerable');
assert.sameValue(desc.configurable, true, 'desc.configurable');

reportCompare(0, 0);
