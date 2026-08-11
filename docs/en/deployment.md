# Deployment

Production deployment guide for the Library API project.

---

## Deployment Options

### Option 1: Docker Compose (Recommended for Small/Medium)

If you have **Docker** installed, getting started is much simpler. After cloning the repository and creating the `.env` file, run the following command to start the **Library API** application, the **PostgreSQL** database, apply the database migrations, and launch the API documentation.

> [!warning]
> When using **Docker**, do not wrap values in the `.env` file with quotes. Docker reads environment variables as plain strings, and including quotes may lead to unexpected behavior.

```sh
docker compose up
```

Now you enter inside the container using:

```sh
docker exec -it libraryapi-app-1 sh
```

Then, run the command described in [Create Initial User Admin](docs/en/installation.md#create-initial-admin-user) to create the administrator account.

When running the application with Docker Compose, the API documentation is exposed on port **80**. Open your browser and navigate to `http://localhost` or `http://127.0.0.1` to access it.

---

### Option 2: Kubernetes (Recommended for Scale)

If you want to run the application with **Kubernetes**, you will need to install [kind](https://kind.sigs.k8s.io/), [kubectl](https://kubernetes.io/docs/tasks/tools/) and [Helm](https://helm.sh/) beforehand.

#### Creating cluster

To create a cluster using kind go to where the kind file is with:

```sh
cd kubernetes/kind
```

> [!info]
> If **KinD** is on **Windows**, you can go for the WSL files using:
> `cd \\wsl.localhost\Ubuntu\home\<username>\<path>`.

Create the cluster with:

```sh
kind create cluster --config config.yaml
```

You can delete the cluster with:
```sh
kind delete cluster
```

#### Adding Docker Images to Cluster Nodes

You can use the same images from **Docker Compose**, but you will need to change the tag to semantic versioning tags. You can also build app images with:

```sh
docker build -t libraryapi-app:1.0.0 .
```

And the MkDocs image with:

```sh
docker build -t libraryapi-docs:1.0.0 -f Dockerfile.mkdocs .
```

Load these images into the cluster nodes with:

```sh
kind load docker-image libraryapi-app:1.0.0
```

```sh
kind load docker-image libraryapi-docs:1.0.0
```

#### Adding Ingress

We will use the **Kong Ingress Controller**, so we need to install the Gateway API CRDs and the **Kong Ingress Controller** with **Helm**.

Install the CRDs first with:

```sh
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
```

Add the **Kong** repository to our **Helm** with:

```sh
helm repo add kong https://charts.konghq.com
```

```sh
helm repo update
```

And install the Kong Ingress Controller with:

```sh
helm upgrade --install --namespace kong --create-namespace kong kong/ingress --version 0.24.0 -f kubernetes/local/kong/values.yaml
```

> [!warning]
> Check the version of your **kong/ingress** before installing on **Helm**, since it can change with time.

#### Installing application

Now to install our application go to the charts folder with:

```sh
cd kubernetes/charts/library-api
```

and run:

```sh
helm upgrade --install --namespace library-api --create-namespace library-api . -f values-local.yaml
```
> [!note]
> On the first run, **Helm** will prompt you to build the chart's dependency, which is the **PostgreSQL** database. Run it with:
`helm dependency build`.

#### Modify hosts file

When using the Ingress we need to add our test hosts on our system hosts file.
- **Windows:** `C:\Windows\System32\drivers\etc\hosts`
- **Linux:** `/etc/hosts`

Add the following entry to your system's `hosts` file:

```text
127.0.0.1 library-api.localhost.com library-api-mkdocs.localhost.com
```

This maps both hostnames to `127.0.0.1`, allowing them to resolve to your local machine.

#### Verifying

We can check if everything is working going to the URLs:
- Application: `library-api.localhost.com/docs`
- Documentation: `library-api-mkdocs.localhost.com`
