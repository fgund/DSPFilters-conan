from conans import ConanFile, CMake, tools


class DSPFiltersConan(ConanFile):
    name = "DSPFilters"
    version = "1.0"
    license = "MIT"
    url = ""
    description = "A Collection of Useful C++ Classes for Digital Signal Processing"
    topics = ("signal processing", "filters")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/fgund/DSPFilters.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("DSPFilters/shared/DSPFilters/CMakeLists.txt", "project (DSPFilters CXX)",
                              '''project (DSPFilters CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="DSPFilters/shared/DSPFilters")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="DSPFilters/shared/DSPFilters/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["DSPFilters"]

