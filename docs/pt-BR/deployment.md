# Implantação

Guia de implantação em produção para o projeto Library API.

---

## Opções de Implantação

### Opção 1: Docker Compose (Recomendado para pequeno/médio porte)

Se você tiver o **Docker** instalado, começar é muito mais simples. Após clonar o repositório e criar o arquivo `.env`, execute o comando abaixo para iniciar a aplicação **Library API** e o banco de dados **PostgreSQL**, aplicar as migrações do banco de dados e disponibilizar a documentação da API.

> [!warning]
> Ao usar o **Docker**, não coloque os valores do arquivo `.env` entre aspas. O Docker lê variáveis ​​de ambiente como strings simples, e a inclusão de aspas pode causar comportamentos inesperados.

```sh
docker compose up
```

Agora, entre no container utilizando:

```sh
docker exec -it libraryapi-app-1 sh
```

Em seguida, execute o comando descrito em [Criar Usuário Administrador Inicial](docs/pt-BR/installation.md#criar-usuário-administrador-inicial) para criar a conta de administrador.

Ao executar a aplicação com o Docker Compose, a documentação da API fica disponível na porta **80**. Abra o seu navegador e acesse `http://localhost` ou `http://127.0.0.1` para visualizá-la.

---

### Opção 2: Kubernetes (Recomendado para escalabilidade)

Se você quiser executar a aplicação com **Kubernetes**, precisará instalar o [kind](https://kind.sigs.k8s.io/), o [kubectl](https://kubernetes.io/docs/tasks/tools/) e o [Helm](https://helm.sh/) com antecedência.

#### Criando Cluster

Para criar um cluster usando o kind, navegue até o diretório onde o arquivo do kind está localizado com:

```sh
cd kubernetes/kind
```

> [!info]
> Se estiver usando o **KinD** no **Windows**, você pode acessar os arquivos do WSL utilizando:
> `cd \\wsl.localhost\Ubuntu\home\<username>\<path>`.

Crie o cluster com:

```sh
kind create cluster --config config.yaml
```

Você pode excluir o cluster com:
```sh
kind delete cluster
```

#### Adicionando Imagens do Docker aos Nós do Cluster

Você pode usar as mesmas imagens do **Docker Compose**, mas precisará alterar a tag para tags de controle de versão semântico. Você também pode criar imagens de aplicativos com:

```sh
docker build -t libraryapi-app:1.0.0 .
```

E a imagem MkDocs com:

```sh
docker build -t libraryapi-docs:1.0.0 -f Dockerfile.mkdocs .
```

Carregue essas imagens nos nós do cluster com:

```sh
tipo carregar docker-image libraryapi-app:1.0.0
```

```sh
tipo carregar docker-image libraryapi-docs:1.0.0
```

#### Adicionando Ingress

Utilizaremos o **Kong Ingress Controller**; portanto, precisamos instalar os CRDs da Gateway API e o **Kong Ingress Controller** usando o **Helm**.

Primeiro, instale os CRDs com:

```sh
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
```

Adicione o repositório do **Kong** ao **Helm** com:

```sh
helm repo add kong https://charts.konghq.com
```

```sh
helm repo update
```

E instale o Kong Ingress Controller com:

```sh
helm upgrade --install --namespace kong --create-namespace kong kong/ingress --version 0.24.0 -f kubernetes/local/kong/values.yaml
```

> [!warning]
> Verifique a versão do **kong/ingress** antes de instalá-lo via **Helm**, pois ela pode mudar com o tempo.

#### Instalando aplicativo

Agora, para instalar nossa aplicação, vá para a pasta dos charts com:

```sh
cd kubernetes/charts/library-api
```

e execute:

```sh
helm upgrade --install --namespace library-api --create-namespace library-api . -f values-local.yaml
```
> [!note]
> Na primeira execução, o **Helm** solicitará que você compile a dependência do chart, que é o banco de dados **PostgreSQL**. Execute o comando:
`helm dependency build`.

#### Modificar o arquivo hosts

Ao utilizar o Ingress, precisamos adicionar nossos hosts de teste ao arquivo `hosts` do sistema.
- **Windows:** `C:\Windows\System32\drivers\etc\hosts`
- **Linux:** `/etc/hosts`

Adicione a seguinte entrada ao arquivo `hosts` do seu sistema:

```text
127.0.0.1 library-api.localhost.com library-api-mkdocs.localhost.com
```

Isso mapeia ambos os nomes de host para `127.0.0.1`, permitindo que sejam resolvidos para a sua máquina local.

#### Verificando

Podemos verificar se tudo está funcionando acessando as URLs:
- Aplicação: `library-api.localhost.com/docs`
- Documentação: `library-api-mkdocs.localhost.com`
