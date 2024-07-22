# FastAPI CRUD API with User Management and Auto-Reply Functionality

This project is a FastAPI application that provides CRUD operations for users, posts, and comments, along with auto-reply functionality and basic content moderation.

## Features

### User Management
- **User Creation:** Register new users with username, email, password, auto-reply, and reply delay.
- **User Login:** Authenticate users and issue JWT tokens.
- **User Update:** Modify user details such as username, email, password, auto-reply, and reply delay.

### Comment Management
- **Create Comments:** Add comments to posts with optional parent comment references.
- **Retrieve Comments:** Fetch comments by post or user, and get replies for specific comments.
- **Delete Comments:** Remove comments (only by the owner).

### Post Management
- **Create Posts:** Add new posts.
- **Retrieve Posts:** View posts by ID or user.
- **Update and Delete Posts:** Modify or remove posts (only by the owner).

### Auto-Reply
- **Auto-Reply Feature:** Enable auto-reply for users with a specified delay for automatic responses to comments on their posts.
- **AI-Powered Replies:** Automatically generate replies if auto-reply is enabled for the post owner.

### Moderation
- **Content Moderation:** Posts and comments are checked for inappropriate content using the `better-profanity` library.

## Running the Application

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/paashkovaaa/social_media_fastapi_project.git
    cd social_media_fastapi_project
    ```

2. **Set Up a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the Database:**
    - Edit `database.py` to set up your database connection details.

5. **Create a `.env` File:**
    - Generate a `SECRET_KEY` for JWT:
      ```bash
      openssl rand -hex 32
      ```
    - Create your `GOOGLE_AI_API_KEY` and add it to the `.env` file. Example `.env` entries:
      ```
      SECRET_KEY=your_generated_secret_key
      GOOGLE_AI_API_KEY=your_google_ai_api_key
      ```

6. **Run the Application:**
    ```bash
    uvicorn main:app --reload
    ```
    The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

### User Management
- **`POST /users/`**: Create a new user.
- **`POST /users/token`**: Login and obtain a JWT access token.
- **`GET /users/me`**: Retrieve the current user's information.
- **`PUT /users/me`**: Update the current user's information.

### Comment Management
- **`POST /comments/`**: Add a new comment to a post.
- **`GET /comments/{comment_id}`**: Retrieve a specific comment.
- **`GET /comments/user/{user_id}`**: Get comments made by a user.
- **`GET /comments/post/{post_id}`**: Get comments on a specific post.
- **`GET /comments/replies/{comment_id}`**: Get replies to a specific comment.
- **`DELETE /comments/{comment_id}`**: Delete a comment (owner only).
-**`GET /comments/analytics/comments-daily-breakdown`**: Retrieve daily analytics for comments within a specified date range. The response includes:
  - **`date`**: The specific date for the analytics data.
  - **`created_comments`**: Number of comments created on that date.
  - **`blocked_comments`**: Number of comments blocked on that date.

### Post Management
- **`POST /posts/`**: Create a new post.
- **`GET /posts/`**: Retrieve all posts.
- **`GET /posts/{post_id}`**: Get details of a specific post.
- **`GET /posts/user/{user_id}`**: Get posts by a specific user.
- **`PUT /posts/{post_id}`**: Update a post (owner only).
- **`DELETE /posts/{post_id}`**: Delete a post (owner only).

## Testing

To run tests:

1. **Navigate to the Tests Directory:**
    ```bash
    cd tests
    ```

2. **Run Tests with pytest:**
    ```bash
    pytest
    ```

---

Feel free to contribute, report issues, or suggest improvements!
