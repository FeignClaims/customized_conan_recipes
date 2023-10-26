#!/usr/bin/env python3
import os
import yaml
import subprocess


def export_conan_recipes(root_dir):
    """
    Export all recipes inside a folder using the corresponding ``config.yml``
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'config.yml':
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as file:
                    try:
                        config = yaml.safe_load(file)
                    except yaml.YAMLError as exc:
                        print(f"Error in {file_path}: {exc}")
                        continue

                    if 'versions' in config:
                        for version, details in config['versions'].items():
                            if 'folder' in details:
                                folder_path = os.path.join(dirpath, details['folder'])
                                subprocess.run(['conan', 'export', folder_path, '--version', version])


if __name__ == "__main__":
    export_conan_recipes('recipes')
