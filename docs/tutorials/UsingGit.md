# Using Git

This tutorial will cover how to pull new changes from git and checkout a specific version. Steps 1 only has to be completed once, when you first download the content. Steps 2-6 require that you be in the main project directory.

1. Clone the repository:

    ``` SHELL
    git clone
    ```

2. Initialize submodules:

    ``` SHELL
    git submodule init
    ```

3. Pull content from submodules:

    ``` SHELL
    git submodule update
    ```

4. Fetch newest content:

    ``` SHELL
    git checkout main
    git pull
    git submodule update
    ```

5. Find release numbers:

    ``` SHELL
    git tag
    ```

6. Checkout a release:

    ``` SHELL
    git checkout <tag>
    ```

    * Replace `<tag>` with the version number for the version you found in step 5.
