# Installing Odoo 18.0 with one command (Supports multiple Odoo instances on one server).

## Quick Installation

Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) yourself, then run the following to set up first Odoo instance @ `localhost:10018` (default master password: `P@ss@123`):

``` bash
cd /opt
curl -s https://raw.githubusercontent.com/HaithamSaqr/odoo-18-docker-compose-pgbouncer/master/run.sh | sudo bash -s odoo18 10018 20018
```
and/or run the following to set up another Odoo instance @ `localhost:11018` (default master password: `P@ss@123`):

``` bash
cd /opt
curl -s https://raw.githubusercontent.com/HaithamSaqr/odoo-18-docker-compose-pgbouncer/master/run.sh | sudo bash -s odoo18 11018 21018
```

Some arguments:
* First argument (**odoo-one**): Odoo deploy folder
* Second argument (**10018**): Odoo port
* Third argument (**20018**): live chat port

If `curl` is not found, install it:

``` bash
$ sudo apt-get install curl
# or
$ sudo yum install curl
```

<p>
<img src="screenshots/odoo-18-docker-compose.gif" width="100%">
</p>

## Usage

Start the container:
``` sh
docker-compose up
```
Then open `localhost:10018` to access Odoo 18.

- **If you get any permission issues**, change the folder permission to make sure that the container is able to access the directory:

``` sh
$ sudo chmod -R 777 addons
$ sudo chmod -R 777 etc
$ sudo chmod -R 777 postgresql
```

- If you want to start the server with a different port, change **10018** to another value in **docker-compose.yml** inside the parent dir:

```
ports:
 - "10018:8069"
```

