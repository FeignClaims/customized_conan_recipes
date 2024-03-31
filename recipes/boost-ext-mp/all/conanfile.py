import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy
from conan.tools.layout import basic_layout
from conan.tools.scm import Version, Git

required_conan_version = ">=2.0.0"


class MpConan(ConanFile):
    name = "boost-ext-mp"
    description = "MP: C++20 ~~Template~~ Meta-Programming"
    license = "BSL-1.0"
    url = "https://github.com/FeignClaims/customized_conan_recipes"
    homepage = "https://boost-ext.github.io/mp/"
    topics = ("reflection", "stl", "compile-time", "meta-programming", "ranges", "cpp20", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True
    options = {
        "disable_module": [True, False]
    }
    default_options = {
        "disable_module": False
    }

    @property
    def _min_cppstd(self):
        return 20

    @property
    def _compilers_minimum_version(self):
        return {"msvc": "193",
                "gcc": "11",
                "clang": "13",
                "apple-clang": "14"}

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support."
            )

    @property
    def _should_test(self):
        return not self.conf.get("tools.build:skip_test", default=True, check_type=bool)

    def build_requirements(self):
        if self._should_test:
            self.test_requires("boost-ext-ut/1.1.9")
        self.tool_requires("cmake/[>=3.23 <4.0.0]")

    def source(self):
        data = self.conan_data["sources"][self.version]
        git = Git(self)
        git.clone(data["url"], target=".", args=["--recursive"])
        git.checkout(data["commit"])

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.cache_variables["BOOST_MP_BUILD_EXAMPLES"] = False
        toolchain.cache_variables["BOOST_MP_BUILD_TESTS"] = self._should_test
        # TODO: cmake.install() and support module
        toolchain.cache_variables["BOOST_MP_DISABLE_MODULE"] = self.options.get_safe("disable_module", False)
        toolchain.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE*",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))
        copy(self,
             pattern="*",
             src=os.path.join(self.source_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        self.cpp_info.set_property("cmake_file_name", "mp")
        self.cpp_info.set_property("cmake_target_name", "boost-ext-mp::mp")
