[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/taxuspt-garmin-mcp-badge.png)](https://mseep.ai/app/taxuspt-garmin-mcp)

# Garmin MCP Server

This Model Context Protocol (MCP) server connects to Garmin Connect and exposes your fitness and health data to Claude and other MCP-compatible clients.

## Features

### Core Functionality
- 🏃 **Activity Management**: List, query, and analyze your activities with detailed metrics
- ❤️ **Health & Wellness**: Access steps, heart rate, sleep, stress, body battery, and more
- 📊 **Body Composition**: Track weight, body fat, muscle mass, and other composition metrics
- 🎯 **Training Insights**: Monitor training status, readiness, VO2 max, and fitness age
- ⌚ **Device Management**: View and manage your Garmin devices
- 🎽 **Gear Tracking**: Track equipment usage across activities
- 🏆 **Challenges & Badges**: View your achievements and active challenges

### Technical Features (v0.2.0)
- ✅ **Type Safety**: Full type hints throughout codebase
- ✅ **Input Validation**: Pydantic models for all user inputs
- ✅ **Structured Logging**: Comprehensive logging with configurable levels
- ✅ **Error Handling**: Detailed error responses with proper exception handling
- ✅ **MCP Resources**: Direct access to health summaries and recent activities
- ✅ **MCP Prompts**: Pre-defined templates for common analyses
- ✅ **Health Check**: Built-in health check endpoint
- ✅ **CI/CD**: Automated testing and linting with GitHub Actions
- ✅ **Standardized Responses**: All tools return consistent JSON format

## Setup

1. Install the required packages on a new environment:

```bash
uv sync
```

## Running the Server

### Configuration

Your Garmin Connect credentials are read from environment variables:

- `GARMIN_EMAIL`: Your Garmin Connect email address
- `GARMIN_EMAIL_FILE`: Path to a file containing your Garmin Connect email address
- `GARMIN_PASSWORD`: Your Garmin Connect password
- `GARMIN_PASSWORD_FILE`: Path to a file containing your Garmin Connect password

File-based secrets are useful in certain environments, such as inside a Docker container. Note that you cannot set both `GARMIN_EMAIL` and `GARMIN_EMAIL_FILE`, similarly you cannot set both `GARMIN_PASSWORD` and `GARMIN_PASSWORD_FILE`.

### With Claude Desktop

1. Create a configuration in Claude Desktop:

Edit your Claude Desktop configuration file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add this server configuration:

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uvx",
      "args": [
        "--python",
        "3.12",
        "--from",
        "git+https://github.com/Taxuspt/garmin_mcp",
        "garmin-mcp"
      ],
      "env": {
        "GARMIN_EMAIL": "YOUR_GARMIN_EMAIL",
        "GARMIN_PASSWORD": "YOUR_GARMIN_PASSWORD"
      }
    }
  }
}
```

Replace the path with the absolute path to your server file.

2. Restart Claude Desktop

### With MCP Inspector

For testing, you can use the MCP Inspector from the project root:

```bash
npx @modelcontextprotocol/inspector uv run garmin-mcp
```

## Usage Examples

Once connected in Claude, you can ask questions like:

- "Show me my recent activities"
- "What was my sleep like last night?"
- "How many steps did I take yesterday?"
- "Show me the details of my latest run"

## Security Note

### Credential Management

Your Garmin Connect credentials are sensitive. Follow these best practices:

- **Never commit credentials** to version control
- Use **file-based secrets** for production deployments (Docker, Kubernetes)
- Rotate credentials regularly
- Enable MFA on your Garmin Connect account

### OAuth Token Storage

- Tokens are stored in `~/.garminconnect` with user-only permissions
- Tokens automatically refresh when expired
- Alternative base64 storage available at `~/.garminconnect_base64`

### Logging

Configure logging securely:

```bash
export LOG_LEVEL="INFO"          # Options: DEBUG, INFO, WARNING, ERROR
export LOG_FILE="/var/log/garmin-mcp/server.log"  # Optional log file
```

### For Detailed Security Information

See [Security Documentation](docs/SECURITY.md) for:
- Credential storage best practices
- Network security considerations
- Container security guidelines
- Vulnerability reporting process
- Compliance information

## Troubleshooting

If you encounter login issues:

1. Verify your credentials are correct
2. Check if Garmin Connect requires additional verification
3. Ensure the garminconnect package is up to date

For other issues, check the Claude Desktop logs at:

- macOS: `~/Library/Logs/Claude/mcp-server-garmin.log`
- Windows: `%APPDATA%\Claude\logs\mcp-server-garmin.log`

## Development

### Running Tests

```bash
# Install dev dependencies
uv sync --all-extras

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/garmin_mcp --cov-report=html

# Run specific tests
uv run pytest tests/unit/
```

### Code Quality

```bash
# Format code
uv run ruff format src/

# Lint code
uv run ruff check src/ --fix

# Type check
uv run mypy src/garmin_mcp --ignore-missing-imports
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup instructions
- Code style guidelines
- Testing requirements
- Pull request process

## Changelog

### v0.2.0 (2025-01-15)
- ✨ Added comprehensive type hints throughout codebase
- ✨ Implemented input validation with Pydantic models
- ✨ Added structured logging and error handling
- ✨ Standardized all tool responses to JSON format
- ✨ Added MCP resources and prompts
- ✨ Created health check module
- ✨ Added CI/CD with GitHub Actions
- 📝 Completed security documentation
- 🐛 Fixed variable shadowing bug in credential loading
- 🐛 Fixed test file referencing non-existent file
- 🧹 Removed dead code from main module
- 🔧 Updated dependencies with better version constraints
- 🧪 Added test infrastructure with pytest and coverage

### v0.1.0
- Initial release with basic Garmin Connect integration

## License

MIT License - see [LICENSE](LICENSE) file for details
