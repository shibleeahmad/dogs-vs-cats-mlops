# Contributing Guide

## Branching Strategy

The project uses three permanent branches:

- main - production/release
- staging - release candidate
- dev - integration

Short-lived branches:

- eat/<name>
- data/<name>
- exp/<member>-<idea>
- ix/<name>

## Commit Convention

We use Conventional Commits.

Examples:

- eat: add image preprocessing
- ix: correct data split
- data: add dataset version
- 	est: add preprocessing tests
- docs: update README

## Pull Requests

Changes to dev, staging, and main must go through pull requests.

At least one teammate must review each pull request.

## Merge Strategy

Pull requests into dev will use squash merging.
