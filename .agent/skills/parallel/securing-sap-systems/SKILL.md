---
agents:
- none
category: parallel
description: XSUAA configuration and scopes, OAuth 2.0 flows in BTP, principal propagation
  (cloud to on-premise), CDS access control (DCL rules), API authentication patterns
knowledge:
- none
name: securing-sap-systems
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Sap Security

XSUAA configuration and scopes, OAuth 2.0 flows in BTP, principal propagation (cloud to on-premise), CDS access control (DCL rules), API authentication patterns

Implement security for SAP applications including XSUAA configuration, OAuth 2.0 flows, principal propagation, CDS access control, and API authentication patterns.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Configure XSUAA Scopes and Roles

```json
{
  "xsappname": "travel-booking-app",
  "tenant-mode": "dedicated",
  "scopes": [
    {
      "name": "$XSAPPNAME.Display",
      "description": "Display travel bookings"
    },
    {
      "name": "$XSAPPNAME.Edit",
      "description": "Edit travel bookings"
    },
    {
      "name": "$XSAPPNAME.Delete",
      "description": "Delete travel bookings"
    },
    {
      "name": "$XSAPPNAME.Admin",
      "description": "Admin access"
    }
  ],
  "role-templates": [
    {
      "name": "TravelBookingViewer",
      "description": "View travel bookings",
      "scope-references": [
        "$XSAPPNAME.Display"
      ]
    },
    {
      "name": "TravelBookingEditor",
      "description": "Edit travel bookings",
      "scope-references": [
        "$XSAPPNAME.Display",
        "$XSAPPNAME.Edit"
      ]
    },
    {
      "name": "TravelBookingAdmin",
      "description": "Admin access",
      "scope-references": [
        "$XSAPPNAME.Display",
        "$XSAPPNAME.Edit",
        "$XSAPPNAME.Delete",
        "$XSAPPNAME.Admin"
      ]
    }
  ],
  "role-collections": [
    {
      "name": "TravelBookingViewer",
      "role-template-references": [
        "$XSAPPNAME.TravelBookingViewer"
      ]
    },
    {
      "name": "TravelBookingEditor",
      "role-template-references": [
        "$XSAPPNAME.TravelBookingEditor"
      ]
    },
    {
      "name": "TravelBookingAdmin",
      "role-template-references": [
        "$XSAPPNAME.TravelBookingAdmin"
      ]
    }
  ],
  "oauth2-configuration": {
    "redirect-uris": [
      "https://*.cfapps.*.hana.ondemand.com/**",
      "https://*.kyma.*.hana.ondemand.com/**"
    ],
    "system-attributes": [
      "xs.system.attributes.rolecollections"
    ],
    "token-validity": 3600
  }
}
```

### Step 2: Implement OAuth 2.0 Client Credentials Flow

```javascript
// OAuth 2.0 Client Credentials Flow
const axios = require('axios');
const https = require('https');

class XSUAAClient {
    constructor(xsuaaUrl, clientId, clientSecret) {
        this.xsuaaUrl = xsuaaUrl;
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.token = null;
        this.tokenExpiry = null;
    }

    async getAccessToken() {
        // Check if token is still valid
        if (this.token && this.tokenExpiry && Date.now() < this.tokenExpiry) {
            return this.token;
        }

        try {
            const response = await axios.post(
                `${this.xsuaaUrl}/oauth/token`,
                new URLSearchParams({
                    grant_type: 'client_credentials',
                    client_id: this.clientId,
                    client_secret: this.clientSecret
                }),
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    httpsAgent: new https.Agent({
                        rejectUnauthorized: false // Only for development
                    })
                }
            );

            this.token = response.data.access_token;
            const expiresIn = response.data.expires_in || 3600;
            this.tokenExpiry = Date.now() + (expiresIn * 1000) - 60000; // Refresh 1 minute before expiry

            return this.token;
        } catch (error) {
            console.error('Error getting access token:', error);
            throw error;
        }
    }

    async validateToken(token) {
        try {
            const response = await axios.get(
                `${this.xsuaaUrl}/userinfo`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );
            return response.data;
        } catch (error) {
            console.error('Error validating token:', error);
            throw error;
        }
    }
}

// Usage
const xsuaaClient = new XSUAAClient(
    'https://your-subaccount.authentication.us10.hana.ondemand.com',
    'your-client-id',
    'your-client-secret'
);

const token = await xsuaaClient.getAccessToken();
```

### Step 3: Implement OAuth 2.0 Authorization Code Flow

```javascript
// OAuth 2.0 Authorization Code Flow
const express = require('express');
const axios = require('axios');
const session = require('express-session');

const app = express();
app.use(session({ secret: 'your-secret-key' }));

// Step 1: Redirect to authorization endpoint
app.get('/login', (req, res) => {
    const authUrl = `${xsuaaUrl}/oauth/authorize?` +
        `client_id=${clientId}&` +
        `response_type=code&` +
        `redirect_uri=${encodeURIComponent(redirectUri)}&` +
        `scope=${encodeURIComponent(scope)}&` +
        `state=${req.session.state || 'random-state'}`;

    req.session.state = 'random-state';
    res.redirect(authUrl);
});

// Step 2: Handle callback and exchange code for token
app.get('/callback', async (req, res) => {
    const { code, state } = req.query;

    if (state !== req.session.state) {
        return res.status(400).send('Invalid state parameter');
    }

    try {
        const response = await axios.post(
            `${xsuaaUrl}/oauth/token`,
            new URLSearchParams({
                grant_type: 'authorization_code',
                client_id: clientId,
                client_secret: clientSecret,
                code: code,
                redirect_uri: redirectUri
            }),
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        );

        req.session.accessToken = response.data.access_token;
        req.session.refreshToken = response.data.refresh_token;

        res.redirect('/dashboard');
    } catch (error) {
        console.error('Error exchanging code for token:', error);
        res.status(500).send('Authentication failed');
    }
});

// Step 3: Use access token for API calls
app.get('/api/travel-bookings', async (req, res) => {
    if (!req.session.accessToken) {
        return res.redirect('/login');
    }

    try {
        const response = await axios.get(
            'https://your-api.cfapps.us10.hana.ondemand.com/api/travel-bookings',
            {
                headers: {
                    'Authorization': `Bearer ${req.session.accessToken}`
                }
            }
        );

        res.json(response.data);
    } catch (error) {
        if (error.response?.status === 401) {
            // Token expired, refresh or redirect to login
            return res.redirect('/login');
        }
        res.status(500).send('Error fetching travel bookings');
    }
});
```

### Step 4: Implement Principal Propagation

```javascript
// Principal Propagation to On-Premise System
const axios = require('axios');
const https = require('https');

class PrincipalPropagationClient {
    constructor(destinationName, xsuaaClient) {
        this.destinationName = destinationName;
        this.xsuaaClient = xsuaaClient;
    }

    async callOnPremiseService(endpoint, userToken) {
        try {
            // Get destination configuration
            const destination = await this.getDestination(this.destinationName);

            // Add principal propagation headers
            const headers = {
                'Authorization': `Bearer ${userToken}`,
                'SAP-Connectivity-Authentication': 'PrincipalPropagation',
                'Content-Type': 'application/json'
            };

            // Call on-premise service through Cloud Connector
            const response = await axios.get(
                `${destination.url}${endpoint}`,
                {
                    headers: headers,
                    httpsAgent: new https.Agent({
                        rejectUnauthorized: false // Only for development
                    })
                }
            );

            return response.data;
        } catch (error) {
            console.error('Error calling on-premise service:', error);
            throw error;
        }
    }

    async getDestination(name) {
        // Get destination from Destination service
        const token = await this.xsuaaClient.getAccessToken();

        const response = await axios.get(
            `https://destination-configuration.cfapps.us10.hana.ondemand.com/destination-configuration/v1/destinations/${name}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );

        return response.data;
    }
}
```

### Step 5: Create CDS Access Control (DCL) Rules

```abap
@EndUserText.label: 'Travel Booking Access Control'
@MappingRole: true
define role ZC_TravelBooking {
  grant select on ZI_TravelBooking
    where ( AgencyID ) = aspect pfcg_auth( ZTRAVELBOOK, AGENCYID, ACTVT = '03' )
       or ( CreatedBy ) = aspect user_filter( CreatedBy );
}

@EndUserText.label: 'Travel Booking Item Access Control'
@MappingRole: true
define role ZC_TravelBookingItem {
  grant select on ZI_TravelBookingItem
    where ( _TravelBooking.AgencyID ) = aspect pfcg_auth( ZTRAVELBOOK, AGENCYID, ACTVT = '03' );
}

@EndUserText.label: 'Travel Booking Admin Access Control'
@MappingRole: true
define role ZC_TravelBookingAdmin {
  grant select, insert, update, delete on ZI_TravelBooking
    where ( AgencyID ) = aspect pfcg_auth( ZTRAVELBOOK, AGENCYID, ACTVT = '02' );
}
```

### Step 6: Implement API Authentication Middleware

```javascript
// API Authentication Middleware
const jwt = require('jsonwebtoken');
const axios = require('axios');

class AuthenticationMiddleware {
    constructor(xsuaaUrl, clientId) {
        this.xsuaaUrl = xsuaaUrl;
        this.clientId = clientId;
        this.publicKey = null;
    }

    async getPublicKey() {
        if (this.publicKey) {
            return this.publicKey;
        }

        try {
            const response = await axios.get(
                `${this.xsuaaUrl}/token_keys`
            );

            // Get the first key (in production, select based on kid)
            this.publicKey = response.data.keys[0];
            return this.publicKey;
        } catch (error) {
            console.error('Error getting public key:', error);
            throw error;
        }
    }

    async authenticate(req, res, next) {
        try {
            const authHeader = req.headers.authorization;

            if (!authHeader || !authHeader.startsWith('Bearer ')) {
                return res.status(401).json({ error: 'Missing or invalid authorization header' });
            }

            const token = authHeader.substring(7);
            const publicKey = await this.getPublicKey();

            // Verify token
            const decoded = jwt.verify(token, publicKey, {
                algorithms: ['RS256'],
                issuer: `${this.xsuaaUrl}/oauth/token`,
                audience: this.clientId
            });

            // Check scopes
            const scopes = decoded.scope || [];
            req.user = {
                id: decoded.user_id || decoded.sub,
                email: decoded.email,
                scopes: scopes
            };

            next();
        } catch (error) {
            console.error('Authentication error:', error);
            return res.status(401).json({ error: 'Invalid or expired token' });
        }
    }

    requireScope(scope) {
        return (req, res, next) => {
            if (!req.user || !req.user.scopes.includes(scope)) {
                return res.status(403).json({ error: `Missing required scope: ${scope}` });
            }
            next();
        };
    }
}

// Usage
const authMiddleware = new AuthenticationMiddleware(
    'https://your-subaccount.authentication.us10.hana.ondemand.com',
    'your-client-id'
);

app.get('/api/travel-bookings',
    authMiddleware.authenticate.bind(authMiddleware),
    authMiddleware.requireScope('$XSAPPNAME.Display'),
    async (req, res) => {
        // Handle request
    }
);
```

### Step 7: Configure Destination Authentication

```json
{
  "name": "S4HANA_ONPREMISE",
  "description": "S/4HANA On-Premise System",
  "type": "HTTP",
  "url": "https://s4hana.example.com",
  "authentication": "PrincipalPropagation",
  "proxyType": "OnPremise",
  "cloudConnectorLocationId": "EU1",
  "sapCloudConnectorVersion": "latest"
}
```

## Security Patterns

### OAuth 2.0 Flows
- **Client Credentials**: Server-to-server communication
- **Authorization Code**: User authentication with redirect
- **Resource Owner Password**: Direct username/password (not recommended)
- **Implicit**: Client-side apps (deprecated)

### Principal Propagation
- **SAML Assertion**: For SAML-based systems
- **OAuth 2.0 Token**: For OAuth-based systems
- **X.509 Certificate**: For certificate-based systems
- **Basic Authentication**: For legacy systems

### CDS Access Control
- **Field-level**: Control access to specific fields
- **Instance-level**: Control access to specific records
- **Role-based**: Based on user roles
- **Attribute-based**: Based on entity attributes

## Best Practices

- Use XSUAA for all BTP applications
- Implement proper scope-based authorization
- Use principal propagation for on-premise connectivity
- Implement CDS access control for data security
- Use OAuth 2.0 authorization code flow for user apps
- Use client credentials flow for server-to-server
- Never hardcode credentials (use secure stores)
- Implement token refresh mechanisms
- Validate tokens on every request
- Use HTTPS for all communications
- Implement proper error handling
- Log security events for auditing
- Use role-based access control (RBAC)
- Implement least privilege principle
- Configure proper token validity periods (short for access tokens, longer for refresh tokens)
- Use destination service for managing connection configurations securely
- Implement proper CORS policies for API endpoints to prevent unauthorized access
- Regularly rotate client secrets and review XSUAA scopes for unused permissions
- Use Cloud Connector with proper authentication for secure on-premise connectivity

## Anti-Patterns

- Hardcoding credentials (use secure credential stores)
- Not validating tokens (security vulnerability)
- Missing scope checks (unauthorized access)
- Not using principal propagation (authentication failures)
- Missing CDS access control (data exposure)
- Using deprecated OAuth flows (security risks)
- Not implementing token refresh (poor user experience)
- Missing error handling (information leakage)
- Not logging security events (audit trail missing)
- Using HTTP instead of HTTPS (data exposure)

## Related

- Skill: `btp-deployment` - XSUAA configuration in MTA
- Skill: `integrating-sap-systems` - API authentication patterns
- Knowledge: `sap-security-patterns.json` - Security patterns and guidelines

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
