# dynpojschemer

This project provides a dynamic jschema package, you can generate sample json from a provided jschema. The supported jschema is the version used on Open API Specification. The samples can be generated from a pool of random values or interactively.

## Installation

Install from source:

```
$ git clone git@github.com:dynpo/jschemer.git
$ cd jschemer
$ pip install .
```

## Example

By default, the rbkcli will attempt to read the the Rubrik Cluster credentials from the following environment variables:

```python
import dynpojschemer

my_schema = {
  "schema": {
          "UserDefinition": {
            "type": "object",
            "properties": {
              "password": {
                "x-secret": true,
                "type": "string"
              },
              "firstName": {
                "type": "string"
              },
              "mfaServerId": {
                "type": "string"
              },
              "contactNumber": {
                "type": "string"
              },
              "username": {
                "type": "string"
              },
              "emailAddress": {
                "type": "string"
              },
              "lastName": {
                "type": "string"
              }
            },
            "required": [
              "username",
              "password"
            ]
          }
        }
    }

schemer = dynpoinput.JSchemer(my_schema)
my_sample = schemer.sample()
print(my_sample)

```


## Documentation

Here are some resources to get you started! If you find any challenges from this project are not properly documented or are unclear, please raise an issue and let us know!

* [Documentation Summary](docs/SUMMARY.md)

## How You Can Help

We glady welcome contributions from the community. From updating the documentation to adding more functions for Python, all ideas are welcome.

* [Contributing Guide](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

## License

* [MIT License](LICENSE)

## About Dynpo

It is a group of libraries to facilitate Python Automation, seeks to empower dynamic coding and decrease the time to maintain and write new code.
