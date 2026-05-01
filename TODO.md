# TODO: Striver A2Z DSA Sheet Integration

## Phase 1: Database Setup (SQLite)
- [x] 1.1 Create SQLite database schema for problems and user progress
- [x] 1.2 Define tables: problems, user_progress, problem_attempts
- [x] 1.3 Initialize database with Striver A2Z Sheet (~400 problems)

## Phase 2: Data & Backend
### 2.1 Add Striver A2Z Sheet Problems
- [ ] Create problems_data.py with Striver A2Z problems organized by topic/difficulty
- [ ] Add function to populate problems into SQLite database
- [ ] Define topics: Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, DP, Sorting, Searching, etc.

### 2.2 Create Database Helper Functions (CRUD)
- [ ] Add delete_problem(problem_id) - Delete a problem by ID
- [ ] Add delete_user_progress(user_id, problem_id) - Delete user progress for problem
- [ ] Add clear_user_progress(user_id) - Clear all progress for a user
- [ ] Add search_problems(query) - Search problems by name

### 2.3 Add API Endpoints for Problem Fetching
- [ ] GET /api/problems - List all problems (filters: topic, difficulty)
- [ ] GET /api/problems/{problem_id} - Get single problem details
- [ ] GET /api/topics - Get all topics with problem counts
- [ ] PUT /api/progress/{user_id} - Update user progress (mark solved/not solved)
- [ ] GET /api/progress/{user_id} - Get user progress with stats
- [ ] Integrate SQLite with backend instead of in-memory storage

## Phase 3: Streamlit UI Integration
- [ ] 3.1 Update app.py to load problems from SQLite
- [ ] 3.2 Connect Driver Sheet table with database
- [ ] 3.3 Add live progress display (solved count per topic)
- [ ] 3.4 Make UI reactive to data changes

## Phase 4: Progress Tracking
- [ ] 4.1 Track solved/unsolved status per problem per user
- [ ] 4.2 Show topic-wise progress statistics
- [ ] 4.3 Add functionality to mark problems as solved
