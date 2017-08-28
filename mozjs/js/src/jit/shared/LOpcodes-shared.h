/* -*- Mode: C++; tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 4 -*-
 * vim: set ts=8 sts=4 et sw=4 tw=99:
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

#ifndef jit_shared_LOpcodes_shared_h
#define jit_shared_LOpcodes_shared_h

#define LIR_COMMON_OPCODE_LIST(_)   \
    _(Unbox)                        \
    _(Box)                          \
    _(UnboxFloatingPoint)           \
    _(OsiPoint)                     \
    _(MoveGroup)                    \
    _(Integer)                      \
    _(Integer64)                    \
    _(Pointer)                      \
    _(Double)                       \
    _(Float32)                      \
    _(SimdBox)                      \
    _(SimdUnbox)                    \
    _(SimdSplatX16)                 \
    _(SimdSplatX8)                  \
    _(SimdSplatX4)                  \
    _(Simd128Int)                   \
    _(Simd128Float)                 \
    _(SimdAllTrue)                  \
    _(SimdAnyTrue)                  \
    _(SimdReinterpretCast)          \
    _(SimdExtractElementI)          \
    _(SimdExtractElementU2D)        \
    _(SimdExtractElementB)          \
    _(SimdExtractElementF)          \
    _(SimdInsertElementI)           \
    _(SimdInsertElementF)           \
    _(SimdGeneralShuffleI)          \
    _(SimdGeneralShuffleF)          \
    _(SimdSwizzleI)                 \
    _(SimdSwizzleF)                 \
    _(SimdShuffle)                  \
    _(SimdShuffleX4)                \
    _(SimdUnaryArithIx16)           \
    _(SimdUnaryArithIx8)            \
    _(SimdUnaryArithIx4)            \
    _(SimdUnaryArithFx4)            \
    _(SimdBinaryCompIx16)           \
    _(SimdBinaryCompIx8)            \
    _(SimdBinaryCompIx4)            \
    _(SimdBinaryCompFx4)            \
    _(SimdBinaryArithIx16)          \
    _(SimdBinaryArithIx8)           \
    _(SimdBinaryArithIx4)           \
    _(SimdBinaryArithFx4)           \
    _(SimdBinarySaturating)         \
    _(SimdBinaryBitwise)            \
    _(SimdShift)                    \
    _(SimdSelect)                   \
    _(Value)                        \
    _(CloneLiteral)                 \
    _(Parameter)                    \
    _(Callee)                       \
    _(IsConstructing)               \
    _(TableSwitch)                  \
    _(TableSwitchV)                 \
    _(Goto)                         \
    _(NewArray)                     \
    _(NewArrayCopyOnWrite)          \
    _(NewArrayDynamicLength)        \
    _(NewIterator)                  \
    _(NewTypedArray)                \
    _(NewTypedArrayDynamicLength)   \
    _(NewObject)                    \
    _(NewTypedObject)               \
    _(NewNamedLambdaObject)         \
    _(NewCallObject)                \
    _(NewSingletonCallObject)       \
    _(NewStringObject)              \
    _(NewDerivedTypedObject)        \
    _(InitElem)                     \
    _(InitElemGetterSetter)         \
    _(MutateProto)                  \
    _(InitPropGetterSetter)         \
    _(CheckOverRecursed)            \
    _(DefVar)                       \
    _(DefLexical)                   \
    _(DefFun)                       \
    _(CallKnown)                    \
    _(CallGeneric)                  \
    _(CallNative)                   \
    _(ApplyArgsGeneric)             \
    _(ApplyArrayGeneric)            \
    _(Bail)                         \
    _(Unreachable)                  \
    _(EncodeSnapshot)               \
    _(GetDynamicName)               \
    _(CallDirectEval)               \
    _(StackArgT)                    \
    _(StackArgV)                    \
    _(CreateThis)                   \
    _(CreateThisWithProto)          \
    _(CreateThisWithTemplate)       \
    _(CreateArgumentsObject)        \
    _(GetArgumentsObjectArg)        \
    _(SetArgumentsObjectArg)        \
    _(ReturnFromCtor)               \
    _(ComputeThis)                  \
    _(BitNotI)                      \
    _(BitNotV)                      \
    _(BitOpI)                       \
    _(BitOpI64)                     \
    _(BitOpV)                       \
    _(ShiftI)                       \
    _(ShiftI64)                     \
    _(SignExtendInt32)              \
    _(SignExtendInt64)              \
    _(UrshD)                        \
    _(Return)                       \
    _(Throw)                        \
    _(Phi)                          \
    _(TestIAndBranch)               \
    _(TestI64AndBranch)             \
    _(TestDAndBranch)               \
    _(TestFAndBranch)               \
    _(TestVAndBranch)               \
    _(TestOAndBranch)               \
    _(FunctionDispatch)             \
    _(ObjectGroupDispatch)          \
    _(Compare)                      \
    _(CompareAndBranch)             \
    _(CompareI64)                   \
    _(CompareI64AndBranch)          \
    _(CompareD)                     \
    _(CompareDAndBranch)            \
    _(CompareF)                     \
    _(CompareFAndBranch)            \
    _(CompareS)                     \
    _(CompareStrictS)               \
    _(CompareB)                     \
    _(CompareBAndBranch)            \
    _(CompareBitwise)               \
    _(CompareBitwiseAndBranch)      \
    _(CompareVM)                    \
    _(BitAndAndBranch)              \
    _(IsNullOrLikeUndefinedV)       \
    _(IsNullOrLikeUndefinedT)       \
    _(IsNullOrLikeUndefinedAndBranchV)\
    _(IsNullOrLikeUndefinedAndBranchT)\
    _(MinMaxI)                      \
    _(MinMaxD)                      \
    _(MinMaxF)                      \
    _(NegI)                         \
    _(NegD)                         \
    _(NegF)                         \
    _(AbsI)                         \
    _(AbsD)                         \
    _(AbsF)                         \
    _(ClzI)                         \
    _(ClzI64)                       \
    _(CtzI)                         \
    _(CtzI64)                       \
    _(PopcntI)                      \
    _(PopcntI64)                    \
    _(SqrtD)                        \
    _(SqrtF)                        \
    _(CopySignD)                    \
    _(CopySignF)                    \
    _(Atan2D)                       \
    _(Hypot)                        \
    _(PowI)                         \
    _(PowD)                         \
    _(PowV)                         \
    _(PowHalfD)                     \
    _(Random)                       \
    _(MathFunctionD)                \
    _(MathFunctionF)                \
    _(NotI)                         \
    _(NotI64)                       \
    _(NotD)                         \
    _(NotF)                         \
    _(NotO)                         \
    _(NotV)                         \
    _(AddI)                         \
    _(AddI64)                       \
    _(SubI)                         \
    _(SubI64)                       \
    _(MulI)                         \
    _(MulI64)                       \
    _(MathD)                        \
    _(MathF)                        \
    _(DivI)                         \
    _(DivPowTwoI)                   \
    _(ModI)                         \
    _(ModPowTwoI)                   \
    _(ModD)                         \
    _(BinaryV)                      \
    _(Concat)                       \
    _(CharCodeAt)                   \
    _(FromCharCode)                 \
    _(FromCodePoint)                \
    _(StringConvertCase)            \
    _(SinCos)                       \
    _(StringSplit)                  \
    _(Int32ToDouble)                \
    _(Float32ToDouble)              \
    _(DoubleToFloat32)              \
    _(Int32ToFloat32)               \
    _(ValueToDouble)                \
    _(ValueToInt32)                 \
    _(ValueToFloat32)               \
    _(DoubleToInt32)                \
    _(Float32ToInt32)               \
    _(TruncateDToInt32)             \
    _(TruncateFToInt32)             \
    _(WrapInt64ToInt32)             \
    _(ExtendInt32ToInt64)           \
    _(BooleanToString)              \
    _(IntToString)                  \
    _(DoubleToString)               \
    _(ValueToString)                \
    _(ValueToObject)                \
    _(ValueToObjectOrNull)          \
    _(Int32x4ToFloat32x4)           \
    _(Float32x4ToInt32x4)           \
    _(Float32x4ToUint32x4)          \
    _(Start)                        \
    _(NaNToZero)                    \
    _(OsrEntry)                     \
    _(OsrValue)                     \
    _(OsrEnvironmentChain)          \
    _(OsrReturnValue)               \
    _(OsrArgumentsObject)           \
    _(RegExp)                       \
    _(RegExpMatcher)                \
    _(RegExpSearcher)               \
    _(RegExpTester)                 \
    _(RegExpPrototypeOptimizable)   \
    _(RegExpInstanceOptimizable)    \
    _(GetFirstDollarIndex)          \
    _(StringReplace)                \
    _(Substr)                       \
    _(BinarySharedStub)             \
    _(UnarySharedStub)              \
    _(NullarySharedStub)            \
    _(ClassConstructor)             \
    _(Lambda)                       \
    _(LambdaArrow)                  \
    _(LambdaForSingleton)           \
    _(SetFunName)                   \
    _(KeepAliveObject)              \
    _(Slots)                        \
    _(Elements)                     \
    _(ConvertElementsToDoubles)     \
    _(MaybeToDoubleElement)         \
    _(MaybeCopyElementsForWrite)    \
    _(LoadSlotV)                    \
    _(LoadSlotT)                    \
    _(StoreSlotV)                   \
    _(StoreSlotT)                   \
    _(GuardShape)                   \
    _(GuardReceiverPolymorphic)     \
    _(GuardObjectGroup)             \
    _(GuardObjectIdentity)          \
    _(GuardClass)                   \
    _(GuardUnboxedExpando)          \
    _(LoadUnboxedExpando)           \
    _(TypeBarrierV)                 \
    _(TypeBarrierO)                 \
    _(MonitorTypes)                 \
    _(PostWriteBarrierO)            \
    _(PostWriteBarrierV)            \
    _(PostWriteElementBarrierO)     \
    _(PostWriteElementBarrierV)     \
    _(InitializedLength)            \
    _(SetInitializedLength)         \
    _(UnboxedArrayLength)           \
    _(UnboxedArrayInitializedLength) \
    _(IncrementUnboxedArrayInitializedLength) \
    _(SetUnboxedArrayInitializedLength) \
    _(BoundsCheck)                  \
    _(BoundsCheckRange)             \
    _(BoundsCheckLower)             \
    _(LoadElementV)                 \
    _(LoadElementT)                 \
    _(LoadElementHole)              \
    _(LoadUnboxedScalar)            \
    _(LoadUnboxedPointerV)          \
    _(LoadUnboxedPointerT)          \
    _(LoadElementFromStateV)        \
    _(UnboxObjectOrNull)            \
    _(StoreElementV)                \
    _(StoreElementT)                \
    _(StoreUnboxedScalar)           \
    _(StoreUnboxedPointer)          \
    _(ConvertUnboxedObjectToNative) \
    _(ArrayPopShiftV)               \
    _(ArrayPopShiftT)               \
    _(ArrayPushV)                   \
    _(ArrayPushT)                   \
    _(ArraySlice)                   \
    _(ArrayJoin)                    \
    _(StoreElementHoleV)            \
    _(StoreElementHoleT)            \
    _(FallibleStoreElementV)        \
    _(FallibleStoreElementT)        \
    _(LoadTypedArrayElementHole)    \
    _(LoadTypedArrayElementStatic)  \
    _(StoreTypedArrayElementHole)   \
    _(StoreTypedArrayElementStatic) \
    _(AtomicIsLockFree)             \
    _(GuardSharedTypedArray)        \
    _(CompareExchangeTypedArrayElement) \
    _(AtomicExchangeTypedArrayElement) \
    _(AtomicTypedArrayElementBinop) \
    _(AtomicTypedArrayElementBinopForEffect) \
    _(EffectiveAddress)             \
    _(ClampIToUint8)                \
    _(ClampDToUint8)                \
    _(ClampVToUint8)                \
    _(LoadFixedSlotV)               \
    _(LoadFixedSlotT)               \
    _(LoadFixedSlotAndUnbox)        \
    _(StoreFixedSlotV)              \
    _(StoreFixedSlotT)              \
    _(FunctionEnvironment)          \
    _(NewLexicalEnvironmentObject)  \
    _(CopyLexicalEnvironmentObject) \
    _(GetPropertyCacheV)            \
    _(GetPropertyCacheT)            \
    _(GetPropertyPolymorphicV)      \
    _(GetPropertyPolymorphicT)      \
    _(BindNameCache)                \
    _(CallBindVar)                  \
    _(CallGetProperty)              \
    _(GetNameCache)                 \
    _(CallGetIntrinsicValue)        \
    _(CallGetElement)               \
    _(CallSetElement)               \
    _(CallInitElementArray)         \
    _(CallSetProperty)              \
    _(CallDeleteProperty)           \
    _(CallDeleteElement)            \
    _(SetPropertyCache)             \
    _(SetPropertyPolymorphicV)      \
    _(SetPropertyPolymorphicT)      \
    _(GetIteratorCache)             \
    _(IteratorMore)                 \
    _(IsNoIterAndBranch)            \
    _(IteratorEnd)                  \
    _(ArrayLength)                  \
    _(SetArrayLength)               \
    _(GetNextEntryForIterator)      \
    _(TypedArrayLength)             \
    _(TypedArrayElements)           \
    _(SetDisjointTypedElements)     \
    _(TypedObjectDescr)             \
    _(TypedObjectElements)          \
    _(SetTypedObjectOffset)         \
    _(StringLength)                 \
    _(ArgumentsLength)              \
    _(GetFrameArgument)             \
    _(SetFrameArgumentT)            \
    _(SetFrameArgumentC)            \
    _(SetFrameArgumentV)            \
    _(RunOncePrologue)              \
    _(Rest)                         \
    _(TypeOfV)                      \
    _(ToAsync)                      \
    _(ToAsyncGen)                   \
    _(ToAsyncIter)                  \
    _(ToIdV)                        \
    _(Floor)                        \
    _(FloorF)                       \
    _(Ceil)                         \
    _(CeilF)                        \
    _(Round)                        \
    _(RoundF)                       \
    _(NearbyInt)                    \
    _(NearbyIntF)                   \
    _(InCache)                      \
    _(InArray)                      \
    _(HasOwnCache)                  \
    _(InstanceOfO)                  \
    _(InstanceOfV)                  \
    _(CallInstanceOf)               \
    _(InterruptCheck)               \
    _(Rotate)                       \
    _(RotateI64)                    \
    _(GetDOMProperty)               \
    _(GetDOMMemberV)                \
    _(GetDOMMemberT)                \
    _(SetDOMProperty)               \
    _(CallDOMNative)                \
    _(IsCallableO)                  \
    _(IsCallableV)                  \
    _(IsConstructor)                \
    _(IsArrayO)                     \
    _(IsArrayV)                     \
    _(IsTypedArray)                 \
    _(IsObject)                     \
    _(IsObjectAndBranch)            \
    _(HasClass)                     \
    _(ObjectClassToString)          \
    _(RecompileCheck)               \
    _(MemoryBarrier)                \
    _(AssertRangeI)                 \
    _(AssertRangeD)                 \
    _(AssertRangeF)                 \
    _(AssertRangeV)                 \
    _(AssertResultV)                \
    _(AssertResultT)                \
    _(LexicalCheck)                 \
    _(ThrowRuntimeLexicalError)     \
    _(GlobalNameConflictsCheck)     \
    _(Debugger)                     \
    _(NewTarget)                    \
    _(ArrowNewTarget)               \
    _(CheckReturn)                  \
    _(CheckIsObj)                   \
    _(CheckIsCallable)              \
    _(CheckObjCoercible)            \
    _(DebugCheckSelfHosted)         \
    _(FinishBoundFunctionInit)      \
    _(IsPackedArray)                \
    _(GetPrototypeOf)               \
    _(AsmJSLoadHeap)                \
    _(AsmJSStoreHeap)               \
    _(AsmJSCompareExchangeHeap)     \
    _(AsmJSAtomicExchangeHeap)      \
    _(AsmJSAtomicBinopHeap)         \
    _(AsmJSAtomicBinopHeapForEffect)\
    _(WasmTruncateToInt32)          \
    _(WasmTrap)                     \
    _(WasmReinterpret)              \
    _(WasmReinterpretToI64)         \
    _(WasmReinterpretFromI64)       \
    _(WasmSelect)                   \
    _(WasmSelectI64)                \
    _(WasmBoundsCheck)              \
    _(WasmLoadTls)                  \
    _(WasmAddOffset)                \
    _(WasmLoad)                     \
    _(WasmLoadI64)                  \
    _(WasmStore)                    \
    _(WasmStoreI64)                 \
    _(WasmLoadGlobalVar)            \
    _(WasmLoadGlobalVarI64)         \
    _(WasmStoreGlobalVar)           \
    _(WasmStoreGlobalVarI64)        \
    _(WasmParameter)                \
    _(WasmParameterI64)             \
    _(WasmReturn)                   \
    _(WasmReturnI64)                \
    _(WasmReturnVoid)               \
    _(WasmStackArg)                 \
    _(WasmStackArgI64)              \
    _(WasmCall)                     \
    _(WasmCallI64)                  \
    _(WasmUint32ToDouble)           \
    _(WasmUint32ToFloat32)

#endif /* jit_shared_LOpcodes_shared_h */
