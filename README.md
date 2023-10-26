# Customized Conan Recipe

:warning: This repository contains my customized conan recipes.

## Why repository?

This repository is intended to benefit from [Adding a folder with conan-center-index clone as a remote](https://github.com/conan-io/conan/pull/13930), which allows to **use any folder structured like [conan-io/conan-center-index](https://github.com/conan-io/conan-center-index) as a conan remote!**

## Get Started

Currently, you can clone this and run `conan export recipes/<recipe>/all --version <the version specified in 'recipes/<recipe>/config.yml'>` to export the wanted recipe to your conan cache, then run conan normally.

Or better, you can setup [a conan server to manage this](https://docs.conan.io/2/tutorial/conan_repositories.html).
