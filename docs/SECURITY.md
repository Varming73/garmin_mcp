# Security Documentation

## Overview

This document outlines the security considerations and best practices for the Garmin MCP Server.

## Authentication & Credentials

### Credential Storage

The server requires Garmin Connect credentials which can be provided in two ways:

1. **Environment Variables** (for development):
   ```bash
   export GARMIN_EMAIL="your-email@example.com"
   export GARMIN_PASSWORD="your-password"
   ```

2. **File-based Secrets** (recommended for production/Docker):
   ```bash
   export GARMIN_EMAIL_FILE="/run/secrets/garmin_email"
   export GARMIN_PASSWORD_FILE="/run/secrets/garmin_password"
   ```

### Security Best Practices for Credentials

- ✅ **DO**: Use file-based secrets in production environments
- ✅ **DO**: Use Docker secrets or Kubernetes secrets for containerized deployments
- ✅ **DO**: Rotate credentials regularly
- ✅ **DO**: Use dedicated service accounts where possible
- ❌ **DON'T**: Commit credentials to version control
- ❌ **DON'T**: Share credentials across multiple services
- ❌ **DON'T**: Store credentials in plain text files with weak permissions

### Token Management

OAuth tokens are stored in:
- Default: `~/.garminconnect` (directory with token files)
- Alternative: `~/.garminconnect_base64` (base64-encoded tokens)

**Token Security:**
- Tokens are stored with user-only read/write permissions
- Tokens automatically refresh when expired
- Failed authentication triggers fresh login flow

**Environment Variables:**
- `GARMINTOKENS`: Custom path for token directory
- `GARMINTOKENS_BASE64`: Custom path for base64 token file

## Network Security

### HTTPS/TLS

- All communication with Garmin Connect uses HTTPS
- Certificate validation is enforced by the `garminconnect` library
- No support for insecure HTTP connections

### API Rate Limiting

**Current Status**: Not implemented (roadmap item)

**Recommendations**:
- Implement client-side rate limiting to avoid API bans
- Use exponential backoff for retry logic
- Cache frequently accessed data

## Data Privacy

### Data Access

The MCP server only accesses data that you explicitly request through tools:
- Activity data
- Health metrics
- Sleep data
- Body composition
- Device information

### Data Storage

- **Local Only**: No data is persisted by the MCP server
- **OAuth Tokens**: Only authentication tokens are stored locally
- **No Logging of Sensitive Data**: Credentials are never logged

### Data Transmission

- Data is transmitted directly between:
  1. Garmin Connect → MCP Server
  2. MCP Server → Claude (or other MCP clients)
- No intermediate services or third-party APIs involved

## Input Validation

All user inputs are validated using Pydantic models before processing:

- Date formats (YYYY-MM-DD)
- Numeric ranges (e.g., activity IDs > 0)
- String lengths
- Optional parameter validation

Example validation:
```python
class ActivityIdInput(BaseModel):
    activity_id: int = Field(..., gt=0, description="Activity ID must be positive")
```

## Error Handling

### Secure Error Messages

Error responses follow a structured format that avoids exposing sensitive information:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "authentication_error",
    "message": "Authentication failed"
  }
}
```

### Logging

- Errors are logged with context but without sensitive data
- Stack traces are logged only in DEBUG mode
- Credentials are never included in logs
- Use `LOG_LEVEL` environment variable to control verbosity

## Multi-Factor Authentication (MFA)

The server supports Garmin Connect's MFA:
- Interactive prompt when MFA is required
- MFA codes are not stored or cached
- Fresh authentication required after MFA

**Note**: MFA in server environments requires terminal access for code input.

## Security Audit Trail

### Logging Configuration

Configure logging for audit purposes:

```bash
export LOG_LEVEL="INFO"
export LOG_FILE="/var/log/garmin-mcp/server.log"
```

Logged events include:
- Authentication attempts (success/failure)
- API requests (without sensitive data)
- Configuration errors
- System errors

## Dependency Security

### Vulnerability Scanning

The project uses:
- **Dependabot**: Automated dependency updates
- **Safety**: Python dependency vulnerability scanning (in CI)
- **GitHub Security Advisories**: Automatic alerts for known vulnerabilities

### Dependency Policy

- Dependencies are version-pinned with `~=` for patch updates
- Regular updates via Dependabot PRs
- Security updates prioritized over feature updates

## Container Security

When deploying in containers:

1. **Use Official Base Images**:
   ```dockerfile
   FROM python:3.10-slim
   ```

2. **Run as Non-Root User**:
   ```dockerfile
   RUN useradd -m -u 1000 garmin
   USER garmin
   ```

3. **Secret Management**:
   ```dockerfile
   # Use Docker secrets
   RUN --mount=type=secret,id=garmin_email \
       --mount=type=secret,id=garmin_password
   ```

4. **Read-Only Filesystem** (where possible):
   ```yaml
   security_opt:
     - no-new-privileges:true
   read_only: true
   ```

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public GitHub issue
2. Email security concerns to: [maintainer-email]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

We will respond within 48 hours and work with you to address the issue.

## Security Checklist

Before deploying to production:

- [ ] Credentials stored using secure secret management
- [ ] Token directories have appropriate file permissions (600)
- [ ] Logging configured with appropriate verbosity
- [ ] Log files have restricted access
- [ ] Running as non-root user (if containerized)
- [ ] Network access restricted to Garmin Connect APIs
- [ ] Dependencies are up to date
- [ ] Security scanning enabled in CI/CD
- [ ] MFA enabled on Garmin Connect account

## Known Limitations

1. **MFA Interactive Prompt**: Requires terminal access, not suitable for headless deployments with MFA-enabled accounts
2. **No Rate Limiting**: Currently no client-side rate limiting (use with caution)
3. **Token Refresh**: Failed refresh requires manual intervention
4. **Credential Rotation**: Requires server restart

## Future Security Enhancements

Planned improvements:
- Implement client-side rate limiting
- Add support for OAuth flow without password storage
- Implement request retry with exponential backoff
- Add circuit breaker pattern for API failures
- Encrypted token storage option
- Audit log export functionality

## Compliance

This software:
- Does not store user data beyond authentication tokens
- Communicates directly with Garmin Connect APIs
- Does not share data with third parties
- Operates entirely under user control

**Note**: Users are responsible for compliance with Garmin's Terms of Service and their own data protection requirements.

## References

- [Garmin Connect API Documentation](https://connect.garmin.com/)
- [garminconnect Python Library](https://github.com/cyberjunky/python-garminconnect)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

Last Updated: 2025-01-15
