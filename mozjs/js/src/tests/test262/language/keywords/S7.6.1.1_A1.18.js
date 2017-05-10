// |reftest| error:ReferenceError
// Copyright 2009 the Sputnik authors.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
info: The "this" token can not be used as identifier
es5id: 7.6.1.1_A1.18
description: Checking if execution of "this=1" fails
negative:
  phase: early
  type: ReferenceError
---*/

this = 1;
