# API Documentation

## Base URL
```
Production: https://your-app.run.app
Staging: https://your-app-staging.run.app
Local: http://localhost:8080
```

## Authentication

All API requests require an API key in the header:
```bash
curl -H "X-API-Key: your-api-key" https://your-app.run.app/api/endpoint
```

## Endpoints

### Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-27T10:00:00Z"
}
```

---

### Process Query

**POST** `/api/v1/query`

Process user query through agent system.

**Request:**
```json
{
  "message": "I have a headache and fever",
  "session_id": "optional-session-id",
  "context": {
    "user_id": "user123",
    "metadata": {}
  }
}
```

**Response:**
```json
{
  "response": "Based on your symptoms...",
  "session_id": "abc-123-def",
  "metadata": {
    "agent_used": "symptom-analyzer",
    "confidence": 0.95,
    "processing_time_ms": 1250
  },
  "citations": [
    {
      "source": "Medical Knowledge Base",
      "url": "https://..."
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (invalid input)
- `401` - Unauthorized (invalid API key)
- `429` - Rate limit exceeded
- `500` - Internal server error

---

### Get Conversation History

**GET** `/api/v1/history/{session_id}`

Retrieve conversation history for a session.

**Parameters:**
- `session_id` (path) - Session identifier
- `limit` (query, optional) - Number of messages to return (default: 50)

**Response:**
```json
{
  "session_id": "abc-123-def",
  "messages": [
    {
      "timestamp": "2025-12-27T10:00:00Z",
      "role": "user",
      "content": "I have a headache"
    },
    {
      "timestamp": "2025-12-27T10:00:01Z",
      "role": "assistant",
      "content": "I understand you're experiencing..."
    }
  ],
  "total": 10
}
```

---

### Clear Session

**DELETE** `/api/v1/session/{session_id}`

Clear conversation history for a session.

**Response:**
```json
{
  "message": "Session cleared successfully",
  "session_id": "abc-123-def"
}
```

---

## Rate Limiting

- **Authenticated users:** 100 requests/minute
- **Anonymous users:** 20 requests/minute

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  },
  "timestamp": "2025-12-27T10:00:00Z",
  "request_id": "req-123-abc"
}
```

### Common Error Codes

- `INVALID_INPUT` - Malformed request
- `MISSING_FIELD` - Required field missing
- `UNAUTHORIZED` - Invalid or missing API key
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `INTERNAL_ERROR` - Server error

## SDK Examples

### Python
```python
import requests

API_KEY = "your-api-key"
BASE_URL = "https://your-app.run.app"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Process query
response = requests.post(
    f"{BASE_URL}/api/v1/query",
    headers=headers,
    json={
        "message": "I have a headache",
        "session_id": "my-session"
    }
)

print(response.json())
```

### JavaScript
```javascript
const API_KEY = 'your-api-key';
const BASE_URL = 'https://your-app.run.app';

async function processQuery(message) {
  const response = await fetch(`${BASE_URL}/api/v1/query`, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message,
      session_id: 'my-session'
    })
  });
  
  return await response.json();
}

processQuery('I have a headache')
  .then(data => console.log(data));
```

### cURL
```bash
curl -X POST https://your-app.run.app/api/v1/query \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a headache",
    "session_id": "my-session"
  }'
```

## Webhooks

Configure webhooks to receive real-time updates.

**Webhook URL:** Set in dashboard
**Events:** `query.completed`, `session.created`, `error.occurred`

**Payload:**
```json
{
  "event": "query.completed",
  "timestamp": "2025-12-27T10:00:00Z",
  "data": {
    "session_id": "abc-123",
    "message": "...",
    "response": "..."
  }
}
```

---

Last Updated: December 2025
