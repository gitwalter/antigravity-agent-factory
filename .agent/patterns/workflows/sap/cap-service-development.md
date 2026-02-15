# CAP Service Development Workflow

## Overview

End-to-end workflow for developing SAP Cloud Application Programming Model (CAP) services. Covers CDS modeling, service implementation, testing, and deployment to SAP BTP.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** sap-cap

## Trigger Conditions

This workflow is activated when:

- New CAP service required
- OData/REST API for SAP needed
- Full-stack BTP application
- Fiori Elements on CAP

**Trigger Examples:**
- "Create a CAP service for customer management"
- "Build a Fiori app with CAP backend"
- "Deploy CAP service to BTP"
- "Implement custom handlers in CAP"

## Phases

### Phase 1: CDS Domain Modeling

**Description:** Define the domain model using CDS.

**Entry Criteria:** Requirements defined
**Exit Criteria:** Domain model complete

#### Step 1.1: Create Entity Definitions

**Actions:**
- Define entities in db/schema.cds
- Add relationships and associations
- Define types and enums
- Add annotations

**CDS Entity Template:**
```cds
namespace my.bookshop;

entity Books {
  key ID : UUID;
  title  : String(111);
  descr  : String(1111);
  author : Association to Authors;
  stock  : Integer;
  price  : Decimal(9,2);
}

entity Authors {
  key ID : UUID;
  name   : String(111);
  books  : Association to many Books on books.author = $self;
}
```

#### Step 1.2: Add Aspects

**Actions:**
- Add managed aspect (cuid, temporal)
- Add audit fields
- Add localization
- Add extensibility

**Aspects:**
```cds
using { cuid, managed, temporal } from '@sap/cds/common';

entity Books : cuid, managed {
  // managed adds createdAt, createdBy, modifiedAt, modifiedBy
}
```

**Knowledge:**
- `sap-cap-patterns.json`: CAP patterns

**Outputs:**
- Domain model
- Entity relationships

**Is Mandatory:** Yes

---

### Phase 2: Service Definition

**Description:** Define and expose services.

**Entry Criteria:** Domain model complete
**Exit Criteria:** Services defined

#### Step 2.1: Create Service Definitions

**Actions:**
- Create service in srv/ folder
- Project entities
- Add custom actions/functions
- Define access control

**Service Template:**
```cds
using my.bookshop from '../db/schema';

service CatalogService {
  @readonly entity Books as projection on bookshop.Books;
  @readonly entity Authors as projection on bookshop.Authors;

  action submitOrder(book : Books:ID, quantity : Integer);
  function getBooksByAuthor(author : String) returns array of Books;
}

service AdminService @(requires: 'admin') {
  entity Books as projection on bookshop.Books;
  entity Authors as projection on bookshop.Authors;
}
```

**Outputs:**
- Service definitions
- Access control

**Is Mandatory:** Yes

---

### Phase 3: Service Implementation

**Description:** Implement custom handlers and logic.

**Entry Criteria:** Services defined
**Exit Criteria:** Handlers implemented

#### Step 3.1: Implement Event Handlers

**Actions:**
- Create handler file
- Implement before/on/after handlers
- Add validation logic
- Implement custom actions

**Handler Template (Node.js):**
```javascript
const cds = require('@sap/cds');

module.exports = class CatalogService extends cds.ApplicationService {
  async init() {
    const { Books } = this.entities;

    this.before('CREATE', Books, req => {
      if (req.data.stock < 0) {
        req.error(400, 'Stock cannot be negative');
      }
    });

    this.on('submitOrder', async req => {
      const { book, quantity } = req.data;
      // Implementation
    });

    await super.init();
  }
};
```

**Handler Template (Java):**
```java
@Component
@ServiceName(CatalogService_.CDS_NAME)
public class CatalogServiceHandler implements EventHandler {

    @Before(event = CqnService.EVENT_CREATE, entity = Books_.CDS_NAME)
    public void beforeCreateBook(Books book) {
        if (book.getStock() < 0) {
            throw new ServiceException("Stock cannot be negative");
        }
    }
}
```

**Outputs:**
- Event handlers
- Custom actions

**Is Mandatory:** Yes

---

### Phase 4: Testing

**Description:** Test the CAP service.

**Entry Criteria:** Handlers implemented
**Exit Criteria:** Tests passing

#### Step 4.1: Unit Testing

**Actions:**
- Create test file
- Test CRUD operations
- Test custom actions
- Test validations

**Test Template:**
```javascript
const cds = require('@sap/cds/lib');
const { expect } = require('chai');

describe('CatalogService', () => {
  let srv;

  before(async () => {
    srv = await cds.connect.to('CatalogService');
  });

  it('should read books', async () => {
    const books = await srv.read('Books');
    expect(books).to.be.an('array');
  });

  it('should reject negative stock', async () => {
    const result = await srv.create('Books', { stock: -1 })
      .catch(e => e);
    expect(result.code).to.equal(400);
  });
});
```

#### Step 4.2: Integration Testing

**Actions:**
- Test with database
- Test OData endpoints
- Test authentication
- Test error handling

**Outputs:**
- Test results
- Coverage report

**Is Mandatory:** Yes

---

### Phase 5: Fiori UI (Optional)

**Description:** Add Fiori Elements UI.

**Entry Criteria:** Service tested
**Exit Criteria:** UI configured

#### Step 5.1: Add UI Annotations

**Actions:**
- Add @UI annotations
- Configure list report
- Configure object page
- Add value helps

**UI Annotations:**
```cds
annotate CatalogService.Books with @(
  UI: {
    HeaderInfo: {
      TypeName: 'Book',
      TypeNamePlural: 'Books',
      Title: { Value: title }
    },
    SelectionFields: [ title, author_ID ],
    LineItem: [
      { Value: title },
      { Value: author.name },
      { Value: stock },
      { Value: price }
    ]
  }
);
```

#### Step 5.2: Create Fiori App

**Actions:**
- Generate Fiori Elements app
- Configure app manifest
- Add i18n
- Test locally

**Outputs:**
- Fiori Elements app
- App manifest

**Is Mandatory:** No

---

### Phase 6: BTP Deployment

**Description:** Deploy to SAP BTP Cloud Foundry.

**Entry Criteria:** Testing complete
**Exit Criteria:** Deployed to BTP

#### Step 6.1: Configure MTA

**Actions:**
- Create mta.yaml
- Configure modules
- Add resources
- Set destinations

**MTA Template:**
```yaml
_schema-version: '3.1'
ID: bookshop
version: 1.0.0

modules:
  - name: bookshop-srv
    type: nodejs
    path: gen/srv
    requires:
      - name: bookshop-db
      - name: bookshop-auth
    provides:
      - name: srv-api
        properties:
          srv-url: ${default-url}

  - name: bookshop-db-deployer
    type: hdb
    path: gen/db
    requires:
      - name: bookshop-db

resources:
  - name: bookshop-db
    type: com.sap.xs.hdi-container
  - name: bookshop-auth
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
```

#### Step 6.2: Build and Deploy

**Actions:**
- Build MTA archive
- Deploy to BTP
- Verify deployment
- Test endpoints

**Commands:**
```bash
mbt build
cf deploy mta_archives/bookshop_1.0.0.mtar
```

**Outputs:**
- Deployed application
- Service URLs

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Database Selection

| Requirement | Database |
|-------------|----------|
| Development | SQLite |
| Production SAP | SAP HANA |
| Production Cloud | PostgreSQL |

### Decision: Service Layer

| Need | Approach |
|------|----------|
| Simple CRUD | Auto-exposed entities |
| Custom logic | Custom handlers |
| Complex queries | Custom actions/functions |

### Decision: Deployment Target

| Environment | Target |
|-------------|--------|
| Development | Local |
| Testing | CF trial |
| Production | CF production |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| HANA not available | Use SQLite for development |
| BTP deployment fails | Check quotas and entitlements |
| Handler errors | Add error handling middleware |
| Service binding fails | Manual binding via CLI |

---

## Example Session

```
User: Create a CAP service for order management

Agent:
━━━ PHASE 1: CDS Domain Modeling ━━━
Creating entities...

db/schema.cds:
✓ Orders entity
✓ OrderItems entity
✓ Products entity
✓ Associations defined

━━━ PHASE 2: Service Definition ━━━
Creating services...

srv/orders-service.cds:
✓ OrderService exposed
✓ Actions: submitOrder, cancelOrder
✓ Access control configured

━━━ PHASE 3: Implementation ━━━
Implementing handlers...

srv/orders-service.js:
✓ Validation: stock check
✓ Action: submitOrder
✓ Action: cancelOrder

━━━ PHASE 4: Testing ━━━
Running tests...

✓ 15/15 tests passing
✓ Coverage: 92%

━━━ PHASE 5: Fiori UI ━━━
Adding UI annotations...

✓ List Report: Orders
✓ Object Page: Order details
✓ Value helps configured

━━━ PHASE 6: Deployment ━━━
Building MTA...
✓ Build successful

Deploying to BTP...
✓ Deployed to cf space 'dev'

Service URL: https://orders-srv.cfapps.eu10.hana.ondemand.com

✨ CAP service deployed!
```

---

## Related Artifacts

- **Knowledge**: `knowledge/sap-cap-patterns.json`
- **Blueprints**: `blueprints/sap-cap/blueprint.json`
