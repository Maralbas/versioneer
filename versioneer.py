#!/usr/bin/python3
#coding=utf-8

"""
    Simple version manager using cli command.

    Args:
        project (optional): The project that will zip and have an updated version.
                            If the argument is not defined, then the project will be the actual folder.
        --update (optional): Number of decimals to increment the next version.
        --reset (optional): Reset version to 0.0.
"""

import os
import shutil
import argparse


def get_version(f_version_loc):
    """ Get version.
        If doens't exist the file with the version creates it.

        Args:
            f_version_loc: Location of the file with the version of the project

        Returns:
            version: The number (float) of the version
    """

    try:
        f_version = open(f_version_loc, "r+")
        version = float(f_version.read())

    except FileNotFoundError:
        f_version = open(f_version_loc, "w")
        f_version.write("0.0")

        version = 0.0

    finally:
        f_version.close()

    return version


def change_version(version, f_version_loc):
    """ Updates the version file to have the new version of the project

        Args:
            version: The new version
            f_version_loc: Location of the file that will have the new version
    """

    with open(f_version_loc, "w") as f_version:
        f_version.write(version)


def update_version(version, decimals_count):
    """ Updates the file to the next version.
        This code is to "round" to the decimals of the desired uptade.
        ex: 0.004 update 0.1 we want the next version to be 0.1 and not 0.1004.

        Args:
            version: The number of version that will be updated
            decimals_count: How many decimals_count the new version will have

        Return:
            version: The number (float) of the new version
    """

    update = 1 if decimals_count == 0 else 1 / 10 ** decimals_count
    version += update

    version = str(version)

    # find the location of . and then add to the string only the number of decimals that the desired version has
    loc_decimal = version.find(".") + 1
    version = "{}.{}".format(
        version[:loc_decimal - 1], version[loc_decimal: loc_decimal + decimals_count])

    return float(version)


def backup(project, version):
    """ Creates the zip file

        Args:
            project: Location of the project
            version: Actual number of the version
    """

    print("Backing up {}".format(project))

    zipFilename = "{}/{}_{}.zip".format(os.path.dirname(
        project), os.path.basename(project), str(version))

    shutil.make_archive(zipFilename, "zip")

    print("BackUp Finished!!")


if __name__ == "__main__":
    # Add the arguments that can be defined calling the program
    # The first argument will be the file to backup, if there is no argument then
    # it is the actual folder
    parser = argparse.ArgumentParser(description="Backup file")
    parser.add_argument("project", default=".", nargs="?",
                        help="name of the file")
    parser.add_argument("-u", "--update", default=0, type=int,
                        help="number of decimals to increment the next version")
    parser.add_argument("-r", "--reset", action="store_true",
                        help="reset version to 0.0")
    args = parser.parse_args()

    project = os.path.abspath("./{}".format(args.project))
    f_version_loc = "{}/versioneer.txt".format(project)

    # Reset version to 0.0 in case of the optional argument --reset is used
    if args.reset:
        print("Reseting version to 0.0")
        change_version("0.0", f_version_loc)
        print("Reset Finished!!")

        quit()

    # In case it is not a folder, raise an Exception
    if not os.path.isdir(project):
        raise Exception("It must be an existing folder")

    # get version
    version = get_version(f_version_loc)

    # version
    backup(project, version)

    # update version and the file
    version = update_version(version, args.update)

    print("Updating version to {}".format(version))

    change_version(str(version), f_version_loc)

    print("Update Finished!!")
