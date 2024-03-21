# Customized Conan Recipe

This repository contains my customized conan recipes.

## Why repository?

This repository is intended to benefit from [Adding a folder with conan-center-index clone as a remote](https://github.com/conan-io/conan/pull/13930), which allows to **use any folder structured like [conan-io/conan-center-index](https://github.com/conan-io/conan-center-index) as a conan remote!**

## Get Started

First, clone this repository locally.

```bash
git clone https://github.com/FeignClaims/customized_conan_recipes.git
```

Then, add this folder as a conan remote:

```bash
conan remote add <remote_name> <path_to_this_repository> -t local-recipes-index
```

Or better, you can setup [a conan server to manage this](https://docs.conan.io/2/devops/using_conancenter.html).
