# 🔐 Authentication Guide

## Overview

The Multi-Agent Content Creator Assistant now includes a secure authentication system that allows multiple users to maintain their own separate workspaces and projects.

## Features

### ✅ User Management
- **Registration**: Create a new account with username, email, and password
- **Login**: Secure login with password hashing (SHA-256)
- **User Isolation**: Each user has their own separate workspace and session data

### 🗂️ Session Management
- **User-Specific Sessions**: All sessions are stored with username prefix
- **Session History**: View and load your previous projects from the sidebar
- **Data Persistence**: Your work is automatically saved and tied to your account

### 🔒 Security Features
- **Password Hashing**: Passwords are hashed using SHA-256 before storage
- **Secure File Storage**: User credentials stored in `users.json` (git-ignored)
- **Session Isolation**: Users can only access their own data
- **Automatic Logout**: Clear session data on logout

## Usage

### First Time Users

1. **Access the Application**
   ```bash
   streamlit run app.py
   ```

2. **Register a New Account**
   - Click on the "📝 Register" tab
   - Enter a unique username (minimum 3 characters)
   - Provide a valid email address
   - Choose a password (minimum 6 characters)
   - Confirm your password
   - Click "Register"

3. **Login**
   - Switch to "🔐 Login" tab
   - Enter your username and password
   - Click "Login"

### Returning Users

1. **Login to Your Account**
   - Enter your credentials on the login page
   - Click "Login"

2. **Access Your Projects**
   - Your previous projects appear in the sidebar under "📁 Your Recent Projects"
   - Click on any project to expand details
   - Click "Load Project" to continue where you left off

3. **Create New Projects**
   - Click "🔄 Start a New Project" to begin a fresh workflow
   - Your new project will be saved automatically

### Logout

- Click the "🚪 Logout" button in the sidebar
- This will clear your current session and return you to the login page

## File Structure

```
Multi-Agent-Content-Creator-Assistant/
├── users.json                    # User credentials (git-ignored)
├── session_data/
│   ├── username_sessionid.json  # User-specific session files
│   └── .gitkeep
├── utils/
│   ├── auth.py                  # Authentication module
│   └── helpers.py               # Updated with user-specific functions
└── app.py                       # Main app with auth integration
```

## Technical Details

### Password Security
- Passwords are hashed using SHA-256 cryptographic hash function
- Original passwords are never stored
- Hash comparison is used for authentication

### Session Data Format
Session files are named: `{username}_{session_id}.json`

Example:
```
john_doe_5c95c366-e3fe-45ce-8438-44adb6457a40.json
```

### User Data Structure
```json
{
  "username": {
    "password": "hashed_password_string",
    "email": "user@example.com",
    "created_at": "2025-11-13T10:30:00.000000",
    "last_login": "2025-11-13T15:45:00.000000"
  }
}
```

## Privacy & Data

### What is Stored?
- Username (plaintext)
- Email address (plaintext)
- Password hash (SHA-256)
- Session data (JSON files with your project data)
- Account creation and last login timestamps

### What is NOT Stored?
- Your actual password (only the hash)
- Any personal information beyond email
- Payment or billing information

### Data Deletion
To delete your account and all associated data:
1. Delete your entry from `users.json`
2. Delete all session files starting with your username from `session_data/`

## Troubleshooting

### "Username already exists"
- Choose a different username
- Each username must be unique

### "Email already registered"
- You may have already registered with this email
- Use a different email address

### "Invalid username or password"
- Check your credentials carefully
- Usernames and passwords are case-sensitive
- Make sure Caps Lock is not on

### Cannot See Previous Projects
- Make sure you're logged in with the correct username
- Previous projects are user-specific
- Check that session files exist in `session_data/` folder

### Lost Password
- Currently, password recovery is not implemented
- Contact the system administrator or manually reset in `users.json`

## Security Best Practices

### For Users
1. Use a strong password (combination of letters, numbers, symbols)
2. Don't share your credentials
3. Logout when finished, especially on shared computers
4. Use a unique password (don't reuse from other sites)

### For Administrators
1. Keep `users.json` secure and backed up
2. Never commit `users.json` to version control
3. Regularly audit user accounts
4. Consider implementing password complexity requirements
5. Add rate limiting for login attempts in production

## Future Enhancements

Planned features for future versions:
- [ ] Password recovery via email
- [ ] Two-factor authentication (2FA)
- [ ] Password strength requirements
- [ ] Account deletion from UI
- [ ] User profile management
- [ ] Session expiration
- [ ] Activity logs
- [ ] Admin panel for user management
- [ ] OAuth integration (Google, GitHub, etc.)
- [ ] Database backend (SQLite/PostgreSQL)

## Migration from Non-Authenticated Version

If you were using the app before authentication was added:

1. **Register a New Account**
   - Your old session files are still in `session_data/`
   - They're named without username prefix

2. **Rename Old Sessions** (optional)
   ```bash
   cd session_data
   # Rename your old sessions to include your username
   mv old_session_id.json your_username_old_session_id.json
   ```

3. **Continue Working**
   - Old sessions won't automatically appear in sidebar
   - You can manually rename files or start fresh

## Support

For issues or questions:
1. Check this documentation
2. Review error messages in the UI
3. Check application logs in `app_debug.log`
4. Contact the development team

---

**Note**: This authentication system is designed for development and small-scale deployment. For production use with many users, consider upgrading to a database-backed solution with additional security features.
