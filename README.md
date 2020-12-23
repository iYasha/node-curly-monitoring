# NodeCurly Monitoring

The Curly monitoring system allows you to monitor the state of the server and notice incorrect work in time.

## Getting Started

```
git clone https://github.com/iYasha/node-curly-monitoring.git
```
```
cd node-curly-monitoring
```
```
docker-compose up --build
```

### Prerequisites

To run the project, you need to install Docker and Docker-Compose.
Details [Here](https://docs.docker.com/compose/install/)

### Installing

The first step is to set up your environment variables. To do this, run

```
mv .docker.env.example .docker.env
```
And customize to fit your needs

## Deployment

Clone repo
```
git clone https://github.com/iYasha/node-curly-monitoring.git
```
Change environment variables
```
mv .docker.env.example .docker.env
```
UP Container with build options
```
docker-compose up --build
```
Set the following command to execute in the crontab
```
echo "*/5 * * * * docker start node_monitoring" >> /etc/crontab
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [MasterCurlyMonitoring](https://github.com/iYasha/master-curly-monitoring/branches/all). 

## Authors

* **Ivan Simantiev** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details