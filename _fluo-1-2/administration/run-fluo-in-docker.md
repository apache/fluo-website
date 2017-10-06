---
title: Run Fluo in Docker
category: administration
order: 4
---

## Obtain the Docker image

To obtain the docker image created by this project, you can either pull it from DockerHub at
`apache/fluo` or build it yourself. To pull the image from DockerHub, run the command below:

    docker pull apache/fluo

While it is easier to pull from DockerHub, the image will default to the software versions below:

| Software    | Version |
|-------------|---------|
| [Fluo]      | 1.2.0   |
| [Accumulo]  | 1.8.1   |
| [Hadoop]    | 2.7.3   |
| [Zookeeper] | 3.4.9   |

If these versions do not match what is running on your cluster, you should consider [building
your own image][build-image] with matching versions.

## Image basics

The entrypoint for the Fluo docker image is the `fluo` script. While the primary use
case for this image is to start an oracle or worker, you can run other commands in the
`fluo` script to test out the image:

```bash
# No arguments prints Fluo command usage
docker run apache/fluo
# Print Fluo version
docker run apache/fluo version
# Print Fluo classpath
docker run apache/fluo classpath
```

## Run application in Docker

Before starting a Fluo oracle and worker using the Fluo Docker image, [initialize your Fluo application][initialize]. 
Next, choose a method below to run the oracle and worker(s) of your Fluo application. In the examples below, the Fluo
application is named `myapp` and was initialized using a Zookeeper node on `zkhost`.

### Docker engine

Use the `docker` command to start local docker containers.

1. Start a Fluo oracle for `myapp` application connecting to a Zookeeper at `zkhost`.

        docker run -d --network="host" apache/fluo oracle -a myapp -o fluo.connection.zookeepers=zkhost/fluo

    The command above uses `-d` to run the container in the background and `--network="host"` to run the container
    on the host's network stack.

2. Start Fluo worker(s). Execute this command multiple times to start multiple workers.

        docker run -d --network="host" apache/fluo worker -a myapp -o fluo.connection.zookeepers=zkhost/fluo

### Marathon

Using the [Marathon] UI, you can create applications using JSON configuration.

The JSON below can be used to start a Fluo oracle.

```json
{
  "id": "myapp-fluo-oracle",
  "cmd": "fluo oracle -a myapp -o fluo.connection.zookeepers=zkhost/fluo",
  "cpus": 1,
  "mem": 256,
  "disk": 0,
  "instances": 1,
  "container": {
    "docker": {
      "image": "apache/fluo",
      "network": "HOST"
    },
    "type": "DOCKER"
  }
}
```

The JSON below can be used to start Fluo worker(s). Modify instances to start multiple workers.

```json
{
  "id": "myapp-fluo-worker",
  "cmd": "fluo worker -a myapp -o fluo.connection.zookeepers=zkhost/fluo",
  "cpus": 1,
  "mem": 512,
  "disk": 0,
  "instances": 1,
  "container": {
    "docker": {
      "image": "apache/fluo",
      "network": "HOST"
    },
    "type": "DOCKER"
  }
}
```

## Next Steps

Learn how to [manage Fluo applications][manage].

[build-image]: https://github.com/apache/fluo-docker/blob/master/README.md#build-the-docker-image
[manage]: {{ page.docs_base }}/administration/manage-applications/
[Fluo]: https://fluo.apache.org/
[Accumulo]: https://accumulo.apache.org/
[Hadoop]: https://hadoop.apache.org/
[Zookeeper]: https://zookeeper.apache.org/
[intialize]: {{ page.docs_base }}/administration/initialize/
[Marathon]: https://mesosphere.github.io/marathon/
