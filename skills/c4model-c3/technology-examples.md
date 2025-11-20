# Technology-Specific Examples

This guide provides technology-specific examples for component identification at the C3 level.

---

## Technology-Specific Examples

### NestJS Example

**Component identification in NestJS backend:**

```typescript
// src/users/user.controller.ts
@Controller('users')
export class UserController {           // Component: User Controller (controller)
  constructor(private userService: UserService) {}

  @Post()
  create(@Body() dto: CreateUserDto) {
    return this.userService.create(dto);
  }
}

// src/users/user.service.ts
@Injectable()
export class UserService {              // Component: User Service (service)
  constructor(private userRepo: UserRepository) {}

  async create(dto: CreateUserDto) {
    return this.userRepo.save(dto);
  }
}

// src/users/user.repository.ts
@Injectable()
export class UserRepository {           // Component: User Repository (repository)
  constructor(@InjectRepository(User) private repo: Repository<User>) {}

  async save(data: CreateUserDto) {
    return this.repo.save(data);
  }
}
```

**Components:**
1. **User Controller** (controller) - Handles HTTP requests
2. **User Service** (service) - Business logic
3. **User Repository** (repository) - Data access

**Patterns:**
- Dependency Injection (@Injectable, constructor injection)
- Repository Pattern (UserRepository)
- Layered Architecture (Controller → Service → Repository)

---

### Django Example (Python)

**Component identification in Django backend:**

```python
# users/views.py
class UserViewSet(viewsets.ModelViewSet):     # Component: User ViewSet (controller)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = UserService.create_user(serializer.validated_data)
            return Response(UserSerializer(user).data)

# users/services.py
class UserService:                            # Component: User Service (service)
    @staticmethod
    def create_user(data):
        # Business logic
        user = User.objects.create(**data)
        EmailService.send_welcome(user)
        return user

# users/models.py
class User(models.Model):                     # Component: User Model (model)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
```

**Components:**
1. **User ViewSet** (controller) - Handles HTTP requests
2. **User Service** (service) - Business logic
3. **User Model** (model) - Data model

---

### Spring Boot Example (Java)

**Component identification in Spring Boot backend:**

```java
// UserController.java
@RestController
@RequestMapping("/users")
public class UserController {                 // Component: User Controller (controller)
    @Autowired
    private UserService userService;

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody CreateUserDto dto) {
        User user = userService.createUser(dto);
        return ResponseEntity.ok(user);
    }
}

// UserService.java
@Service
public class UserService {                    // Component: User Service (service)
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;

    public User createUser(CreateUserDto dto) {
        User user = new User(dto);
        userRepository.save(user);
        emailService.sendWelcome(user);
        return user;
    }
}

// UserRepository.java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {  // Component: User Repository (repository)
    Optional<User> findByEmail(String email);
}
```

**Components:**
1. **User Controller** (controller) - HTTP request handling
2. **User Service** (service) - Business logic
3. **User Repository** (repository) - Data access

**Patterns:**
- Dependency Injection (@Autowired)
- Repository Pattern (Spring Data JPA)
- Layered Architecture

---

### React Example (Frontend)

**Component identification in React frontend:**

```typescript
// src/features/users/UserList.tsx
export function UserList() {                  // Component: User List (page/screen)
  const { users, loading } = useUsers();

  return (
    <div>
      {users.map(user => <UserCard key={user.id} user={user} />)}
    </div>
  );
}

// src/features/users/hooks/useUsers.ts
export function useUsers() {                  // Component: User Hook (state management)
  const [users, setUsers] = useState([]);

  useEffect(() => {
    UserService.fetchUsers().then(setUsers);
  }, []);

  return { users, loading };
}

// src/services/UserService.ts
export class UserService {                    // Component: User Service (service)
  static async fetchUsers() {
    const response = await api.get('/users');
    return response.data;
  }

  static async createUser(data: CreateUserDto) {
    const response = await api.post('/users', data);
    return response.data;
  }
}
```

**Components:**
1. **User List** (page) - UI component
2. **useUsers Hook** (state-management) - State management
3. **User Service** (service) - API client
