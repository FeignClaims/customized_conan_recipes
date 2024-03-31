from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, rm, rmdir, save, load
import os


required_conan_version = ">=2.0.0"


class QtOpenCVConan(ConanFile):
    name = "qtopencv"
    description = "Qt and OpenCV2 Integration, cv::Mat <==> QImage"
    license = "MIT"
    url = "https://github.com/FeignClaims/customized_conan_recipes"
    homepage = "https://github.com/dbzhang800/QtOpenCV"
    topics = ("opengl", "texture")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 11

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "CMakeLists.txt", src=self.recipe_folder, dst=self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("opencv/4.5.5")
        self.requires("qt/6.5.3")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.27 <4.0.0]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.variables["QTOPENCV_SRC_DIR"] = self.source_folder.replace("\\", "/")
        toolchain.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def _save_license(self):
        temp = open(os.path.join(self.source_folder, "cvmatandqimage.cpp")).read()
        temp = temp[temp.find("Copyright", 1):temp.find("SOFTWARE.", 1)+9]

        license_contents = ""
        for line in temp.splitlines():
            license_contents += line.removeprefix("** ").removeprefix("**")
            license_contents += '\n'

        save(self, os.path.join(self.package_folder, "licenses", "LICENSE"), license_contents)

    def package(self):
        self._save_license()

        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "share"))
        rm(self, "*.la", os.path.join(self.package_folder, "lib"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "lib"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.libs = ["QtOpenCV"]

        self.cpp_info.set_property("cmake_file_name", "qtopencv")
        self.cpp_info.set_property("cmake_target_name", "qtopencv::qtopencv")
