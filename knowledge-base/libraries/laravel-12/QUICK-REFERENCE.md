# Laravel 12 Quick Reference Guide

> Fast lookup for common Laravel patterns, methods, and concepts

---

## 🚀 Getting Started

### Installation
```bash
# Install Laravel
composer create-project laravel/laravel my-app

# Start development server
php artisan serve
```
📖 See: `installation.md`

### Project Structure
```
app/                # Application code
  Http/Controllers/ # HTTP controllers
  Models/           # Eloquent models
bootstrap/          # Framework bootstrap
config/            # Configuration files
database/          # Migrations, factories, seeders
public/            # Web server document root
resources/         # Views, assets
routes/            # Route definitions
storage/           # Generated files, logs, cache
tests/             # Test files
```
📖 See: `structure.md`

---

## 🔀 Routing

### Basic Routes
```php
use Illuminate\Support\Facades\Route;

// GET route
Route::get('/users', [UserController::class, 'index']);

// POST route
Route::post('/users', [UserController::class, 'store']);

// Multiple HTTP methods
Route::match(['get', 'post'], '/path', $callback);
Route::any('/path', $callback);

// Named routes
Route::get('/profile', ProfileController::class)->name('profile');

// Route groups with middleware
Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', DashboardController::class);
});
```
📖 See: `routing.md`, `middleware.md`

### Route Parameters
```php
Route::get('/users/{id}', function ($id) { });
Route::get('/posts/{post}/comments/{comment}', function ($post, $comment) { });
Route::get('/users/{name?}', function ($name = 'Guest') { });
```
📖 See: `routing.md`

---

## 🎮 Controllers

### Resource Controllers
```php
// Generate controller
php artisan make:controller PostController --resource

// Register resource routes
Route::resource('posts', PostController::class);

// Available methods: index, create, store, show, edit, update, destroy
```
📖 See: `controllers.md`

### Dependency Injection
```php
public function store(Request $request, PostRepository $posts) {
    // Automatic dependency resolution
}
```
📖 See: `controllers.md`, `container.md`

---

## 📝 Requests & Validation

### Accessing Input
```php
$request->input('name');
$request->input('name', 'default');
$request->all();
$request->only(['name', 'email']);
$request->except(['password']);
$request->has('name');
$request->filled('name');
```
📖 See: `requests.md`

### Validation
```php
$validated = $request->validate([
    'title' => 'required|max:255',
    'body' => 'required',
    'email' => 'required|email|unique:users',
    'age' => 'required|integer|min:18',
]);
```
📖 See: `validation.md`

### Form Requests
```php
php artisan make:request StorePostRequest

// In controller
public function store(StorePostRequest $request) {
    $validated = $request->validated();
}
```
📖 See: `validation.md`

---

## 🗄️ Database & Eloquent

### Query Builder
```php
use Illuminate\Support\Facades\DB;

DB::table('users')->get();
DB::table('users')->where('status', 'active')->get();
DB::table('users')->find(1);
DB::table('users')->insert(['name' => 'John']);
DB::table('users')->where('id', 1)->update(['name' => 'Jane']);
DB::table('users')->where('id', 1)->delete();
```
📖 See: `database.md`, `queries.md`

### Eloquent Models
```php
// Generate model
php artisan make:model Post -m  # with migration
php artisan make:model Post -mfc  # with migration, factory, controller

// CRUD Operations
$post = Post::create(['title' => 'Hello', 'body' => 'World']);
$post = Post::find(1);
$posts = Post::where('published', true)->get();
$post->update(['title' => 'Updated']);
$post->delete();

// Mass assignment protection
protected $fillable = ['title', 'body'];
protected $guarded = ['id', 'user_id'];
```
📖 See: `eloquent.md`

### Relationships
```php
// One to Many
public function posts() {
    return $this->hasMany(Post::class);
}
public function user() {
    return $this->belongsTo(User::class);
}

// Many to Many
public function roles() {
    return $this->belongsToMany(Role::class);
}

// Eager Loading
$users = User::with('posts')->get();
$users = User::with(['posts', 'comments'])->get();
```
📖 See: `eloquent-relationships.md`

### Migrations
```php
php artisan make:migration create_posts_table

// In migration
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('body');
    $table->foreignId('user_id')->constrained();
    $table->timestamps();
});

// Run migrations
php artisan migrate
php artisan migrate:rollback
php artisan migrate:fresh --seed
```
📖 See: `migrations.md`

---

## 🔐 Authentication & Authorization

### Authentication
```php
// Check if authenticated
if (Auth::check()) { }

// Get authenticated user
$user = Auth::user();
$id = Auth::id();

// Login/Logout
Auth::login($user);
Auth::logout();

// Attempt login
Auth::attempt(['email' => $email, 'password' => $password]);
```
📖 See: `authentication.md`

### Authorization (Gates & Policies)
```php
// Define gate
Gate::define('update-post', function (User $user, Post $post) {
    return $user->id === $post->user_id;
});

// Check authorization
if (Gate::allows('update-post', $post)) { }
Gate::authorize('update-post', $post);

// In controller
$this->authorize('update', $post);
```
📖 See: `authorization.md`

---

## 📮 Mail & Notifications

### Sending Mail
```php
// Generate mailable
php artisan make:mail OrderShipped

// Send mail
use Illuminate\Support\Facades\Mail;

Mail::to($user)->send(new OrderShipped($order));
Mail::to($user)->queue(new OrderShipped($order)); // Queue it
```
📖 See: `mail.md`

### Notifications
```php
// Generate notification
php artisan make:notification InvoicePaid

// Send notification
$user->notify(new InvoicePaid($invoice));

// Multiple channels
public function via($notifiable) {
    return ['mail', 'database', 'broadcast'];
}
```
📖 See: `notifications.md`

---

## ⚡ Queues & Jobs

### Creating Jobs
```php
// Generate job
php artisan make:job ProcessPodcast

// Dispatch job
ProcessPodcast::dispatch($podcast);
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(10));
ProcessPodcast::dispatch($podcast)->onQueue('high-priority');
```
📖 See: `queues.md`

### Running Queue Workers
```bash
php artisan queue:work
php artisan queue:work --queue=high,default
php artisan queue:listen
```
📖 See: `queues.md`, `horizon.md`

---

## 📡 Events & Broadcasting

### Events
```php
// Generate event
php artisan make:event OrderShipped

// Dispatch event
event(new OrderShipped($order));
OrderShipped::dispatch($order);
```
📖 See: `events.md`

### Broadcasting
```php
// Make event broadcastable
class OrderShipped implements ShouldBroadcast {
    public function broadcastOn() {
        return new Channel('orders');
    }
}

// Listen in JavaScript
Echo.channel('orders')
    .listen('OrderShipped', (e) => {
        console.log(e.order);
    });
```
📖 See: `broadcasting.md`, `reverb.md`

---

## 🎨 Views & Blade

### Returning Views
```php
return view('welcome');
return view('posts.index', ['posts' => $posts]);
return view('posts.show')->with('post', $post);
```
📖 See: `views.md`

### Blade Syntax
```blade
{{-- Comments --}}
{{ $variable }}  {{-- Escaped output --}}
{!! $html !!}   {{-- Unescaped output --}}

@if ($condition)
@elseif ($other)
@else
@endif

@foreach ($posts as $post)
    {{ $post->title }}
@endforeach

@forelse ($posts as $post)
    {{ $post->title }}
@empty
    <p>No posts found.</p>
@endforelse

@auth
    {{-- User is authenticated --}}
@endauth

@guest
    {{-- User is not authenticated --}}
@endguest

{{-- Layouts --}}
@extends('layouts.app')
@section('content')
    Content here
@endsection

{{-- Components --}}
<x-alert type="success" :message="$message" />
```
📖 See: `blade.md`

---

## 💾 Cache

### Cache Operations
```php
use Illuminate\Support\Facades\Cache;

Cache::put('key', 'value', $seconds);
Cache::forever('key', 'value');
Cache::get('key');
Cache::get('key', 'default');
Cache::remember('users', 3600, function () {
    return DB::table('users')->get();
});
Cache::forget('key');
Cache::flush();
```
📖 See: `cache.md`

---

## 🧪 Testing

### Feature Tests
```php
// Test HTTP requests
$response = $this->get('/');
$response = $this->post('/posts', $data);

$response->assertStatus(200);
$response->assertSee('Welcome');
$response->assertJson(['created' => true]);
$response->assertRedirect('/dashboard');
```
📖 See: `http-tests.md`

### Database Testing
```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class ExampleTest extends TestCase {
    use RefreshDatabase;

    public function test_example() {
        $user = User::factory()->create();

        $this->assertDatabaseHas('users', [
            'email' => $user->email,
        ]);
    }
}
```
📖 See: `database-testing.md`, `eloquent-factories.md`

---

## 🛠️ Artisan Commands

### Common Commands
```bash
# Application
php artisan serve
php artisan about

# Database
php artisan migrate
php artisan migrate:fresh --seed
php artisan db:seed

# Code Generation
php artisan make:model Post -mfc
php artisan make:controller PostController --resource
php artisan make:migration create_posts_table
php artisan make:seeder PostSeeder
php artisan make:factory PostFactory
php artisan make:request StorePostRequest
php artisan make:middleware CheckAge
php artisan make:command SendEmails

# Cache & Config
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
php artisan optimize

# Queue
php artisan queue:work
php artisan queue:restart
php artisan queue:failed

# Testing
php artisan test
php artisan test --filter=ExampleTest
```
📖 See: `artisan.md`

---

## 📚 Collections

### Common Methods
```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->all();
$collection->map(fn($item) => $item * 2);
$collection->filter(fn($item) => $item > 2);
$collection->first();
$collection->last();
$collection->pluck('name');
$collection->where('status', 'active');
$collection->sum();
$collection->count();
$collection->chunk(2);
$collection->groupBy('category');
$collection->sortBy('name');
```
📖 See: `collections.md`, `eloquent-collections.md`

---

## 🔧 Configuration

### Environment Variables
```env
APP_NAME=Laravel
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```
📖 See: `configuration.md`

### Accessing Config
```php
config('app.name');
config('database.default');
config('app.name', 'Default Name');
```
📖 See: `configuration.md`

---

## 🌐 API Development

### API Resources
```php
// Generate resource
php artisan make:resource PostResource

// Use resource
return new PostResource($post);
return PostResource::collection($posts);
```
📖 See: `eloquent-resources.md`

### API Authentication
```php
// Sanctum (simpler)
$token = $user->createToken('token-name')->plainTextToken;

// Passport (OAuth2)
php artisan passport:install
```
📖 See: `sanctum.md`, `passport.md`

### Rate Limiting
```php
Route::middleware('throttle:60,1')->group(function () {
    Route::get('/api/users', [UserController::class, 'index']);
});
```
📖 See: `rate-limiting.md`

---

## 📦 Common Packages

| Package | Purpose | Documentation |
|---------|---------|---------------|
| **Cashier** | Stripe subscription billing | `billing.md` |
| **Sanctum** | API token authentication | `sanctum.md` |
| **Passport** | OAuth2 server | `passport.md` |
| **Scout** | Full-text search | `scout.md` |
| **Horizon** | Queue monitoring | `horizon.md` |
| **Telescope** | Debugging assistant | `telescope.md` |
| **Socialite** | OAuth providers | `socialite.md` |
| **Dusk** | Browser testing | `dusk.md` |
| **Fortify** | Auth backend | `fortify.md` |
| **Pennant** | Feature flags | `pennant.md` |
| **Pulse** | Monitoring | `pulse.md` |

---

## 🚀 Performance

### Optimization Commands
```bash
# Cache everything
php artisan optimize
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Clear cache
php artisan optimize:clear

# Use Octane for performance
php artisan octane:start
```
📖 See: `deployment.md`, `octane.md`, `cache.md`

---

## 🐳 Development Environments

| Tool | Platform | Use Case | Docs |
|------|----------|----------|------|
| **Sail** | All | Docker dev environment | `sail.md` |
| **Valet** | macOS | Lightweight local dev | `valet.md` |
| **Homestead** | All | Full-featured Vagrant box | `homestead.md` |

---

## 🔗 Important Links

- **Official Docs**: https://laravel.com/docs
- **Laracasts**: https://laracasts.com (video tutorials)
- **Laravel News**: https://laravel-news.com
- **GitHub**: https://github.com/laravel/laravel

---

**Quick Reference Version**: 1.0.0
**Generated**: 2025-11-21
**For Laravel**: 12.x
