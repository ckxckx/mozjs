/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

//! Nicer, Rust-y APIs for structured cloning.

use glue;
use jsapi;
use rust::Runtime;
use std::marker::PhantomData;
use std::ptr;

/// The scope of a structured clone buffer.
pub trait StructuredCloneScope {
    /// The raw JSAPI form.
    fn raw() -> jsapi::JS::StructuredCloneScope;
}

/// A non-`Send` structured clone within this thread.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct SameProcessSameThread(PhantomData<*mut ()>);

impl StructuredCloneScope for SameProcessSameThread {
    fn raw() -> jsapi::JS::StructuredCloneScope {
        jsapi::JS::StructuredCloneScope::SameProcessSameThread
    }
}

/// A structured clone that crosses thread boundaries within the same process.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct SameProcessDifferentThread;

impl StructuredCloneScope for SameProcessDifferentThread {
    fn raw() -> jsapi::JS::StructuredCloneScope {
        jsapi::JS::StructuredCloneScope::SameProcessDifferentThread
    }
}

/// A structured clone that crosses process boundaries.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct DifferentProcess;

impl StructuredCloneScope for DifferentProcess {
    fn raw() -> jsapi::JS::StructuredCloneScope {
        jsapi::JS::StructuredCloneScope::DifferentProcess
    }
}

/// An RAII owned buffer for structured cloning into and out of.
#[derive(Debug)]
pub struct StructuredCloneBuffer<'a, S> {
    raw: *mut jsapi::JSAutoStructuredCloneBuffer,
    callbacks: &'a jsapi::JSStructuredCloneCallbacks,
    scope: PhantomData<S>,
}

/// A `StructuredCloneBuffer`'s `Send` is controlled by its scope: if its scope
/// is `Send`, then it is too.
unsafe impl<'a, S: Send> Send for StructuredCloneBuffer<'a, S> {}

impl<'a, S> StructuredCloneBuffer<'a, S>
where
    S: StructuredCloneScope,
{
    /// Construct a new `StructuredCloneBuffer`.
    ///
    /// # Panics
    ///
    /// Panics if the underlying JSAPI calls fail.
    pub fn new(callbacks: &'a jsapi::JSStructuredCloneCallbacks)-> Self {
        let raw = unsafe {
            glue::NewJSAutoStructuredCloneBuffer(S::raw(), callbacks)
        };
        assert!(!raw.is_null());
        StructuredCloneBuffer {
            raw,
            callbacks,
            scope: PhantomData,
        }
    }

    /// Get the raw `*mut JSStructuredCloneData` owned by this buffer.
    pub fn data(&self) -> *mut jsapi::JSStructuredCloneData {
        unsafe {
            &mut (*self.raw).data_
        }
    }

    /// Copy this buffer's data into a vec.
    pub fn copy_to_vec(&self) -> Vec<u8> {
        let len = unsafe {
            glue::GetLengthOfJSStructuredCloneData(self.data())
        };
        let mut vec = Vec::with_capacity(len);
        unsafe {
            glue::CopyJSStructuredCloneData(self.data(), vec.as_mut_ptr());
        }
        vec
    }

    /// Read a JS value out of this buffer.
    pub fn read(&mut self, vp: jsapi::JS::MutableHandleValue)
                -> Result<(), ()> {
        if unsafe {
            (*self.raw).read(Runtime::get(), vp, self.callbacks, ptr::null_mut())
        } {
            Ok(())
        } else {
            Err(())
        }
    }

    /// Write a JS value into this buffer.
    pub fn write(&mut self,
                 v: jsapi::JS::HandleValue,
                 callbacks: &jsapi::JSStructuredCloneCallbacks)
                 -> Result<(), ()> {
        if unsafe {
            (*self.raw).write(Runtime::get(), v, callbacks, ptr::null_mut())
        } {
            Ok(())
        } else {
            Err(())
        }
    }

    /// Copy the given slice into this buffer.
    pub fn write_bytes(&mut self, bytes: &[u8]) -> Result<(), ()> {
        let len = bytes.len();
        let src = bytes.as_ptr();
        if unsafe {
            glue::WriteBytesToJSStructuredCloneData(src, len, self.data())
        } {
            Ok(())
        } else {
            Err(())
        }
    }
}

impl<'a, S> Drop for StructuredCloneBuffer<'a, S> {
    fn drop(&mut self) {
        unsafe {
            glue::DeleteJSAutoStructuredCloneBuffer(self.raw);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn is_send<S: Send>(_: S) {}

    #[test]
    fn same_process_different_thread_scope_is_send() {
        is_send(SameProcessDifferentThread);
    }

    #[test]
    fn different_process_scope_is_send() {
        is_send(DifferentProcess);
    }
}
