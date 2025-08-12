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

 to use casa os 

run 

git clone --depth=1 https://github.com/HaithamSaqr/odoo-18-docker-compose-pgbouncer odoo18

then inport   casaos-compose.yml  to casa

 

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
 
