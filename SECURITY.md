# Security Policy

## Supported versions

CMDforge currently supports the latest release published from the `main` branch and the most recent tagged version in GitHub.

## Reporting a vulnerability

If you believe you have found a security issue in CMDforge:

1. Do not open a public issue with exploit details.
2. Use GitHub Security Advisories or another private GitHub contact path available in the repository.
3. Include a clear description, affected versions, reproduction steps, and any suggested mitigations.

You can expect an initial acknowledgement as soon as practical, followed by triage and a coordinated fix when the report is confirmed.

## Scope

This project is a local CLI tool and scaffold generator.
Relevant issues include:

- unsafe filesystem behavior
- improper handling of destructive commands
- packaging or supply-chain concerns
- code execution or template injection risks in generated scaffolds

## Disclosure

Please allow time for triage and a fix before publicly disclosing a vulnerability.
