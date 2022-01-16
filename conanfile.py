from conans import ConanFile, CMake, tools
import os, shutil

class ConanPackage(ConanFile):
    name = "libgit2cpp"
    version = "0.0.1"
    description = "This is a package for libgit2cpp by AndreyG on github"
    license = "Unknown"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    url = "https://github.com/AndreyG/libgit2cpp"
    settings = ("os", "build_type", "arch", "compiler")
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    
    requires=[  
        "libgit2/1.3.0",
        ]

    generators = "cmake"
    cmake = None
    exports_sources = "cmake*", "lib/*", "CMakeLists.txt"

    _source_subfolder = "source_subfolder"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
#        del self.settings.compiler.libcxx
#        del self.settings.compiler.cppstd

    def source(self):
        self.run("git clone https://github.com/AndreyG/libgit2cpp.git")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["USE_BOOST"] = "OFF"
        cmake.definitions["BUNDLE_LIBGIT2"] = "OFF"
        cmake.definitions["BUILD_LIBGIT2CPP_EXAMPLES"] = "OFF"
        
#        cmake.configure(source_folder="libgit2cpp")
        cmake.configure()
        cmake.build()
        
    def package(self):
        self.copy("*.h", dst="include/git2cpp", src=".", keep_path=False)
        self.copy("*.hpp", dst="include/git2cpp", src=".", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        
    def package_info(self):
        self.cpp_info.name = "git2cpp"
#        self.cpp_info.names["generator_name"] = "<PKG_NAME>"
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libs = tools.collect_libs(self)  # The libs to link against
        self.cpp_info.system_libs = []  # System libs to link against
        self.cpp_info.libdirs = ['.', 'lib']  # Directories where libraries can be found
        self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc. can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        self.cpp_info.srcdirs = []  # Directories where sources can be found (debugging, reusing sources)
        self.cpp_info.build_modules = []  # Build system utility module files
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cxxflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
        self.cpp_info.components  # Dictionary with the different components a package may have
