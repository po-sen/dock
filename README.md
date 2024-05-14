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
$ dock image set-registry posen -y
  Set [DEFAULT] registry = posen

# Set default registry for all charts
$ dock chart set-registry oci://registry-1.docker.io/posen -y
  Set [DEFAULT] oci-registry = oci://registry-1.docker.io/posen

# Add images/myFirstImage/ to the configuration
$ dock image set images/myFirstImage/ -y
  Set [images/myFirstImage]
  Set [images/myFirstImage] type = image
  Set [images/myFirstImage] image-file = Dockerfile
  Unset [images/myFirstImage] image-name
  Unset [images/myFirstImage] depends-on

# Add images/mySecondImage/ to the configuration
$ dock image set images/mySecondImage/ --depends-on=images/myFirstImage/ -y
  Set [images/mySecondImage]
  Set [images/mySecondImage] type = image
  Set [images/mySecondImage] image-file = Dockerfile
  Unset [images/mySecondImage] image-name
  Set [images/mySecondImage] depends-on = images/myFirstImage

# Add charts/myFirstChart/ to the configuration
$ dock chart set charts/myFirstChart/ -y
  Set [charts/myFirstChart]
  Set [charts/myFirstChart] type = chart

# Add charts/mySecondChart/ to the configuration
$ dock chart set charts/mySecondChart/ -y
  Set [charts/mySecondChart]
  Set [charts/mySecondChart] type = chart
```

And the content of `dock.ini` is as follows:

```bash
$ cat dock.ini
[DEFAULT]
registry = posen
oci-registry = oci://registry-1.docker.io/posen

[images/myFirstImage]
type = image
image-file = Dockerfile

[images/mySecondImage]
type = image
image-file = Dockerfile
depends-on = images/myFirstImage

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

## Links

- Source: https://github.com/Posen2101024/dock
- PyPI: https://pypi.org/project/dock-cli/
