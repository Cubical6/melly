---
library:
  name: Laravel
  version: 11.x
  url: https://laravel.com/docs/11.x/routing#route-model-binding
  language: PHP
  type: framework
file:
  path: knowledge-base/libraries/laravel-11/routing/route-model-binding.md
  category: Routing
  topic: Advanced Routing
  concepts:
    - Implicit Binding
    - Explicit Binding
    - Custom Keys
metadata:
  word_count: 1650
  code_blocks: 10
  headings: 7
  external_links: 2
  internal_references: 4
analyzed_at: 2025-11-16T12:05:00Z
basic_memory_id: entity-def456
---

## Metadata

### Observations

#### Concept: Route Model Binding
**Category**: routing
**Source**: ## Introduction
**Confidence**: high

Route model binding automatically injects model instances based on route parameters, eliminating manual database queries in controllers.

**Keywords**: route-model-binding, automatic-injection, eloquent

---

#### Technique: Implicit Binding Convention
**Category**: routing
**Source**: ## Implicit Binding
**Confidence**: high

Implicit binding works when the route parameter name matches the type-hinted parameter in the controller method. Laravel automatically resolves the model instance.

**Keywords**: implicit-binding, type-hinting, convention

---

#### Example: Basic Implicit Binding
**Category**: routing
**Source**: ## Implicit Binding Example
**Confidence**: high

```php
Route::get('/users/{user}', function (User $user) {
    return $user;
});
```

This automatically finds the User model by ID from the {user} parameter.

**Keywords**: example, implicit-binding, user-model

---

#### Technique: Custom 404 Behavior
**Category**: routing
**Source**: ## Customizing Missing Model Behavior
**Confidence**: high

Use the `->missing()` method on route definitions to customize the behavior when a model is not found, instead of the default 404 error.

```php
Route::get('/users/{user}', function (User $user) {
    return $user;
})->missing(function () {
    return response('User not found', 404);
});
```

**Keywords**: missing, 404, error-handling

---

#### Technique: Custom Route Keys
**Category**: routing
**Source**: ## Customizing The Key
**Confidence**: high

Override the `getRouteKeyName()` method in your model to use a different column for route model binding (e.g., slug instead of id).

```php
public function getRouteKeyName()
{
    return 'slug';
}
```

**Keywords**: custom-keys, slug, route-key-name

---

#### Best Practice: Scoped Bindings
**Category**: routing
**Source**: ## Scoped Bindings
**Confidence**: high

Use scoped bindings to ensure child models belong to parent models in nested routes.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

**Keywords**: scoped-bindings, nested-routes, relationships

---

### Relations

#### Extends: laravel-routing-basics
**Type**: extends
**Source**: implicit
**Confidence**: high

Route model binding builds on basic routing concepts and extends them with automatic model injection capabilities.

---

#### Requires: laravel-eloquent-models
**Type**: requires
**Source**: ## Model Requirements
**Confidence**: high

Model binding requires Eloquent models to be defined. The route parameter type-hint must reference a valid Eloquent model class.

---

#### Alternative To: laravel-route-parameters
**Type**: alternative_to
**Source**: ## Benefits
**Confidence**: medium

Model binding provides a more elegant alternative to manually retrieving models from route parameters:

**Traditional approach**:
```php
Route::get('/users/{id}', function ($id) {
    $user = User::findOrFail($id);
    return $user;
});
```

**Model binding**:
```php
Route::get('/users/{user}', function (User $user) {
    return $user;
});
```

---

#### Uses: laravel-service-container
**Type**: uses
**Source**: ## How It Works
**Confidence**: high

Route model binding leverages Laravel's service container for dependency injection and model resolution.

---

---

# Route Model Binding

## Introduction

Route model binding provides a convenient way to automatically inject model instances into your routes. For example, instead of injecting a user's ID, you can inject the entire `User` model instance that matches the given ID.

## Implicit Binding

Laravel automatically resolves Eloquent models defined in routes or controller actions whose type-hinted variable names match a route segment name.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

Since the `$user` variable is type-hinted as the `App\Models\User` Eloquent model and the variable name matches the `{user}` URI segment, Laravel will automatically inject the model instance that has an ID matching the corresponding value from the request URI.

If a matching model instance is not found in the database, a 404 HTTP response will automatically be generated.

### Customizing The Key

Sometimes you may wish to resolve Eloquent models using a column other than `id`. To do so, you may specify the column in the route parameter definition:

```php
Route::get('/users/{user:slug}', function (User $user) {
    return $user;
});
```

If you would like model binding to always use a database column other than `id` when retrieving a given model class, you may override the `getRouteKeyName` method on the Eloquent model:

```php
/**
 * Get the route key for the model.
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

### Customizing Missing Model Behavior

Typically, a 404 HTTP response will be generated if an implicitly bound model is not found. However, you may customize this behavior by calling the `missing` method when defining your route:

```php
use App\Http\Controllers\LocationsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
    ->name('locations.view')
    ->missing(function (Request $request) {
        return Redirect::route('locations.index');
    });
```

## Explicit Binding

You are not required to use Laravel's implicit, convention based model resolution in order to use model binding. You can also explicitly define how route parameters correspond to models.

To register an explicit binding, use the router's `model` method to specify the class for a given parameter. You should define your explicit model bindings at the beginning of the `boot` method of your `AppServiceProvider` class:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

Next, define a route that contains a `{user}` parameter:

```php
Route::get('/users/{user}', function (User $user) {
    // ...
});
```

Since we have bound all `{user}` parameters to the `App\Models\User` model, an instance of that class will be injected into the route.

## Scoped Bindings

Sometimes, when implicitly binding multiple Eloquent models in a single route definition, you may wish to scope the second Eloquent model such that it must be a child of the previous Eloquent model.

For example, consider this route definition that retrieves a blog post by slug for a specific user:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `User` model has a relationship named `posts` (the plural form of the route parameter name) which can be used to retrieve the `Post` model.

If you wish, you may instruct Laravel to scope "child" bindings even when a custom key is not provided. To do so, you may invoke the `scopeBindings` method when defining your route:

```php
Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

Or, you may instruct an entire group of route definitions to use scoped bindings:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

## Customizing The Resolution Logic

If you would like to use your own custom model binding resolution logic, you may use the `Route::bind` method. The closure you pass to the `bind` method will receive the value of the URI segment and should return the instance of the class that should be injected into the route:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```
