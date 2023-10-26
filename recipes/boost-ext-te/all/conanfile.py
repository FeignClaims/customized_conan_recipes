from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, download
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=2.0.0"


class TeConan(ConanFile):
    name = "boost-ext-te"
    description = "TE: C++17 Run-time polymorphism (type erasure) library"
    license = "BSL-1.0"
    url = "https://github.com/FeignClaims/customized_conan_recipes"
    homepage = "https://github.com/boost-ext/te"
    topics = ("concepts", "metaprogramming", "header-only", "cpp17", "type-erasure", "polymorphism")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 17

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    @property
    def _should_test(self):
        return not self.conf.get("tools.build:skip_test", default=True, check_type=bool)

    def build_requirements(self):
        if self._should_test:
            self.build_requires("cmake/[>=3.1 <4.0.0]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        if self._should_test:
            toolchain = CMakeToolchain(self)
            toolchain.cache_variables["ENABLE_MEMCHECK"] = self._should_test
            toolchain.generate()

    def build(self):
        apply_conandata_patches(self)
        if self._should_test:
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def package(self):
        download(self,
                 url="http://www.boost.org/LICENSE_1_0.txt",
                 filename=os.path.join(self.package_folder, "licenses"))
        copy(self,
             pattern="*.hpp",
             src=os.path.join(self.source_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        self.cpp_info.set_property("cmake_file_name", "te")
        self.cpp_info.set_property("cmake_target_name", "boost-ext-te::te")
