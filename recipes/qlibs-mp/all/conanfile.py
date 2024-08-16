import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, download
from conan.tools.scm import Version

required_conan_version = ">=2.0.0"


class qlibs_mp_conan(ConanFile):
    name = "qlibs-mp"
    description = "MP: ~~Template~~ Meta-Programming library"
    license = "BSL-1.0"
    url = "https://github.com/FeignClaims/customized_conan_recipes"
    homepage = "https://github.com/qlibs/mp"
    topics = ("compile-time", "meta-programming", "ranges", "cpp20", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 20

    @property
    def _compilers_minimum_version(self):
        return {"msvc": "193",
                "gcc": "12",
                "clang": "15"}

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

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

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, url="https://www.boost.org/LICENSE_1_0.txt", filename="LICENSE")

    def generate(self):
        pass

    def build(self):
        apply_conandata_patches(self)

    def package(self):
        copy(self, pattern="LICENSE*",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))
        copy(self,
             pattern="mp",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        self.cpp_info.set_property("cmake_file_name", "mp")
        self.cpp_info.set_property("cmake_target_name", "qlibs::mp")
