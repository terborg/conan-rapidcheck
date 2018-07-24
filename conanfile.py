
from conans import ConanFile, CMake, tools


class RapidCheckConan(ConanFile):
    name = "rapidcheck"
    version = "0.0.1"
    license = "BSD 2-clause"
    url = "https://github.com/emil-e/rapidcheck"
    description = "RapidCheck is a C++ framework for property based testing inspired by QuickCheck and other similar frameworks."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    
    #requires = ( "gtest/1.8.0@bincrafters/stable" )

    def source(self):
        self.run( "git clone --depth 1 https://github.com/emil-e/rapidcheck" )
        
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("rapidcheck/CMakeLists.txt", "project(rapidcheck CXX)",
                              '''project(rapidcheck CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="rapidcheck")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        
        self.copy("*.h",   dst="include", src="rapidcheck/include")
        self.copy("*.hpp", dst="include", src="rapidcheck/include")
        
        self.copy("*rapidcheck.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["rapidcheck"]

