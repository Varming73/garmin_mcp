# Garmin MCP Server - LibreChat Integration Guide

Complete guide for integrating the Garmin MCP Server with LibreChat for the best user experience.

---

## Overview

Based on the actual code implementation, this Garmin MCP server is a **stdio-based MCP server** that provides:
- **76 tools** for comprehensive Garmin Connect data access
- **2 MCP resources** for direct data streaming
- **4 MCP prompts** for common analysis patterns
- **69 refactored tools** with full validation and error handling (v0.2.0)

---

## LibreChat Configuration

### Recommended Configuration (Best UX)

Add this to your `librechat.yaml` under the `mcpServers` section:

```yaml
mcpServers:
  garmin:
    type: stdio
    command: uvx
    args:
      - --from
      - git+https://github.com/Varming73/garmin_mcp
      - garmin-mcp
    env:
      GARMIN_EMAIL: "${GARMIN_EMAIL}"
      GARMIN_PASSWORD: "${GARMIN_PASSWORD}"
      LOG_LEVEL: "INFO"
    timeout: 60000          # 60 seconds for long-running API calls
    initTimeout: 30000      # 30 seconds for server initialization & Garmin login
    stderr: "inherit"       # Show detailed error messages
    iconPath: "/path/to/garmin-icon.svg"  # Optional: Custom Garmin icon
    serverInstructions: |
      Garmin Connect MCP Server - Access to comprehensive fitness and health data:

      **Best Practices:**
      1. Use date format YYYY-MM-DD for all date parameters
      2. Check today's health summary resource (garmin://health/today) before querying specific metrics
      3. Use list_activities tool first to get activity IDs before requesting detailed data
      4. For date ranges, verify end_date is after start_date
      5. Activity analysis prompts (analyze_weekly_activity, sleep_quality_analysis) provide structured insights

      **Data Categories:**
      - Activities: 17 tools for activity management and analysis
      - Health & Wellness: 22 tools for steps, sleep, heart rate, stress, body battery, etc.
      - Training: 8 tools for training status, VO2 max, HRV, readiness
      - Body Metrics: 8 tools for weight, body composition, blood pressure
      - Devices & Gear: 9 tools for device and equipment management
      - Challenges: 9 tools for badges, goals, and virtual races
      - Women's Health: 3 tools for menstrual and pregnancy tracking

      **MCP Resources (Direct Access):**
      - garmin://health/today - Today's health metrics summary
      - garmin://activities/recent - Last 10 activities

      **Common Patterns:**
      - For recent data: Use resources first, then tools for details
      - For historical analysis: Use date ranges with appropriate tools
      - For trends: Query multiple days and analyze progression
      - For specific metrics: Use dedicated tools (e.g., get_sleep_data for sleep)
```

---

## Configuration Options Explained

### Required Settings

#### `type: stdio`
- **Why**: The Garmin MCP server uses FastMCP with stdio transport (not SSE or WebSocket)
- **Implementation**: Calls `app.run()` which starts stdio server

#### `command: uvx`
- **Why**: Uses `uvx` (uv's tool runner) for isolated Python environment
- **Benefit**: No system-wide Python package installation needed
- **Alternative**: Use `npx` if you prefer npm-based tooling

#### `args`
```yaml
args:
  - --from
  - git+https://github.com/Varming73/garmin_mcp
  - garmin-mcp
```
- **Why**: Installs directly from your GitHub fork
- **Entry Point**: `garmin-mcp` (defined in pyproject.toml)
- **Alternative**: Use local path for development: `uv run --directory /path/to/garmin_mcp garmin-mcp`

#### `env.GARMIN_EMAIL` & `env.GARMIN_PASSWORD`
- **Required**: Server will not start without these credentials
- **Implementation**: Read by `get_credentials()` function in `__init__.py`
- **Security**: Use LibreChat environment variable substitution with `${ENV_VAR}` syntax

---

### Optional Settings (Recommended)

#### `env.LOG_LEVEL`
```yaml
env:
  LOG_LEVEL: "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```
- **Purpose**: Controls server logging verbosity
- **Default**: INFO (if not specified)
- **Production**: Use INFO or WARNING
- **Debugging**: Use DEBUG to see all API calls and validation

#### `env.LOG_FILE`
```yaml
env:
  LOG_FILE: "/var/log/garmin-mcp/server.log"  # Optional log file path
```
- **Purpose**: Write logs to file instead of stderr
- **Default**: Logs to stderr if not specified
- **Use Case**: Persistent logging for debugging

#### `timeout: 60000`
- **Why**: Garmin Connect API calls can be slow (especially for historical data)
- **Default**: 30000ms (30s) if not specified
- **Recommendation**: 60000ms (60s) for reliability
- **Implementation**: LibreChat waits this long for tool responses

#### `initTimeout: 30000`
- **Why**: Server initialization includes:
  1. Python environment setup
  2. Package installation (first run)
  3. Garmin Connect authentication
  4. Token storage/retrieval
- **Default**: 10000ms (10s) if not specified
- **Recommendation**: 30000ms (30s) minimum
- **First Run**: May need 60000ms (60s) for package downloads

#### `stderr: "inherit"`
- **Why**: Shows error messages in LibreChat logs for debugging
- **Default**: "inherit"
- **Alternatives**:
  - `"ignore"` - Suppress all stderr
  - `"pipe"` - Capture stderr programmatically

#### `serverInstructions`
- **Why**: Provides AI assistant with context about Garmin data capabilities
- **Options**:
  - `true` - Use server-provided instructions (if implemented)
  - `false` - No instructions (saves tokens)
  - `string` - Custom instructions (see example above)
- **Recommendation**: Use custom string for best UX (as shown above)

---

## Environment Variables Setup

### Option 1: LibreChat .env File (Recommended)

Add to your LibreChat `.env` file:

```bash
# Garmin Connect Credentials
GARMIN_EMAIL=your.email@example.com
GARMIN_PASSWORD=your_secure_password

# Optional: Token storage (for persistent sessions)
GARMINTOKENS=/var/lib/garmin-mcp/tokens
```

Then reference in `librechat.yaml`:
```yaml
env:
  GARMIN_EMAIL: "${GARMIN_EMAIL}"
  GARMIN_PASSWORD: "${GARMIN_PASSWORD}"
  GARMINTOKENS: "${GARMINTOKENS}"
```

**Benefits**:
- Centralized credential management
- Environment variable substitution by LibreChat
- Easy to update credentials

---

### Option 2: File-Based Secrets (Docker/Kubernetes)

For containerized deployments, use file-based secrets:

**Mount secret files**:
```bash
/run/secrets/garmin_email
/run/secrets/garmin_password
```

**LibreChat configuration**:
```yaml
mcpServers:
  garmin:
    type: stdio
    command: uvx
    args: [--from, "git+https://github.com/Varming73/garmin_mcp", garmin-mcp]
    env:
      GARMIN_EMAIL_FILE: "/run/secrets/garmin_email"
      GARMIN_PASSWORD_FILE: "/run/secrets/garmin_password"
```

**Benefits**:
- Secure secret management
- Works with Docker secrets, Kubernetes secrets, etc.
- No plain-text credentials in config files

**Implementation Note**: The server code supports this (see `get_credentials()` in `__init__.py`):
- `GARMIN_EMAIL_FILE` instead of `GARMIN_EMAIL`
- `GARMIN_PASSWORD_FILE` instead of `GARMIN_PASSWORD`
- Cannot use both (server will raise ConfigurationError)

---

### Option 3: Per-User Credentials (Multi-Tenant)

For multi-user LibreChat deployments where each user has their own Garmin account:

```yaml
mcpServers:
  garmin:
    type: stdio
    command: uvx
    args: [--from, "git+https://github.com/Varming73/garmin_mcp", garmin-mcp]
    customUserVars:
      GARMIN_EMAIL:
        title: "Garmin Connect Email"
        description: "Your Garmin Connect account email address"
      GARMIN_PASSWORD:
        title: "Garmin Connect Password"
        description: "Your Garmin Connect password (stored securely)"
    env:
      GARMIN_EMAIL: "{{GARMIN_EMAIL}}"
      GARMIN_PASSWORD: "{{GARMIN_PASSWORD}}"
      # Use user ID for separate token storage per user
      GARMINTOKENS: "/var/lib/garmin-mcp/tokens/{{LIBRECHAT_USER_ID}}"
    startup: false  # Don't start at app startup (requires user config)
```

**Benefits**:
- Each user provides their own Garmin credentials
- Credentials stored securely per user by LibreChat
- Token storage isolated per user (prevents conflicts)
- Users configure via UI (Settings > MCP Settings)

**Important**: Set `startup: false` since server requires user credentials before starting.

---

## Token Storage & Sessions

### How Token Storage Works

The Garmin MCP server implements OAuth token caching to avoid repeated logins:

1. **First Login**:
   - Uses email/password to authenticate
   - Garmin returns OAuth1 and OAuth2 tokens
   - Tokens saved to `GARMINTOKENS` directory (default: `~/.garminconnect`)
   - Also saved as base64 to `GARMINTOKENS_BASE64` (default: `~/.garminconnect_base64`)

2. **Subsequent Connections**:
   - Server attempts to login using stored tokens
   - If tokens valid → instant authentication (no credentials needed)
   - If tokens expired → fresh login with email/password

3. **Token Lifetime**:
   - Tokens typically valid for several days/weeks
   - Automatic refresh on server startup
   - Graceful fallback to credential-based login

### Multi-User Token Storage

**Problem**: Multiple LibreChat users sharing same token directory causes conflicts.

**Solution**: Use user-specific token directories:

```yaml
env:
  GARMINTOKENS: "/var/lib/garmin-mcp/tokens/{{LIBRECHAT_USER_ID}}"
  GARMINTOKENS_BASE64: "/var/lib/garmin-mcp/tokens/{{LIBRECHAT_USER_ID}}_base64"
```

**Why This Works**:
- `{{LIBRECHAT_USER_ID}}` replaced with unique user ID by LibreChat
- Each user gets isolated token storage
- No cross-user token conflicts
- Sessions persist across LibreChat restarts

---

## MCP Resources (Direct Data Access)

The server exposes 2 MCP resources for efficient data access:

### Resource 1: `garmin://health/today`

**Purpose**: Quick access to today's health summary

**Data Provided**:
- Total steps
- Total distance (meters)
- Active calories
- Floors climbed

**Usage in LibreChat**:
- Resource appears in assistant context automatically
- No explicit tool call needed
- Updates dynamically throughout the day

**Example Assistant Behavior**:
```
User: "How am I doing today?"
Assistant: [Reads garmin://health/today resource]
"You've walked 8,432 steps so far today, covering 6.2 km and burning
450 active calories. You've also climbed 12 floors. Great progress!"
```

---

### Resource 2: `garmin://activities/recent`

**Purpose**: Last 10 activities for quick reference

**Data Provided**:
- Full activity details for 10 most recent activities
- Activity names, types, dates, durations, etc.

**Usage in LibreChat**:
- Assistant can reference recent activities without tool calls
- Reduces API calls for common queries
- Provides context for activity-related questions

**Example Assistant Behavior**:
```
User: "What was my last run like?"
Assistant: [Reads garmin://activities/recent resource]
"Your last run was yesterday at 6:30 AM - a 5K run in 28:34 with
an average pace of 5:43 /km and average heart rate of 162 bpm."
```

---

## MCP Prompts (Analysis Templates)

The server provides 4 pre-defined prompt templates for common analyses:

### 1. `analyze_weekly_activity`
**Use Case**: Weekly activity summary and trends

**What It Does**:
1. Gets activities from last 7 days
2. Summarizes:
   - Total activities
   - Activity types distribution
   - Total distance
   - Average heart rate
   - Most active day
3. Provides insights and recommendations

**How to Use in LibreChat**:
- Users can say: "Analyze my weekly activity"
- Assistant invokes this prompt template automatically

---

### 2. `sleep_quality_analysis`
**Use Case**: Sleep quality assessment

**What It Does**:
1. Gets sleep data for last 7 days
2. Calculates:
   - Average sleep duration
   - Average sleep score
   - Sleep consistency (bedtime variation)
   - Deep sleep percentage
3. Identifies patterns and recommendations

**How to Use in LibreChat**:
- Users can say: "Analyze my sleep quality"
- Assistant follows structured analysis template

---

### 3. `training_readiness_check`
**Use Case**: Should I train today?

**What It Does**:
1. Gets today's training readiness score
2. Gets body battery data
3. Gets recent activity load
4. Gets last night's sleep quality
5. Provides comprehensive assessment:
   - Do intense workout
   - Do moderate workout
   - Focus on recovery

**How to Use in LibreChat**:
- Users can say: "Am I ready to train today?"
- Assistant evaluates multiple factors systematically

---

### 4. `monthly_fitness_report`
**Use Case**: Comprehensive monthly progress report

**What It Does**:
1. Gets activities for last 30 days
2. Gets health metrics for the month
3. Calculates trends:
   - Activity frequency and types
   - Distance/duration trends
   - Health metric improvements
   - Consistency patterns
4. Provides detailed summary
5. Sets goals for next month

**How to Use in LibreChat**:
- Users can say: "Generate my monthly fitness report"
- Assistant creates comprehensive analysis

---

## Available Tools by Category

### 🏃 Activity Management (17 tools)
- `list_activities` - List recent activities
- `get_activity_by_id` - Get detailed activity data
- `get_activity_summary` - Activity summary with stats
- `get_activity_splits` - Lap/split data
- `get_activity_weather` - Weather conditions during activity
- `get_activity_hr_zones` - Heart rate zone analysis
- `get_activity_details` - Comprehensive activity details
- `get_activity_gear` - Gear used in activity
- `get_activity_evaluation` - Performance evaluation
- `download_activity` - Download activity file (GPX/TCX/FIT)
- And more...

### ❤️ Health & Wellness (22 tools)
- `get_stats` - Daily activity stats
- `get_steps_data` - Steps data for a day
- `get_sleep_data` - Sleep analysis
- `get_heart_rates` - Heart rate data
- `get_stress_data` - Stress levels
- `get_body_battery` - Body battery levels
- `get_hydration_data` - Hydration tracking
- `get_respiration_data` - Respiration rate
- `get_spo2_data` - Blood oxygen levels
- And more...

### 🎯 Training & Performance (8 tools)
- `get_training_status` - Current training status
- `get_training_readiness` - Training readiness score
- `get_hrv_data` - Heart rate variability
- `get_max_metrics` - VO2 max and fitness age
- `get_training_effect` - Training effect for activity
- `get_hill_score` - Hill climbing performance
- `get_endurance_score` - Endurance performance
- And more...

### 📊 Body Metrics (8 tools)
- `get_weigh_ins` - Weight measurements
- `add_weigh_in` - Log new weight
- `get_body_composition` - Body composition data
- `add_body_composition` - Log body composition
- `get_blood_pressure` - Blood pressure readings
- `set_blood_pressure` - Log blood pressure
- `add_hydration_data` - Log water intake
- And more...

### ⌚ Devices & Gear (9 tools)
- `get_devices` - List all devices
- `get_device_settings` - Device configuration
- `get_device_last_used` - Last used device
- `get_device_solar_data` - Solar charging data
- `get_gear` - List gear/equipment
- `get_gear_stats` - Equipment usage stats
- And more...

### 🏆 Challenges & Goals (9 tools)
- `get_goals` - Active/future/past goals
- `get_earned_badges` - Earned badges
- `get_personal_record` - Personal records
- `get_adhoc_challenges` - Ad-hoc challenges
- `get_badge_challenges` - Badge challenges
- `get_race_predictions` - Race time predictions
- And more...

### 👩 Women's Health (3 tools)
- `get_pregnancy_summary` - Pregnancy tracking
- `get_menstrual_data_for_date` - Menstrual cycle data
- `get_menstrual_calendar_data` - Cycle calendar

---

## Advanced Configuration

### Custom Icon

Provide a custom Garmin icon for better UX:

```yaml
iconPath: "/path/to/garmin-icon.svg"
```

**Icon Requirements**:
- Format: SVG (preferred) or PNG
- Size: 24x24 to 48x48 pixels
- Style: Simple, recognizable Garmin logo
- Location: Accessible to LibreChat server

**Where It Appears**:
- Tool selection dialog
- MCP server list
- Chat interface (when tools are active)

---

### Exclude from Chat Menu

If you want Garmin tools available but not in quick-access dropdown:

```yaml
chatMenu: false
```

**When to Use**:
- You have many MCP servers
- Garmin tools used less frequently
- Want cleaner UI

**Note**: Tools still available through assistant selection.

---

### Logging Configuration

For debugging or monitoring:

```yaml
env:
  LOG_LEVEL: "DEBUG"
  LOG_FILE: "/var/log/garmin-mcp/debug.log"
```

**Log Levels**:
- `DEBUG` - All API calls, validation, detailed execution flow
- `INFO` - Normal operations, tool calls, authentication
- `WARNING` - Validation errors, retryable issues
- `ERROR` - Failed operations, authentication failures
- `CRITICAL` - Server crashes, fatal errors

**Log Output**:
- Without `LOG_FILE`: Logs to stderr (visible in LibreChat logs)
- With `LOG_FILE`: Logs to specified file
- Both: Use `stderr: "inherit"` + `LOG_FILE`

---

## Troubleshooting

### Server Won't Start

**Symptom**: MCP server fails to initialize

**Common Causes**:
1. **Missing Credentials**
   - Check: GARMIN_EMAIL and GARMIN_PASSWORD set?
   - Fix: Add to LibreChat .env file

2. **Authentication Failure**
   - Check: Are credentials correct?
   - Check: Does account require 2FA/MFA?
   - Fix: MFA currently requires manual input (not supported in LibreChat)

3. **Timeout During Init**
   - Check: `initTimeout` setting
   - Fix: Increase to 60000ms (60s) for first run

4. **Package Installation Fails**
   - Check: Internet connectivity
   - Check: `uvx` available in PATH
   - Fix: Pre-install packages or use local installation

---

### Slow Tool Responses

**Symptom**: Tools timeout or take too long

**Common Causes**:
1. **Garmin API Slow**
   - Fix: Increase `timeout` to 60000ms or higher

2. **Large Date Ranges**
   - Example: Querying 365 days of data
   - Fix: Use smaller date ranges, paginate requests

3. **Network Issues**
   - Fix: Check internet connection, Garmin Connect status

---

### Token Storage Issues

**Symptom**: Server re-authenticates every time

**Common Causes**:
1. **Token Directory Not Persistent**
   - Check: Is token directory writable?
   - Check: Does directory persist across container restarts?
   - Fix: Mount persistent volume for token storage

2. **Multi-User Conflicts**
   - Check: Are multiple users sharing token directory?
   - Fix: Use user-specific paths: `GARMINTOKENS: "/path/{{LIBRECHAT_USER_ID}}"`

3. **File Permissions**
   - Check: Can server write to token directory?
   - Fix: Ensure directory has correct permissions (chmod 700)

---

### MFA/2FA Required

**Symptom**: Authentication fails with MFA prompt

**Current Limitation**: The server's MFA prompt (`get_mfa()` in `__init__.py`) requires interactive input via stdin, which is not compatible with LibreChat's stdio-based MCP communication.

**Temporary Workarounds**:
1. **Disable 2FA** on Garmin account (if acceptable for your use case)
2. **Pre-authenticate** manually:
   ```bash
   # Run server manually once to authenticate
   GARMIN_EMAIL=your@email.com GARMIN_PASSWORD=yourpass uvx --from git+https://github.com/Varming73/garmin_mcp garmin-mcp
   # Enter MFA code when prompted
   # Tokens saved to ~/.garminconnect
   # Ctrl+C to stop

   # Then configure LibreChat to use saved tokens
   ```
3. **Use OAuth tokens** directly (if you have them from another method)

**Future Enhancement**: This could be enhanced with:
- OAuth flow via LibreChat UI
- Token pre-provisioning
- Alternative authentication methods

---

## Security Best Practices

### 1. Credential Storage
✅ **Do**: Use environment variables with LibreChat .env file
✅ **Do**: Use file-based secrets for Docker/K8s
❌ **Don't**: Hardcode credentials in librechat.yaml
❌ **Don't**: Commit credentials to version control

### 2. Token Storage
✅ **Do**: Use persistent volumes for token storage
✅ **Do**: Use user-specific token directories for multi-tenant
✅ **Do**: Set restrictive permissions (chmod 700)
❌ **Don't**: Share token storage across users
❌ **Don't**: Store tokens in temporary directories

### 3. Multi-User Deployments
✅ **Do**: Use `customUserVars` for per-user credentials
✅ **Do**: Isolate token storage with `{{LIBRECHAT_USER_ID}}`
✅ **Do**: Set `startup: false` when using customUserVars
❌ **Don't**: Share Garmin accounts across users
❌ **Don't**: Use admin credentials for all users

### 4. Logging
✅ **Do**: Use INFO or WARNING in production
✅ **Do**: Rotate log files if using LOG_FILE
✅ **Do**: Monitor logs for authentication failures
❌ **Don't**: Use DEBUG in production (logs may contain sensitive data)
❌ **Don't**: Store logs in publicly accessible locations

---

## Complete Configuration Example

Here's a production-ready configuration with all best practices:

```yaml
# librechat.yaml
mcpServers:
  # Single-user deployment (shared Garmin account)
  garmin-shared:
    type: stdio
    command: uvx
    args:
      - --from
      - git+https://github.com/Varming73/garmin_mcp
      - garmin-mcp
    env:
      GARMIN_EMAIL: "${GARMIN_EMAIL}"
      GARMIN_PASSWORD: "${GARMIN_PASSWORD}"
      GARMINTOKENS: "/var/lib/garmin-mcp/tokens"
      LOG_LEVEL: "INFO"
    timeout: 60000
    initTimeout: 30000
    stderr: "inherit"
    iconPath: "/app/public/assets/garmin-icon.svg"
    serverInstructions: |
      Garmin Connect MCP Server for fitness and health data access.
      Use date format YYYY-MM-DD. Check resources first: garmin://health/today
      and garmin://activities/recent for quick data access.

  # Multi-user deployment (per-user Garmin accounts)
  garmin-personal:
    type: stdio
    command: uvx
    args:
      - --from
      - git+https://github.com/Varming73/garmin_mcp
      - garmin-mcp
    customUserVars:
      GARMIN_EMAIL:
        title: "Garmin Connect Email"
        description: "Your Garmin Connect account email. Sign up at <a href='https://connect.garmin.com' target='_blank'>Garmin Connect</a> if you don't have an account."
      GARMIN_PASSWORD:
        title: "Garmin Connect Password"
        description: "Your Garmin Connect password (stored securely per user)."
    env:
      GARMIN_EMAIL: "{{GARMIN_EMAIL}}"
      GARMIN_PASSWORD: "{{GARMIN_PASSWORD}}"
      GARMINTOKENS: "/var/lib/garmin-mcp/tokens/{{LIBRECHAT_USER_ID}}"
      LOG_LEVEL: "WARNING"
    timeout: 60000
    initTimeout: 30000
    startup: false  # Requires user configuration first
    stderr: "inherit"
    iconPath: "/app/public/assets/garmin-icon.svg"
    serverInstructions: true
```

**Corresponding .env file**:
```bash
# For garmin-shared deployment
GARMIN_EMAIL=shared_account@example.com
GARMIN_PASSWORD=secure_password_here
```

---

## Testing the Configuration

After adding to `librechat.yaml`:

1. **Restart LibreChat**:
   ```bash
   docker compose restart
   # or
   systemctl restart librechat
   ```

2. **Check MCP Server Status**:
   - Open LibreChat UI
   - Go to Settings → MCP Servers
   - Verify "garmin" server shows as connected
   - Check for any error messages

3. **Test Basic Functionality**:
   - Create new chat with assistant that has MCP tools enabled
   - Ask: "Show me my recent activities"
   - Verify response includes activity data

4. **Test Resources**:
   - Ask: "How am I doing today?"
   - Verify assistant uses garmin://health/today resource

5. **Test Prompts**:
   - Ask: "Analyze my weekly activity"
   - Verify structured analysis is provided

---

## Maintenance

### Updating the Server

To update to latest version:

```yaml
# librechat.yaml - no changes needed
# uvx automatically uses latest version from git
```

To force reinstall:
```bash
# Clear uvx cache
uvx --refresh --from git+https://github.com/Varming73/garmin_mcp garmin-mcp
```

### Token Rotation

Garmin OAuth tokens automatically refresh. If tokens become invalid:
1. Server will attempt fresh login with credentials
2. New tokens saved automatically
3. No manual intervention needed

To force fresh login:
```bash
# Delete token storage
rm -rf /var/lib/garmin-mcp/tokens/*
# Restart LibreChat - will re-authenticate
```

---

## Support & Documentation

- **Server Source**: https://github.com/Varming73/garmin_mcp
- **LibreChat Docs**: https://docs.librechat.ai/
- **MCP Specification**: https://modelcontextprotocol.io/
- **Garmin Connect API**: https://github.com/cyberjunky/python-garminconnect

---

## Appendix: Development Configuration

For local development and testing:

```yaml
mcpServers:
  garmin-dev:
    type: stdio
    command: uv
    args:
      - run
      - --directory
      - /path/to/local/garmin_mcp
      - garmin-mcp
    env:
      GARMIN_EMAIL: "${GARMIN_EMAIL}"
      GARMIN_PASSWORD: "${GARMIN_PASSWORD}"
      LOG_LEVEL: "DEBUG"
      LOG_FILE: "/tmp/garmin-mcp-debug.log"
    timeout: 120000  # Longer timeout for debugging
    initTimeout: 60000
    stderr: "inherit"
```

**Benefits**:
- Uses local code (fast iteration)
- Detailed logging for debugging
- Longer timeouts for step-through debugging

---

**Last Updated**: Based on v0.2.0 refactored codebase (2025-11-12)
**Configuration Valid For**: LibreChat with MCP support (v0.7.0+)
