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

Where `dock.ini` can be empty or nonexistent, you can use the following command to update `dock.ini`:

```bash
# Set default registry for all images
$ dock image config set-registry posen
Set [DEFAULT] registry = posen

# Set default registry for all charts
$ dock chart config set-registry oci://registry-1.docker.io/posen
Set [DEFAULT] oci-registry = oci://registry-1.docker.io/posen

# Add images/myFirstImage/ to the configuration
$ dock image config set images/myFirstImage/
Set [images/myFirstImage] image-file = Dockerfile
Set [images/myFirstImage] type = image
images/myFirstImage:
- registry: posen
- image-file: Dockerfile
- image-name:
- depends-on:
- type: image

# Add images/mySecondImage/ to the configuration
$ dock image config set images/mySecondImage/ --depends-on=images/myFirstImage/
Set [images/mySecondImage] image-file = Dockerfile
Set [images/mySecondImage] depends-on = images/myFirstImage
Set [images/mySecondImage] type = image
images/mySecondImage:
- registry: posen
- image-file: Dockerfile
- image-name:
- depends-on: images/myFirstImage
- type: image

# Add charts/myFirstChart/ to the configuration
$ dock chart config set charts/myFirstChart/
Set [charts/myFirstChart] type = chart
charts/myFirstChart:
- oci-registry: oci://registry-1.docker.io/posen
- type: chart

# Add charts/mySecondChart/ to the configuration
$ dock chart config set charts/mySecondChart/
Set [charts/mySecondChart] type = chart
charts/mySecondChart:
- oci-registry: oci://registry-1.docker.io/posen
- type: chart
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
depends-on = images/myFirstImage
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
