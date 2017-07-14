/* This Source Code Form is subject to the terms of the Mozilla Wlic
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
#![feature(test)]
#[macro_use]
extern crate js;
extern crate libc;
extern crate test;

use js::rust::{Runtime, SIMPLE_GLOBAL_CLASS};
use js::rust;
use js::debug::{val_to_str, puts};
use js::jsapi::root::JS;
use js::jsapi::root::{JS_NewGlobalObject, JS_InitClass, JSScript, JS_DefineFunction,};
use js::jsapi::root::JS::CompartmentOptions;
use js::jsapi::root::JS::OnNewGlobalHookOption;
use js::jsapi::root::JS_ExecuteScript;
use js::jsval::UndefinedValue;
use js::magicdom::attr::ATTR_CLASS;
use js::magicdom::attr::ATTR_PS_ARR;
use js::magicdom::attr::Attr_constructor;
use js::magicdom::element::ELEMENT_CLASS;
use js::magicdom::element::ELEMENT_PS_ARR;
use js::magicdom::element::ELEMENT_FN_ARR;
use js::magicdom::element::Element_constructor;
use js::magicdom::htmlelement::HTMLELEMENT_CLASS;
use js::magicdom::htmlelement::HTMLELEMENT_PS_ARR;
use js::magicdom::htmlelement::HtmlElement_constructor;
use js::magicdom::node::NODE_CLASS;
use js::magicdom::node::NODE_PS_ARR;
use js::magicdom::node::NODE_FN_ARR;
use js::magicdom::node::Node_constructor;
use test::Bencher;

use std::ptr;

#[bench]
fn bench_htmlelement_getattributes_js(_b: &mut Bencher) {
    let rt = Runtime::new().unwrap();
    let cx = rt.cx();

    unsafe {
        rooted!(in(cx) let global =
                JS_NewGlobalObject(cx, &SIMPLE_GLOBAL_CLASS, std::ptr::null_mut(),
                                   OnNewGlobalHookOption::FireOnNewGlobalHook,
                                   &CompartmentOptions::default())
        );

        let _ac = js::ac::AutoCompartment::with_obj(cx, global.get());

        rooted!(in(cx) let proto = ptr::null_mut());

        rooted!(in(cx) let node_proto =
                JS_InitClass(cx, global.handle(), proto.handle(), &NODE_CLASS, Some(Node_constructor),
                             6, NODE_PS_ARR.as_ptr(), NODE_FN_ARR.as_ptr(),
                             std::ptr::null(), std::ptr::null())
        );

        rooted!(in(cx) let element_proto =
                JS_InitClass(cx, global.handle(), node_proto.handle(), &ELEMENT_CLASS, Some(Element_constructor),
                             12, ELEMENT_PS_ARR.as_ptr(), ELEMENT_FN_ARR.as_ptr(),
                             std::ptr::null(), std::ptr::null())
        );

        rooted!(in(cx) let _attr_proto =
                JS_InitClass(cx, global.handle(), node_proto.handle(),
                             &ATTR_CLASS, Some(Attr_constructor),
                             11, ATTR_PS_ARR.as_ptr(), std::ptr::null(),
                             std::ptr::null(), std::ptr::null())
        );

        rooted!(in(cx) let _html_element_proto =
                JS_InitClass(cx, global.handle(), element_proto.handle(),
                             &HTMLELEMENT_CLASS, Some(HtmlElement_constructor),
                             22, HTMLELEMENT_PS_ARR.as_ptr(), std::ptr::null(),
                             std::ptr::null(), std::ptr::null())
        );

        let print_function = JS_DefineFunction(cx, global.handle(), b"puts\0".as_ptr() as *const libc::c_char,
                                               Some(puts), 1, 0);
        assert!(!print_function.is_null());
        let to_str_function = JS_DefineFunction(cx, global.handle(), b"val_to_str\0".as_ptr() as *const libc::c_char,
                                                Some(val_to_str), 1, 0);
        assert!(!to_str_function.is_null());

        JS::SetWarningReporter(cx, Some(rust::report_warning));

        rooted!(in(cx) let mut rval = UndefinedValue());
        rooted!(in(cx) let mut script = ptr::null_mut() as *mut JSScript);
        let _ = rt.compile_script(global.handle(), r#"
var duration;
function bench(num) {
    let attr1 = new Attr(1, "Node", "mozilla/en", false, "n", "h1", [], "la", "a", "l", "p", "f");
    let attr2 = new Attr(1, "Node2", "mozilla/en", false, "n", "h1", [], "lb", "b", "l", "p", "b");
    let element1 = new HtmlElement(1, "Node", "mozilla/en", false, "n", "h1", [], "la", "a", "l", "pp",
    "foo", [attr1, attr2], "title123", "en", false, "dir12345", false, 1, "ackeylab", "ackeylab", false, false);
    let attr3 = new Attr(1, "Node3", "mozilla/es", false, "n", "h1", [], "lc", "c", "l", "p", "f");
    let attr4 = new Attr(1, "Node4", "mozilla/es", false, "n", "h1", [], "ld", "d", "l", "p", "b");
    let element2 = new HtmlElement(1, "Node2", "mozilla/es", false, "n", "h1", [], "lb", "b", "l", "pp",
    "bar", [attr3, attr4], "title456", "es", false, "dir", false, 1, "ackey", "ackey456", false, false);
    var t1 = Date.now();
    var ret;
    for ( var i = 0; i < num; i++) {
        ret = element2.getAttributes("p:lc");
    }
    duration = Date.now() - t1;
}
bench(102400);
puts("");
puts("getattribute time is");
puts(val_to_str(duration));
"#,
                                  "test", 22, script.handle_mut());
        JS_ExecuteScript(cx, script.handle(), rval.handle_mut());
    }
}
