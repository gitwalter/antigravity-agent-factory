---
description: BTP Cloud Foundry deployment (cf push, MTA), service bindings (XSUAA,
  destination, connectivity), Kyma runtime deployment, SAP Build Work Zone integration
name: btp-deployment
type: skill
---
# Btp Deployment

BTP Cloud Foundry deployment (cf push, MTA), service bindings (XSUAA, destination, connectivity), Kyma runtime deployment, SAP Build Work Zone integration

Deploy SAP applications to SAP BTP (Business Technology Platform) using Cloud Foundry, MTA (Multi-Target Application), Kyma runtime, and configure service bindings for XSUAA, destinations, and connectivity.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Create MTA Descriptor (mta.yaml)

```yaml
_schema-version: '3.1'
ID: travel-booking-app
version: 1.0.0
description: Travel Booking Application

modules:
  - name: travel-booking-srv
    type: nodejs
    path: srv
    requires:
      - name: travel-booking-db
      - name: travel-booking-auth
    provides:
      - name: srv-api
        properties:
          srv-url: ${default-url}
    parameters:
      memory: 512M
      disk-quota: 512M

  - name: travel-booking-ui
    type: html5
    path: app
    requires:
      - name: travel-booking-db
      - name: travel-booking-auth
      - name: srv-api
        group: destinations
        properties:
          name: travel-booking-api
          url: ~{srv-api/srv-url}
    build-parameters:
      supported-platforms: []

  - name: travel-booking-db-deployer
    type: hdb
    path: db
    requires:
      - name: travel-booking-db
    parameters:
      buildpack: nodejs_buildpack

resources:
  - name: travel-booking-db
    type: com.sap.xs.hdi-container
    parameters:
      service: hana
      service-plan: hdi-shared

  - name: travel-booking-auth
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
      path: ./xs-security.json
      config:
        xsappname: travel-booking-app
        tenant-mode: dedicated
        scopes:
          - name: $XSAPPNAME.Display
            description: Display travel bookings
          - name: $XSAPPNAME.Edit
            description: Edit travel bookings
          - name: $XSAPPNAME.Admin
            description: Admin access
        role-templates:
          - name: TravelBookingViewer
            description: View travel bookings
            scope-references:
              - $XSAPPNAME.Display
          - name: TravelBookingEditor
            description: Edit travel bookings
            scope-references:
              - $XSAPPNAME.Display
              - $XSAPPNAME.Edit
          - name: TravelBookingAdmin
            description: Admin access
            scope-references:
              - $XSAPPNAME.Display
              - $XSAPPNAME.Edit
              - $XSAPPNAME.Admin
        role-collections:
          - name: TravelBookingViewer
            role-template-references:
              - $XSAPPNAME.TravelBookingViewer
          - name: TravelBookingEditor
            role-template-references:
              - $XSAPPNAME.TravelBookingEditor
          - name: TravelBookingAdmin
            role-template-references:
              - $XSAPPNAME.TravelBookingAdmin

  - name: travel-booking-destination
    type: org.cloudfoundry.managed-service
    parameters:
      service: destination
      service-plan: lite
      config:
        destinations:
          - name: S4HANA_ONPREMISE
            description: S/4HANA On-Premise System
            type: HTTP
            url: https://s4hana.example.com
            authentication: BasicAuthentication
            proxyType: Internet
            username: ${S4HANA_USER}
            password: ${S4HANA_PASSWORD}

  - name: travel-booking-connectivity
    type: org.cloudfoundry.managed-service
    parameters:
      service: connectivity
      service-plan: lite
```

### Step 2: Create XSUAA Configuration (xs-security.json)

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
    ]
  }
}
```

### Step 3: Create Manifest.yml for Cloud Foundry

```yaml
---
applications:
  - name: travel-booking-srv
    memory: 512M
    disk-quota: 512M
    instances: 1
    buildpack: nodejs_buildpack
    path: srv
    services:
      - travel-booking-db
      - travel-booking-auth
    env:
      TENCANT_MODE: dedicated
      CDS_ENV: production
      CDS_REQUIRES_DB: true
    routes:
      - route: travel-booking-srv.cfapps.us10.hana.ondemand.com

  - name: travel-booking-ui
    memory: 128M
    disk-quota: 128M
    instances: 1
    buildpack: staticfile_buildpack
    path: app
    services:
      - travel-booking-db
      - travel-booking-auth
    routes:
      - route: travel-booking-ui.cfapps.us10.hana.ondemand.com
```

### Step 4: Build and Deploy MTA

```bash
# Install MTA Build Tool
npm install -g mbt

# Build MTA archive
mbt build

# Deploy to Cloud Foundry
cf deploy mta_archives/travel-booking-app_1.0.0.mtar

# Or deploy directly
cf deploy mta_archives/travel-booking-app_1.0.0.mtar -f
```

### Step 5: Deploy to Kyma Runtime

```yaml
# kyma-deployment.yaml
apiVersion: serverless.kyma-project.io/v1alpha1
kind: Function
metadata:
  name: travel-booking-function
  namespace: default
spec:
  runtime: nodejs18
  source: |
    module.exports = {
      main: async function(event, context) {
        return {
          statusCode: 200,
          message: "Travel Booking Function"
        };
      }
    }
  env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: travel-booking-db-secret
          key: url
```

### Step 6: Configure SAP Build Work Zone Integration

```json
{
  "sap.app": {
    "id": "sap.travel.booking",
    "type": "application",
    "title": "Travel Booking",
    "description": "Manage travel bookings"
  },
  "sap.ui5": {
    "dependencies": {
      "minUI5Version": "1.120.0"
    }
  },
  "sap.portal": {
    "registrationIds": [
      "sap.travel.booking"
    ]
  }
}
```

### Step 7: Set Up CI/CD Pipeline

```yaml
# .github/workflows/btp-deploy.yml
name: Deploy to BTP

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Build MTA
        run: mbt build

      - name: Deploy to BTP
        env:
          CF_API: ${{ secrets.CF_API }}
          CF_USERNAME: ${{ secrets.CF_USERNAME }}
          CF_PASSWORD: ${{ secrets.CF_PASSWORD }}
          CF_ORG: ${{ secrets.CF_ORG }}
          CF_SPACE: ${{ secrets.CF_SPACE }}
        run: |
          cf login -a $CF_API -u $CF_USERNAME -p $CF_PASSWORD -o $CF_ORG -s $CF_SPACE
          cf deploy mta_archives/travel-booking-app_1.0.0.mtar
```

## BTP Services

### XSUAA (Authorization and Trust Management)
- Authentication and authorization
- OAuth 2.0 and SAML support
- Role-based access control
- Token management

### Destination Service
- On-premise connectivity
- Cloud-to-cloud connectivity
- Authentication configuration
- Proxy settings

### Connectivity Service
- Cloud Connector integration
- On-premise system access
- Principal propagation
- Network security

### SAP HANA Cloud
- Database as a service
- HDI containers
- Schema management
- Data modeling

### SAP Build Work Zone
- Fiori Launchpad integration
- App registration
- Navigation configuration
- User experience

## Deployment Strategies

### Cloud Foundry
- Standard BTP runtime
- Supports multiple languages (Node.js, Java, Python)
- Automatic scaling
- Service bindings

### Kyma Runtime
- Kubernetes-based runtime
- More control and flexibility
- Serverless functions
- Event-driven architecture

## Best Practices

- Use MTA for multi-module applications
- Configure proper XSUAA scopes and roles
- Use environment variables for configuration
- Implement proper error handling
- Set up monitoring and logging
- Use destination service for external connectivity
- Configure proper security (OAuth, SAML)
- Use CI/CD pipelines for automated deployment
- Test in development before production
- Use proper resource sizing (memory, disk)
- Configure proper service bindings
- Use Build Work Zone for Fiori apps

## Anti-Patterns

- Hardcoding credentials (use environment variables)
- Missing XSUAA configuration (security vulnerability)
- Not using MTA for multi-module apps (deployment complexity)
- Missing error handling (poor user experience)
- Not configuring destinations properly (connectivity issues)
- Missing monitoring (difficult troubleshooting)
- Not using CI/CD (manual deployment errors)
- Incorrect resource sizing (performance issues)
- Missing service bindings (runtime errors)

## Related

- Skill: `sap-security` - XSUAA and security configuration
- Knowledge: `sap-btp-patterns.json` - BTP deployment patterns

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
