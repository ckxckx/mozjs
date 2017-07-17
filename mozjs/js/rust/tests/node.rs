/* This Source Code Form is subject to the terms of the Mozilla Wlic
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

#[macro_use]
extern crate js;
extern crate libc;

use js::rust::{Runtime, SIMPLE_GLOBAL_CLASS};
use js::jsapi::root::{JS_NewGlobalObject, JS_InitClass};
use js::jsapi::root::JS::CompartmentOptions;
use js::jsapi::root::JS::OnNewGlobalHookOption;
use js::jsval::UndefinedValue;
use js::magicdom::node::NODE_CLASS;
use js::magicdom::node::NODE_PS_ARR;
use js::magicdom::node::NODE_FN_ARR;
use js::magicdom::node::Node_constructor;

use std::ptr;
use std::str;

#[test]
fn get_and_set() {
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

        rooted!(in(cx) let _node_proto =
                JS_InitClass(cx, global.handle(), proto.handle(), &NODE_CLASS, Some(Node_constructor),
                             7, NODE_PS_ARR.as_ptr(), NODE_FN_ARR.as_ptr(),
                             std::ptr::null(), std::ptr::null())
        );

        rooted!(in(cx) let mut rval = UndefinedValue());
        assert!(rt.evaluate_script(global.handle(), r#"
let node1 = new Node(1, "Node2", "mozilla/en", false, "x", "div", []);
let node2 = new Node(1, "Node3", "mozilla/en", false, "p", "div", []);
let node = new Node(1, "Node", "mozilla/en", false, "n", "h1", [node1, node2]);
if (Object.getPrototypeOf(node) != Node.prototype) {
    throw Error("node prototype is wrong");
}
if (!(node instanceof Node)) {
    throw Error("is not instance of Node?");
}
if (node.node_type != 1) {
    throw Error("node.node_type is not 1");
}
if (node.node_name != "Node") {
    throw Error("node.node_name is not Node");
}
if (node.base_uri != "mozilla/en") {
    throw Error("node.base_uri is not mozilla/en");
}
if (node.is_connected != false) {
    throw Error("node.is_connected is not false");
}
if (node.node_value != "n") {
    throw Error("node.node_value is not n");
}
if (node.text_content != "h1") {
    throw Error("node.text_content is not h1");
}
node.node_value = "h6";
node.text_content = "<b>";
if (node.node_value != "h6") {
    throw Error("node.node_value is not h6");
}
if (node.text_content != "<b>") {
    throw Error("node.text_content is not <b>");
}
let childs = node.child_nodes;
if (childs[0].node_type != 1) {
    throw Error("childs[0].node_type is not 1");
}
if (childs[0].node_name != "Node2") {
    throw Error("childs[0].node_name is not Node");
}
if (childs[0].base_uri != "mozilla/en") {
    throw Error("childs[0].base_uri is not mozilla/en");
}
if (childs[0].is_connected != false) {
    throw Error("childs[0].is_connected is not false");
}
if (childs[0].node_value != "x") {
    throw Error("childs[0].node_value is not n");
}
if (childs[0].text_content != "div") {
    throw Error("childs[0].text_content is not h1");
}
if (childs[0].child_nodes.length != 0) {
    throw Error("childs[0].child_nodes is not empty array");
}
if (childs[1].node_type != 1) {
    throw Error("childs[1].node_type is not 1");
}
if (childs[1].node_name != "Node3") {
    throw Error("childs[1].node_name is not Node");
}
if (childs[1].base_uri != "mozilla/en") {
    throw Error("childs[1].base_uri is not mozilla/en");
}
if (childs[1].is_connected != false) {
    throw Error("childs[1].is_connected is not false");
}
if (childs[1].node_value != "p") {
    throw Error("childs[1].node_value is not n");
}
if (childs[1].text_content != "div") {
    throw Error("childs[1].text_content is not h1");
}
if (childs[1].child_nodes.length != 0) {
    throw Error("childs[1].child_nodes is not empty array");
}
"#,
                                   "test", 33, rval.handle_mut()).is_ok());
    }
}