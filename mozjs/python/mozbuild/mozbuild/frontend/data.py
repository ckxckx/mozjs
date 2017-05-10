# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

r"""Data structures representing Mozilla's source tree.

The frontend files are parsed into static data structures. These data
structures are defined in this module.

All data structures of interest are children of the TreeMetadata class.

Logic for populating these data structures is not defined in this class.
Instead, what we have here are dumb container classes. The emitter module
contains the code for converting executed mozbuild files into these data
structures.
"""

from __future__ import absolute_import, unicode_literals

from mozbuild.util import StrictOrderingOnAppendList
from mozpack.chrome.manifest import ManifestEntry

import mozpack.path as mozpath
from .context import FinalTargetValue

from ..util import (
    group_unified_files,
)

from ..testing import (
    all_test_flavors,
)


class TreeMetadata(object):
    """Base class for all data being captured."""
    __slots__ = ()

    def to_dict(self):
        return {k.lower(): getattr(self, k) for k in self.DICT_ATTRS}


class ContextDerived(TreeMetadata):
    """Build object derived from a single Context instance.

    It holds fields common to all context derived classes. This class is likely
    never instantiated directly but is instead derived from.
    """

    __slots__ = (
        'context_main_path',
        'context_all_paths',
        'topsrcdir',
        'topobjdir',
        'relativedir',
        'srcdir',
        'objdir',
        'config',
        '_context',
    )

    def __init__(self, context):
        TreeMetadata.__init__(self)

        # Capture the files that were evaluated to fill this context.
        self.context_main_path = context.main_path
        self.context_all_paths = context.all_paths

        # Basic directory state.
        self.topsrcdir = context.config.topsrcdir
        self.topobjdir = context.config.topobjdir

        self.relativedir = context.relsrcdir
        self.srcdir = context.srcdir
        self.objdir = context.objdir

        self.config = context.config

        self._context = context

    @property
    def install_target(self):
        return self._context['FINAL_TARGET']

    @property
    def defines(self):
        defines = self._context['DEFINES']
        return Defines(self._context, defines) if defines else None

    @property
    def relobjdir(self):
        return mozpath.relpath(self.objdir, self.topobjdir)


class HostMixin(object):
    @property
    def defines(self):
        defines = self._context['HOST_DEFINES']
        return HostDefines(self._context, defines) if defines else None


class DirectoryTraversal(ContextDerived):
    """Describes how directory traversal for building should work.

    This build object is likely only of interest to the recursive make backend.
    Other build backends should (ideally) not attempt to mimic the behavior of
    the recursive make backend. The only reason this exists is to support the
    existing recursive make backend while the transition to mozbuild frontend
    files is complete and we move to a more optimal build backend.

    Fields in this class correspond to similarly named variables in the
    frontend files.
    """
    __slots__ = (
        'dirs',
    )

    def __init__(self, context):
        ContextDerived.__init__(self, context)

        self.dirs = []


class BaseConfigSubstitution(ContextDerived):
    """Base class describing autogenerated files as part of config.status."""

    __slots__ = (
        'input_path',
        'output_path',
        'relpath',
    )

    def __init__(self, context):
        ContextDerived.__init__(self, context)

        self.input_path = None
        self.output_path = None
        self.relpath = None


class ConfigFileSubstitution(BaseConfigSubstitution):
    """Describes a config file that will be generated using substitutions."""


class VariablePassthru(ContextDerived):
    """A dict of variables to pass through to backend.mk unaltered.

    The purpose of this object is to facilitate rapid transitioning of
    variables from Makefile.in to moz.build. In the ideal world, this class
    does not exist and every variable has a richer class representing it.
    As long as we rely on this class, we lose the ability to have flexibility
    in our build backends since we will continue to be tied to our rules.mk.
    """
    __slots__ = ('variables')

    def __init__(self, context):
        ContextDerived.__init__(self, context)
        self.variables = {}

class XPIDLFile(ContextDerived):
    """Describes an XPIDL file to be compiled."""

    __slots__ = (
        'source_path',
        'basename',
        'module',
        'add_to_manifest',
    )

    def __init__(self, context, source, module, add_to_manifest):
        ContextDerived.__init__(self, context)

        self.source_path = source
        self.basename = mozpath.basename(source)
        self.module = module
        self.add_to_manifest = add_to_manifest

class BaseDefines(ContextDerived):
    """Context derived container object for DEFINES/HOST_DEFINES,
    which are OrderedDicts.
    """
    __slots__ = ('defines')

    def __init__(self, context, defines):
        ContextDerived.__init__(self, context)
        self.defines = defines

    def get_defines(self):
        for define, value in self.defines.iteritems():
            if value is True:
                yield('-D%s' % define)
            elif value is False:
                yield('-U%s' % define)
            else:
                yield('-D%s=%s' % (define, value))

    def update(self, more_defines):
        if isinstance(more_defines, Defines):
            self.defines.update(more_defines.defines)
        else:
            self.defines.update(more_defines)

class Defines(BaseDefines):
    pass

class HostDefines(BaseDefines):
    pass

class IPDLFile(ContextDerived):
    """Describes an individual .ipdl source file."""

    __slots__ = (
        'basename',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.basename = path

class WebIDLFile(ContextDerived):
    """Describes an individual .webidl source file."""

    __slots__ = (
        'basename',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.basename = path

class GeneratedEventWebIDLFile(ContextDerived):
    """Describes an individual .webidl source file."""

    __slots__ = (
        'basename',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.basename = path

class TestWebIDLFile(ContextDerived):
    """Describes an individual test-only .webidl source file."""

    __slots__ = (
        'basename',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.basename = path

class PreprocessedTestWebIDLFile(ContextDerived):
    """Describes an individual test-only .webidl source file that requires
    preprocessing."""

    __slots__ = (
        'basename',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.basename = path

class PreprocessedWebIDLFile(ContextDerived):
    """Describes an individual .webidl source file that requires preprocessing."""

    __slots__ = (
        'basename',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.basename = path

class GeneratedWebIDLFile(ContextDerived):
    """Describes an individual .webidl source file that is generated from
    build rules."""

    __slots__ = (
        'basename',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.basename = path


class ExampleWebIDLInterface(ContextDerived):
    """An individual WebIDL interface to generate."""

    __slots__ = (
        'name',
    )

    def __init__(self, context, name):
        ContextDerived.__init__(self, context)

        self.name = name


class LinkageWrongKindError(Exception):
    """Error thrown when trying to link objects of the wrong kind"""


class LinkageMultipleRustLibrariesError(Exception):
    """Error thrown when trying to link multiple Rust libraries to an object"""


class Linkable(ContextDerived):
    """Generic context derived container object for programs and libraries"""
    __slots__ = (
        'cxx_link',
        'lib_defines',
        'linked_libraries',
        'linked_system_libs',
    )

    def __init__(self, context):
        ContextDerived.__init__(self, context)
        self.cxx_link = False
        self.linked_libraries = []
        self.linked_system_libs = []
        self.lib_defines = Defines(context, {})

    def link_library(self, obj):
        assert isinstance(obj, BaseLibrary)
        if isinstance(obj, SharedLibrary) and obj.variant == obj.COMPONENT:
            raise LinkageWrongKindError(
                'Linkable.link_library() does not take components.')
        if obj.KIND != self.KIND:
            raise LinkageWrongKindError('%s != %s' % (obj.KIND, self.KIND))
        # Linking multiple Rust libraries into an object would result in
        # multiple copies of the Rust standard library, as well as linking
        # errors from duplicate symbols.
        if isinstance(obj, RustLibrary) and any(isinstance(l, RustLibrary)
                                                for l in self.linked_libraries):
            raise LinkageMultipleRustLibrariesError("Cannot link multiple Rust libraries into %s",
                                                    self)
        self.linked_libraries.append(obj)
        if obj.cxx_link:
            self.cxx_link = True
        obj.refs.append(self)

    def link_system_library(self, lib):
        # The '$' check is here as a special temporary rule, allowing the
        # inherited use of make variables, most notably in TK_LIBS.
        if not lib.startswith('$') and not lib.startswith('-'):
            if self.config.substs.get('GNU_CC'):
                lib = '-l%s' % lib
            else:
                lib = '%s%s%s' % (
                    self.config.import_prefix,
                    lib,
                    self.config.import_suffix,
                )
        self.linked_system_libs.append(lib)

class BaseProgram(Linkable):
    """Context derived container object for programs, which is a unicode
    string.

    This class handles automatically appending a binary suffix to the program
    name.
    If the suffix is not defined, the program name is unchanged.
    Otherwise, if the program name ends with the given suffix, it is unchanged
    Otherwise, the suffix is appended to the program name.
    """
    __slots__ = ('program')

    DICT_ATTRS = {
        'install_target',
        'KIND',
        'program',
        'relobjdir',
    }

    def __init__(self, context, program, is_unit_test=False):
        Linkable.__init__(self, context)

        bin_suffix = context.config.substs.get(self.SUFFIX_VAR, '')
        if not program.endswith(bin_suffix):
            program += bin_suffix
        self.program = program
        self.is_unit_test = is_unit_test

    def __repr__(self):
        return '<%s: %s/%s>' % (type(self).__name__, self.relobjdir, self.program)


class Program(BaseProgram):
    """Context derived container object for PROGRAM"""
    SUFFIX_VAR = 'BIN_SUFFIX'
    KIND = 'target'


class HostProgram(HostMixin, BaseProgram):
    """Context derived container object for HOST_PROGRAM"""
    SUFFIX_VAR = 'HOST_BIN_SUFFIX'
    KIND = 'host'


class SimpleProgram(BaseProgram):
    """Context derived container object for each program in SIMPLE_PROGRAMS"""
    SUFFIX_VAR = 'BIN_SUFFIX'
    KIND = 'target'


class HostSimpleProgram(HostMixin, BaseProgram):
    """Context derived container object for each program in
    HOST_SIMPLE_PROGRAMS"""
    SUFFIX_VAR = 'HOST_BIN_SUFFIX'
    KIND = 'host'


def cargo_output_directory(context, target_var):
    # cargo creates several directories and places its build artifacts
    # in those directories.  The directory structure depends not only
    # on the target, but also what sort of build we are doing.
    rust_build_kind = 'release'
    if context.config.substs.get('MOZ_DEBUG_RUST'):
        rust_build_kind = 'debug'
    return mozpath.join(context.config.substs[target_var], rust_build_kind)


# Rust programs aren't really Linkable, since Cargo handles all the details
# of linking things.
class BaseRustProgram(ContextDerived):
    __slots__ = (
        'name',
        'cargo_file',
        'location',
        'SUFFIX_VAR',
        'KIND',
        'TARGET_SUBST_VAR',
    )

    def __init__(self, context, name, cargo_file):
        ContextDerived.__init__(self, context)
        self.name = name
        self.cargo_file = cargo_file
        cargo_dir = cargo_output_directory(context, self.TARGET_SUBST_VAR)
        exe_file = '%s%s' % (name, context.config.substs.get(self.SUFFIX_VAR, ''))
        self.location = mozpath.join(cargo_dir, exe_file)


class RustProgram(BaseRustProgram):
    SUFFIX_VAR = 'BIN_SUFFIX'
    KIND = 'target'
    TARGET_SUBST_VAR = 'RUST_TARGET'


class HostRustProgram(BaseRustProgram):
    SUFFIX_VAR = 'HOST_BIN_SUFFIX'
    KIND = 'host'
    TARGET_SUBST_VAR = 'RUST_HOST_TARGET'


class BaseLibrary(Linkable):
    """Generic context derived container object for libraries."""
    __slots__ = (
        'basename',
        'lib_name',
        'import_name',
        'refs',
    )

    def __init__(self, context, basename):
        Linkable.__init__(self, context)

        self.basename = self.lib_name = basename
        if self.lib_name:
            self.lib_name = '%s%s%s' % (
                context.config.lib_prefix,
                self.lib_name,
                context.config.lib_suffix
            )
            self.import_name = self.lib_name

        self.refs = []

    def __repr__(self):
        return '<%s: %s/%s>' % (type(self).__name__, self.relobjdir, self.lib_name)


class Library(BaseLibrary):
    """Context derived container object for a library"""
    KIND = 'target'
    __slots__ = (
    )

    def __init__(self, context, basename, real_name=None):
        BaseLibrary.__init__(self, context, real_name or basename)
        self.basename = basename


class StaticLibrary(Library):
    """Context derived container object for a static library"""
    __slots__ = (
        'link_into',
        'no_expand_lib',
    )

    def __init__(self, context, basename, real_name=None,
        link_into=None, no_expand_lib=False):
        Library.__init__(self, context, basename, real_name)
        self.link_into = link_into
        self.no_expand_lib = no_expand_lib


class RustLibrary(StaticLibrary):
    """Context derived container object for a static library"""
    __slots__ = (
        'cargo_file',
        'crate_type',
        'dependencies',
        'deps_path',
        'features',
        'target_dir',
    )
    TARGET_SUBST_VAR = 'RUST_TARGET'
    FEATURES_VAR = 'RUST_LIBRARY_FEATURES'
    LIB_FILE_VAR = 'RUST_LIBRARY_FILE'

    def __init__(self, context, basename, cargo_file, crate_type, dependencies,
                 features, target_dir, **args):
        StaticLibrary.__init__(self, context, basename, **args)
        self.cargo_file = cargo_file
        self.crate_type = crate_type
        # We need to adjust our naming here because cargo replaces '-' in
        # package names defined in Cargo.toml with underscores in actual
        # filenames. But we need to keep the basename consistent because
        # many other things in the build system depend on that.
        assert self.crate_type == 'staticlib'
        self.lib_name = '%s%s%s' % (context.config.rust_lib_prefix,
                                     basename.replace('-', '_'),
                                     context.config.rust_lib_suffix)
        self.dependencies = dependencies
        build_dir = mozpath.join(target_dir,
                                 cargo_output_directory(context, self.TARGET_SUBST_VAR))
        self.import_name = mozpath.join(build_dir, self.lib_name)
        self.deps_path = mozpath.join(build_dir, 'deps')
        self.features = features
        self.target_dir = target_dir


class SharedLibrary(Library):
    """Context derived container object for a shared library"""
    __slots__ = (
        'soname',
        'variant',
        'symbols_file',
    )

    DICT_ATTRS = {
        'basename',
        'import_name',
        'install_target',
        'lib_name',
        'relobjdir',
        'soname',
    }

    FRAMEWORK = 1
    COMPONENT = 2
    MAX_VARIANT = 3

    def __init__(self, context, basename, real_name=None,
                 soname=None, variant=None, symbols_file=False):
        assert(variant in range(1, self.MAX_VARIANT) or variant is None)
        Library.__init__(self, context, basename, real_name)
        self.variant = variant
        self.lib_name = real_name or basename
        assert self.lib_name

        if variant == self.FRAMEWORK:
            self.import_name = self.lib_name
        else:
            self.import_name = '%s%s%s' % (
                context.config.import_prefix,
                self.lib_name,
                context.config.import_suffix,
            )
            self.lib_name = '%s%s%s' % (
                context.config.dll_prefix,
                self.lib_name,
                context.config.dll_suffix,
            )
        if soname:
            self.soname = '%s%s%s' % (
                context.config.dll_prefix,
                soname,
                context.config.dll_suffix,
            )
        else:
            self.soname = self.lib_name

        if symbols_file is False:
            # No symbols file.
            self.symbols_file = None
        elif symbols_file is True:
            # Symbols file with default name.
            if context.config.substs['OS_TARGET'] == 'WINNT':
                self.symbols_file = '%s.def' % self.lib_name
            else:
                self.symbols_file = '%s.symbols' % self.lib_name
        else:
            # Explicitly provided name.
            self.symbols_file = symbols_file



class ExternalLibrary(object):
    """Empty mixin for libraries built by an external build system."""


class ExternalStaticLibrary(StaticLibrary, ExternalLibrary):
    """Context derived container for static libraries built by an external
    build system."""


class ExternalSharedLibrary(SharedLibrary, ExternalLibrary):
    """Context derived container for shared libraries built by an external
    build system."""


class HostLibrary(HostMixin, BaseLibrary):
    """Context derived container object for a host library"""
    KIND = 'host'


class HostRustLibrary(HostMixin, RustLibrary):
    """Context derived container object for a host rust library"""
    KIND = 'host'
    TARGET_SUBST_VAR = 'RUST_HOST_TARGET'
    FEATURES_VAR = 'HOST_RUST_LIBRARY_FEATURES'
    LIB_FILE_VAR = 'HOST_RUST_LIBRARY_FILE'


class TestManifest(ContextDerived):
    """Represents a manifest file containing information about tests."""

    __slots__ = (
        # The type of test manifest this is.
        'flavor',

        # Maps source filename to destination filename. The destination
        # path is relative from the tests root directory. Values are 2-tuples
        # of (destpath, is_test_file) where the 2nd item is True if this
        # item represents a test file (versus a support file).
        'installs',

        # A list of pattern matching installs to perform. Entries are
        # (base, pattern, dest).
        'pattern_installs',

        # Where all files for this manifest flavor are installed in the unified
        # test package directory.
        'install_prefix',

        # Set of files provided by an external mechanism.
        'external_installs',

        # Set of files required by multiple test directories, whose installation
        # will be resolved when running tests.
        'deferred_installs',

        # The full path of this manifest file.
        'path',

        # The directory where this manifest is defined.
        'directory',

        # The parsed manifestparser.TestManifest instance.
        'manifest',

        # List of tests. Each element is a dict of metadata.
        'tests',

        # The relative path of the parsed manifest within the srcdir.
        'manifest_relpath',

        # The relative path of the parsed manifest within the objdir.
        'manifest_obj_relpath',

        # The relative paths to all source files for this manifest.
        'source_relpaths',

        # If this manifest is a duplicate of another one, this is the
        # manifestparser.TestManifest of the other one.
        'dupe_manifest',
    )

    def __init__(self, context, path, manifest, flavor=None,
            install_prefix=None, relpath=None, sources=(),
            dupe_manifest=False):
        ContextDerived.__init__(self, context)

        assert flavor in all_test_flavors()

        self.path = path
        self.directory = mozpath.dirname(path)
        self.manifest = manifest
        self.flavor = flavor
        self.install_prefix = install_prefix
        self.manifest_relpath = relpath
        self.manifest_obj_relpath = relpath
        self.source_relpaths = sources
        self.dupe_manifest = dupe_manifest
        self.installs = {}
        self.pattern_installs = []
        self.tests = []
        self.external_installs = set()
        self.deferred_installs = set()


class LocalInclude(ContextDerived):
    """Describes an individual local include path."""

    __slots__ = (
        'path',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.path = path


class PerSourceFlag(ContextDerived):
    """Describes compiler flags specified for individual source files."""

    __slots__ = (
        'file_name',
        'flags',
    )

    def __init__(self, context, file_name, flags):
        ContextDerived.__init__(self, context)

        self.file_name = file_name
        self.flags = flags


class JARManifest(ContextDerived):
    """Describes an individual JAR manifest file and how to process it.

    This class isn't very useful for optimizing backends yet because we don't
    capture defines. We can't capture defines safely until all of them are
    defined in moz.build and not Makefile.in files.
    """
    __slots__ = (
        'path',
    )

    def __init__(self, context, path):
        ContextDerived.__init__(self, context)

        self.path = path


class ContextWrapped(ContextDerived):
    """Generic context derived container object for a wrapped rich object.

    Use this wrapper class to shuttle a rich build system object
    completely defined in moz.build files through the tree metadata
    emitter to the build backend for processing as-is.
    """

    __slots__ = (
        'wrapped',
    )

    def __init__(self, context, wrapped):
        ContextDerived.__init__(self, context)

        self.wrapped = wrapped


class JavaJarData(object):
    """Represents a Java JAR file.

    A Java JAR has the following members:
        * sources - strictly ordered list of input java sources
        * generated_sources - strictly ordered list of generated input
          java sources
        * extra_jars - list of JAR file dependencies to include on the
          javac compiler classpath
        * javac_flags - list containing extra flags passed to the
          javac compiler
    """

    __slots__ = (
        'name',
        'sources',
        'generated_sources',
        'extra_jars',
        'javac_flags',
    )

    def __init__(self, name, sources=[], generated_sources=[],
            extra_jars=[], javac_flags=[]):
        self.name = name
        self.sources = StrictOrderingOnAppendList(sources)
        self.generated_sources = StrictOrderingOnAppendList(generated_sources)
        self.extra_jars = list(extra_jars)
        self.javac_flags = list(javac_flags)


class BaseSources(ContextDerived):
    """Base class for files to be compiled during the build."""

    __slots__ = (
        'files',
        'canonical_suffix',
    )

    def __init__(self, context, files, canonical_suffix):
        ContextDerived.__init__(self, context)

        self.files = files
        self.canonical_suffix = canonical_suffix


class Sources(BaseSources):
    """Represents files to be compiled during the build."""

    def __init__(self, context, files, canonical_suffix):
        BaseSources.__init__(self, context, files, canonical_suffix)


class GeneratedSources(BaseSources):
    """Represents generated files to be compiled during the build."""

    def __init__(self, context, files, canonical_suffix):
        BaseSources.__init__(self, context, files, canonical_suffix)


class HostSources(HostMixin, BaseSources):
    """Represents files to be compiled for the host during the build."""

    def __init__(self, context, files, canonical_suffix):
        BaseSources.__init__(self, context, files, canonical_suffix)


class UnifiedSources(BaseSources):
    """Represents files to be compiled in a unified fashion during the build."""

    __slots__ = (
        'have_unified_mapping',
        'unified_source_mapping'
    )

    def __init__(self, context, files, canonical_suffix, files_per_unified_file=16):
        BaseSources.__init__(self, context, files, canonical_suffix)

        self.have_unified_mapping = files_per_unified_file > 1

        if self.have_unified_mapping:
            # Sorted so output is consistent and we don't bump mtimes.
            source_files = list(sorted(self.files))

            # On Windows, path names have a maximum length of 255 characters,
            # so avoid creating extremely long path names.
            unified_prefix = context.relsrcdir
            if len(unified_prefix) > 20:
                unified_prefix = unified_prefix[-20:].split('/', 1)[-1]
            unified_prefix = unified_prefix.replace('/', '_')

            suffix = self.canonical_suffix[1:]
            unified_prefix='Unified_%s_%s' % (suffix, unified_prefix)
            self.unified_source_mapping = list(group_unified_files(source_files,
                                                                   unified_prefix=unified_prefix,
                                                                   unified_suffix=suffix,
                                                                   files_per_unified_file=files_per_unified_file))


class InstallationTarget(ContextDerived):
    """Describes the rules that affect where files get installed to."""

    __slots__ = (
        'xpiname',
        'subdir',
        'target',
        'enabled'
    )

    def __init__(self, context):
        ContextDerived.__init__(self, context)

        self.xpiname = context.get('XPI_NAME', '')
        self.subdir = context.get('DIST_SUBDIR', '')
        self.target = context['FINAL_TARGET']
        self.enabled = context['DIST_INSTALL'] is not False

    def is_custom(self):
        """Returns whether or not the target is not derived from the default
        given xpiname and subdir."""

        return FinalTargetValue(dict(
            XPI_NAME=self.xpiname,
            DIST_SUBDIR=self.subdir)) == self.target


class FinalTargetFiles(ContextDerived):
    """Sandbox container object for FINAL_TARGET_FILES, which is a
    HierarchicalStringList.

    We need an object derived from ContextDerived for use in the backend, so
    this object fills that role. It just has a reference to the underlying
    HierarchicalStringList, which is created when parsing FINAL_TARGET_FILES.
    """
    __slots__ = ('files')

    def __init__(self, sandbox, files):
        ContextDerived.__init__(self, sandbox)
        self.files = files


class FinalTargetPreprocessedFiles(ContextDerived):
    """Sandbox container object for FINAL_TARGET_PP_FILES, which is a
    HierarchicalStringList.

    We need an object derived from ContextDerived for use in the backend, so
    this object fills that role. It just has a reference to the underlying
    HierarchicalStringList, which is created when parsing
    FINAL_TARGET_PP_FILES.
    """
    __slots__ = ('files')

    def __init__(self, sandbox, files):
        ContextDerived.__init__(self, sandbox)
        self.files = files


class ObjdirFiles(FinalTargetFiles):
    """Sandbox container object for OBJDIR_FILES, which is a
    HierarchicalStringList.
    """
    @property
    def install_target(self):
        return ''


class ObjdirPreprocessedFiles(FinalTargetPreprocessedFiles):
    """Sandbox container object for OBJDIR_PP_FILES, which is a
    HierarchicalStringList.
    """
    @property
    def install_target(self):
        return ''


class TestHarnessFiles(FinalTargetFiles):
    """Sandbox container object for TEST_HARNESS_FILES,
    which is a HierarchicalStringList.
    """
    @property
    def install_target(self):
        return '_tests'


class Exports(FinalTargetFiles):
    """Context derived container object for EXPORTS, which is a
    HierarchicalStringList.

    We need an object derived from ContextDerived for use in the backend, so
    this object fills that role. It just has a reference to the underlying
    HierarchicalStringList, which is created when parsing EXPORTS.
    """
    @property
    def install_target(self):
        return 'dist/include'


class BrandingFiles(FinalTargetFiles):
    """Sandbox container object for BRANDING_FILES, which is a
    HierarchicalStringList.

    We need an object derived from ContextDerived for use in the backend, so
    this object fills that role. It just has a reference to the underlying
    HierarchicalStringList, which is created when parsing BRANDING_FILES.
    """
    @property
    def install_target(self):
        return 'dist/branding'


class GeneratedFile(ContextDerived):
    """Represents a generated file."""

    __slots__ = (
        'script',
        'method',
        'outputs',
        'inputs',
        'flags',
    )

    def __init__(self, context, script, method, outputs, inputs, flags=()):
        ContextDerived.__init__(self, context)
        self.script = script
        self.method = method
        self.outputs = outputs if isinstance(outputs, tuple) else (outputs,)
        self.inputs = inputs
        self.flags = flags


class ClassPathEntry(object):
    """Represents a classpathentry in an Android Eclipse project."""

    __slots__ = (
        'dstdir',
        'srcdir',
        'path',
        'exclude_patterns',
        'ignore_warnings',
    )

    def __init__(self):
        self.dstdir = None
        self.srcdir = None
        self.path = None
        self.exclude_patterns = []
        self.ignore_warnings = False


class AndroidEclipseProjectData(object):
    """Represents an Android Eclipse project."""

    __slots__ = (
        'name',
        'package_name',
        'is_library',
        'res',
        'assets',
        'libs',
        'manifest',
        'recursive_make_targets',
        'extra_jars',
        'included_projects',
        'referenced_projects',
        '_classpathentries',
        'filtered_resources',
    )

    def __init__(self, name):
        self.name = name
        self.is_library = False
        self.manifest = None
        self.res = None
        self.assets = None
        self.libs = []
        self.recursive_make_targets = []
        self.extra_jars = []
        self.included_projects = []
        self.referenced_projects = []
        self._classpathentries = []
        self.filtered_resources = []

    def add_classpathentry(self, path, srcdir, dstdir, exclude_patterns=[], ignore_warnings=False):
        cpe = ClassPathEntry()
        cpe.srcdir = srcdir
        cpe.dstdir = dstdir
        cpe.path = path
        cpe.exclude_patterns = list(exclude_patterns)
        cpe.ignore_warnings = ignore_warnings
        self._classpathentries.append(cpe)
        return cpe


class AndroidResDirs(ContextDerived):
    """Represents Android resource directories."""

    __slots__ = (
        'paths',
    )

    def __init__(self, context, paths):
        ContextDerived.__init__(self, context)
        self.paths = paths

class AndroidAssetsDirs(ContextDerived):
    """Represents Android assets directories."""

    __slots__ = (
        'paths',
    )

    def __init__(self, context, paths):
        ContextDerived.__init__(self, context)
        self.paths = paths

class AndroidExtraResDirs(ContextDerived):
    """Represents Android extra resource directories.

    Extra resources are resources provided by libraries and including in a
    packaged APK, but not otherwise redistributed.  In practice, this means
    resources included in Fennec but not in GeckoView.
    """

    __slots__ = (
        'paths',
    )

    def __init__(self, context, paths):
        ContextDerived.__init__(self, context)
        self.paths = paths

class AndroidExtraPackages(ContextDerived):
    """Represents Android extra packages."""

    __slots__ = (
        'packages',
    )

    def __init__(self, context, packages):
        ContextDerived.__init__(self, context)
        self.packages = packages

class ChromeManifestEntry(ContextDerived):
    """Represents a chrome.manifest entry."""

    __slots__ = (
        'path',
        'entry',
    )

    def __init__(self, context, manifest_path, entry):
        ContextDerived.__init__(self, context)
        assert isinstance(entry, ManifestEntry)
        self.path = mozpath.join(self.install_target, manifest_path)
        # Ensure the entry is relative to the directory containing the
        # manifest path.
        entry = entry.rebase(mozpath.dirname(manifest_path))
        # Then add the install_target to the entry base directory.
        self.entry = entry.move(mozpath.dirname(self.path))
