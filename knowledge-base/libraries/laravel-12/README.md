# Laravel 12 Framework Documentation

**Source**: https://github.com/laravel/docs (12.x branch)
**Downloaded**: 2025-11-15
**Total Files**: 100 markdown files

## Description

Complete Laravel 12 framework documentation in markdown format. This collection includes all official Laravel documentation covering:

- Getting Started
- Architecture Concepts
- The Basics
- Digging Deeper
- Security
- Database
- Eloquent ORM
- Testing
- Packages
- And more...

## Contents

This directory contains 100 markdown documentation files from the official Laravel framework documentation repository. Each file covers a specific aspect of the Laravel framework.

## Usage

These documentation files can be used:
- As reference material for Laravel development
- For contextual knowledge retrieval by Claude Code agents
- As training data for understanding Laravel patterns and best practices
- For generating Laravel-specific documentation and code

## Key Documentation Files

- `installation.md` - Getting started with Laravel
- `routing.md` - HTTP routing
- `middleware.md` - HTTP middleware
- `controllers.md` - Controllers
- `requests.md` - HTTP requests
- `responses.md` - HTTP responses
- `views.md` - Views
- `blade.md` - Blade templating
- `eloquent.md` - Eloquent ORM
- `migrations.md` - Database migrations
- `seeding.md` - Database seeding
- `validation.md` - Validation
- `authentication.md` - Authentication
- `authorization.md` - Authorization
- `testing.md` - Testing
- And 85+ more specialized topics

## Maintenance

To update this documentation to the latest version:

```bash
# Remove old files
rm -rf knowledge-base/libraries/laravel-12/*.md

# Clone latest 12.x branch
cd /tmp
git clone --depth 1 --branch 12.x https://github.com/laravel/docs.git laravel-docs-12

# Copy new files
cp /tmp/laravel-docs-12/*.md /path/to/melly/knowledge-base/libraries/laravel-12/

# Clean up
rm -rf /tmp/laravel-docs-12
```

## License

Laravel documentation is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
