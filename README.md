# Dock CLI

CLI tool for managing containerized applications in a Git repository.

It allows you to implement automatic version control for Docker images and Helm charts in a quick and easy way.

## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/).

```bash
$ pip install -U dock-cli
```

## Getting Started

Assuming you have a repository with multiple Docker images and Helm charts that require automatic version control.

For example, the folder structure of your repository is as follows:

```
<repository_root>/
 | - .git/
 | - charts/
 | | - myFirstChart/
 | | | - Chart.yaml
 | | - mySecondChart/
 | | | - Chart.yaml
 | - images/
 | | - myFirstImage/
 | | | - Dockerfile
 | | - mySecondImage/
 | | | - Dockerfile
 | - dock.ini
```

And the content of `dock.ini` is as follows:

```bash
$ cat dock.ini
[DEFAULT]
registry = posen
oci-registry = oci://registry-1.docker.io/posen

[images/myFirstImage]
image-file = Dockerfile
type = image

[images/mySecondImage]
image-file = Dockerfile
type = image

[charts/myFirstChart]
type = chart

[charts/mySecondChart]
type = chart
```

Then you can use the following command to push to the registry:

- List all images and charts
    ```bash
    $ dock image list
    images/myFirstImage
    images/mySecondImage
    $ dock chart list
    charts/myFirstChart
    charts/mySecondChart
    ```
- Build all images and Package all charts
    ```bash
    $ dock image list | xargs -r dock image build
    $ dock chart list | xargs -r dock chart package
    ```
- Push all images and charts
    ```bash
    $ dock image list | xargs -r dock image push
    $ dock chart list | xargs -r dock chart push
    ```
