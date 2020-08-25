from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "aws-lambda-cpp"
    description = "C++ implementation of the lambda runtime API"
    topics = ("conan", "aws-lambda-cpp", "aws-lambda", "aws", "lambda")
    url = "https://github.com/wi3ard/conan-aws-lambda-cpp"
    homepage = "https://github.com/awslabs/aws-lambda-cpp"
    license = "Apache-2.0"
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [
        True, False], "lto": [True, False]}
    default_options = {"shared": False, "fPIC": True, "lto": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    requires = (
        "libcurl/7.71.1"
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

        if "patches" in self.conan_data and self.version in self.conan_data["patches"]:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(**patch)

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["ENABLE_LTO"] = self.options.lto
            self._cmake.definitions["ENABLE_TESTS"] = False
            self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses",
                  src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
