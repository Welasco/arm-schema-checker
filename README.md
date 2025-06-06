# ARM Schema Checker

A simple Python tool to analyze Azure API schemas and validate whether the associated Azure resources support IP address access restrictions.

## Overview

This project reads Azure API JSON schemas and checks if the corresponding Azure products provide the capability to control IP address access to the resource.

## Features

- Parses Azure API schemas to identify IP address access control capabilities.
- Includes auxiliary scripts for:
    - Checking token size
    - Checking file size
    - Retrieving schema versions (PowerShell)

## Requirements

- Python 3.x
- Azure API schema files
- PowerShell (for auxiliary scripts)

## Usage

Run the main Python script:

```bash
python ARM-SCHEMA-CHECKER.py
```

## Auxiliary Scripts

- `CheckTokensize.py`: Validates token size.
- `CheckFileSize.ps1`: Checks schema file sizes.
- `CheckRPVersion.ps1`: Retrieves schema versions using PowerShell.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.