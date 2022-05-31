# NodeCurly Monitoring

The Curly monitoring system allows you to monitor the state of the server and notice incorrect work in time.

## Getting Started

```
git clone https://github.com/iYasha/node-curly-monitoring.git
```
```
pip install -r /path/to/node-curly-monitoring/src/requirements.txt
```

### Installing

Set the following command to execute in the crontab, like this:
```
echo "*/5 * * * * python /path/to/node-curly-monitoring/src/main.py" >> /etc/crontab
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [MasterCurlyMonitoring](https://github.com/iYasha/master-curly-monitoring/branches/all). 

## Authors

* **Ivan Simantiev** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details