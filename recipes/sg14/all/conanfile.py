import os

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, download

required_conan_version = ">=2.0.0"


class sg14_conan(ConanFile):
    name = "sg14"
    description = "Header-only C++ containers and algorithms from the SG14 Low Latency study group"
    license = "BSL-1.0"
    url = "https://github.com/FeignClaims/customized_conan_recipes"
    homepage = "https://github.com/Quuxplusone/SG14"
    topics = ("container", "algorithm", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 14

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
        download(self, url="https://www.boost.org/LICENSE_1_0.txt", filename="LICENSE")

    def generate(self):
        pass

    def build(self):
        apply_conandata_patches(self)

    def package(self):
        copy(self,
             pattern="LICENSE*",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))
        copy(self,
             pattern="*",
             src=os.path.join(self.source_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        self.cpp_info.set_property("cmake_file_name", "sg14")
        self.cpp_info.set_property("cmake_target_name", "sg14::sg14")
