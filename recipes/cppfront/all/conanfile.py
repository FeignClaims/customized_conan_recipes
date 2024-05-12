from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rm, save
import os


required_conan_version = ">=2.0.0"


class CppfrontConan(ConanFile):
    name = "cppfront"
    description = "A personal experimental C++ Syntax 2 -> Syntax 1 compiler"
    license = "CC-BY-NC-ND-4.0"
    url = "https://github.com/FeignClaims/customized_conan_recipes"
    homepage = 'https://github.com/hsutter/cppfront'
    topics = ("cpp2", "compiler")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 20

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "CMakeLists.txt", src=self.recipe_folder, dst=self.export_sources_folder)
        copy(self, "CppfrontHelpers.cmake", src=self.recipe_folder, dst=self.export_sources_folder)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    def validate_build(self):
        if self.settings.os == 'Macos' and self.settings.compiler == 'clang':
            raise ConanInvalidConfiguration(f"{self.ref} can't be built by clang on MacOS. Try apple-clang or something else to build it first, then you're free to use.")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.21.3 <4.0.0]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.variables["CPPFRONT_SRC_DIR"] = self.source_folder.replace("\\", "/")
        toolchain.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE",
             src=os.path.join(self.source_folder, "cppfront"),
             dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="CppfrontHelpers.cmake",
             src=os.path.join(self.source_folder, os.pardir),
             dst=self.package_folder)

        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "cppfront")
        self.cpp_info.set_property("cmake_target_name", "cppfront::cppfront")
        self.cpp_info.set_property("cmake_build_modules", [os.path.join(self.package_folder, "CppfrontHelpers.cmake")])