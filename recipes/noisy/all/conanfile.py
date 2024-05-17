import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, download
from conan.tools.scm import Version

required_conan_version = ">=2.0.0"


class NoisyConan(ConanFile):
    name = "noisy"
    description = "A C++ type to trace calls to special member functions."
    license = "MIT"
    url = "https://github.com/FeignClaims/customized_conan_recipes"
    homepage = "https://github.com/VincentZalzal/noisy"
    topics = ("cpp11", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 11

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        pass

    def build(self):
        apply_conandata_patches(self)

    def package(self):
        copy(self, pattern="LICENSE*",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))
        copy(self,
             pattern="noisy.h",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        self.cpp_info.set_property("cmake_file_name", "noisy")
        self.cpp_info.set_property("cmake_target_name", "noisy::noisy")
