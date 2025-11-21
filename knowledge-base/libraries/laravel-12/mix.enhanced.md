---
title: Laravel Mix
library: laravel
version: '12'
category: frontend
tags:
- api
- home
- introduction
- knowledge-base
- laravel
- laravel-12
- libraries
- melly
- mixmd
- reference
- tutorial
- user
file_info:
  name: mix.md
  path: /home/user/melly/knowledge-base/libraries/laravel-12/mix.md
  size: 1478
structure:
  headings_count: 2
  code_blocks_count: 1
  internal_links_count: 2
processed_at: '2025-11-21T15:35:21.877069Z'
---

## Metadata

### Related Documentation

- [Vite migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md)

---

# Laravel Mix

- [Introduction](#introduction)

<a name="introduction"></a>
## Introduction

> [!WARNING]
> Laravel Mix is a legacy package that is no longer actively maintained. [Vite](/docs/{{version}}/vite) may be used as a modern alternative.

[Laravel Mix](https://github.com/laravel-mix/laravel-mix), a package developed by [Laracasts](https://laracasts.com) creator Jeffrey Way, provides a fluent API for defining [webpack](https://webpack.js.org) build steps for your Laravel application using several common CSS and JavaScript pre-processors.

In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all.

> [!NOTE]
> Vite has replaced Laravel Mix in new Laravel installations. For Mix documentation, please visit the [official Laravel Mix](https://laravel-mix.com/) website. If you would like to switch to Vite, please see our [Vite migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite).
