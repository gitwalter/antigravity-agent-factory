# RAP Development Workflow

## Overview

End-to-end workflow for developing RESTful ABAP Programming Model (RAP) business objects in SAP S/4HANA. Covers CDS modeling, behavior definition, implementation, Fiori Elements UI, and deployment.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Applies To:** sap-rap, sap-abap

## Trigger Conditions

This workflow is activated when:

- New RAP business object required
- CRUD operations needed for SAP data
- Fiori Elements app development
- ABAP Cloud development

**Trigger Examples:**
- "Create a RAP BO for purchase orders"
- "Develop Fiori app for inventory management"
- "Build managed BO with draft handling"
- "Implement custom RAP action"

## Phases

### Phase 1: CDS Data Modeling

**Description:** Create the CDS data model for the business object.

**Entry Criteria:** Requirements defined  
**Exit Criteria:** CDS views created

#### Step 1.1: Create Database Table

**Actions:**
- Define table structure
- Set key fields
- Add semantic annotations
- Create in ADT

**Table Template:**
```abap
@EndUserText.label : 'Purchase Order'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
define table zpurchase_order {
  key client         : abap.clnt not null;
  key order_uuid     : sysuuid_x16 not null;
  order_id           : abap.numc(10);
  description        : abap.char(100);
  status             : abap.char(2);
  created_by         : abap.uname;
  created_at         : timestampl;
  last_changed_by    : abap.uname;
  last_changed_at    : timestampl;
}
```

#### Step 1.2: Create CDS Interface View

**Actions:**
- Create I_ view for data model
- Add associations
- Define compositions
- Add annotations

**CDS Template:**
```abap
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Purchase Order Interface'
define root view entity ZI_PurchaseOrder
  as select from zpurchase_order
  composition [0..*] of ZI_PurchaseOrderItem as _Items
{
  key order_uuid as OrderUUID,
  order_id as OrderID,
  description as Description,
  status as Status,
  _Items
}
```

#### Step 1.3: Create CDS Projection View

**Actions:**
- Create C_ view for UI
- Add UI annotations
- Configure value helps
- Set field properties

**Knowledge:**
- `sap-cap-patterns.json`: CDS patterns

**Outputs:**
- CDS views created
- Associations defined

**Is Mandatory:** Yes

---

### Phase 2: Behavior Definition

**Description:** Define the behavior of the business object.

**Entry Criteria:** CDS model complete  
**Exit Criteria:** Behavior definition created

#### Step 2.1: Create Behavior Definition

**Actions:**
- Define managed/unmanaged scenario
- Set CRUD operations
- Enable draft handling
- Define actions/determinations

**Behavior Template:**
```abap
managed implementation in class zbp_i_purchaseorder unique;
strict ( 2 );
with draft;

define behavior for ZI_PurchaseOrder alias PurchaseOrder
persistent table zpurchase_order
draft table zpurchase_order_d
lock master total etag LastChangedAt
authorization master ( instance )
{
  field ( readonly ) OrderUUID, CreatedBy, CreatedAt;
  field ( mandatory ) Description;

  create;
  update;
  delete;

  draft action Resume;
  draft action Edit;
  draft action Activate;
  draft action Discard;

  action ( features : instance ) submit result [1] $self;
  determination setOrderID on modify { create; }
}
```

**Outputs:**
- Behavior definition
- Draft table

**Is Mandatory:** Yes

---

### Phase 3: Behavior Implementation

**Description:** Implement the business logic.

**Entry Criteria:** Behavior defined  
**Exit Criteria:** Implementation complete

#### Step 3.1: Implement Behavior Pool

**Actions:**
- Create behavior implementation class
- Implement determinations
- Implement validations
- Implement actions

**Implementation Template:**
```abap
CLASS lhc_purchaseorder DEFINITION INHERITING FROM
  cl_abap_behavior_handler.
  PRIVATE SECTION.
    METHODS setOrderID FOR DETERMINE ON MODIFY
      IMPORTING keys FOR PurchaseOrder~setOrderID.
    METHODS submit FOR MODIFY
      IMPORTING keys FOR ACTION PurchaseOrder~submit
      RESULT result.
ENDCLASS.

CLASS lhc_purchaseorder IMPLEMENTATION.
  METHOD setOrderID.
    " Implementation
  ENDMETHOD.
  METHOD submit.
    " Implementation
  ENDMETHOD.
ENDCLASS.
```

#### Step 3.2: Implement Authorization

**Actions:**
- Create authorization control
- Implement instance authorization
- Add field control
- Test authorizations

**Outputs:**
- Behavior implementation
- Authorization control

**Is Mandatory:** Yes

---

### Phase 4: Service Definition

**Description:** Expose the business object as an OData service.

**Entry Criteria:** Behavior implemented  
**Exit Criteria:** Service published

#### Step 4.1: Create Service Definition

**Actions:**
- Define service exposure
- Include entities
- Set alias names

**Service Definition:**
```abap
@EndUserText.label: 'Purchase Order Service'
define service ZUI_PURCHASEORDER_O4 {
  expose ZC_PurchaseOrder as PurchaseOrder;
  expose ZC_PurchaseOrderItem as PurchaseOrderItem;
}
```

#### Step 4.2: Create Service Binding

**Actions:**
- Create OData V4 binding
- Activate service
- Test with /IWFND/V4_ADMIN
- Generate service artifacts

**Outputs:**
- Published OData service

**Is Mandatory:** Yes

---

### Phase 5: Fiori Elements UI

**Description:** Configure the Fiori Elements UI.

**Entry Criteria:** Service published  
**Exit Criteria:** UI configured

#### Step 5.1: Add UI Annotations

**Actions:**
- Configure list report
- Configure object page
- Add value helps
- Set field groups

**UI Annotations:**
```abap
@UI.facet: [
  { id: 'GeneralInfo',
    type: #COLLECTION,
    position: 10 },
  { id: 'OrderDetails',
    parentId: 'GeneralInfo',
    type: #FIELDGROUP_REFERENCE,
    targetQualifier: 'OrderData' }
]

@UI.lineItem: [{ position: 10 }]
@UI.selectionField: [{ position: 10 }]
@UI.fieldGroup: [{ qualifier: 'OrderData', position: 10 }]
OrderID;
```

#### Step 5.2: Create Fiori Launchpad App

**Actions:**
- Register app in catalog
- Configure target mapping
- Set semantic object
- Test in Launchpad

**Outputs:**
- Fiori Elements app
- Launchpad tile

**Is Mandatory:** Yes

---

### Phase 6: Testing & Deployment

**Description:** Test and deploy the RAP application.

**Entry Criteria:** UI configured  
**Exit Criteria:** Deployed to target system

#### Step 6.1: Unit Testing

**Actions:**
- Test CRUD operations
- Test actions
- Test validations
- Test draft handling

#### Step 6.2: Transport & Deploy

**Actions:**
- Release transport request
- Import to quality system
- User acceptance testing
- Import to production

**Outputs:**
- Test results
- Deployed application

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Scenario Type

| Requirement | Scenario |
|-------------|----------|
| Standard CRUD | Managed |
| Legacy tables | Unmanaged |
| Query only | Abstract entity |

### Decision: Draft Handling

| Requirement | Draft |
|-------------|-------|
| Multi-session edit | Enable |
| Simple transactions | Disable |
| Complex approval | Enable with draft actions |

### Decision: UI Approach

| Need | Approach |
|------|----------|
| Standard UI | Fiori Elements |
| Custom UI | Freestyle SAPUI5 |
| Embedded | Extension |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| CDS activation fails | Check syntax and dependencies |
| Behavior implementation error | Use debugger in ADT |
| Service binding fails | Check authorization |
| Fiori preview fails | Clear browser cache |

---

## Example Session

```
User: Create a RAP BO for travel booking

Agent:
━━━ PHASE 1: CDS Data Modeling ━━━
Creating database table...
✓ Created: ztravelbook

Creating interface view...
✓ Created: ZI_TravelBooking

Creating projection view...
✓ Created: ZC_TravelBooking

━━━ PHASE 2: Behavior Definition ━━━
Creating managed behavior...
✓ CRUD operations defined
✓ Draft handling enabled
✓ Actions: approve, reject

━━━ PHASE 3: Implementation ━━━
Implementing behavior pool...
✓ Determination: setBookingID
✓ Validation: validateDates
✓ Action: approve

━━━ PHASE 4: Service Definition ━━━
Creating service...
✓ Service: ZUI_TRAVELBOOKING_O4
✓ Activated and tested

━━━ PHASE 5: Fiori Elements ━━━
Adding UI annotations...
✓ List Report configured
✓ Object Page configured
✓ Value helps added

━━━ PHASE 6: Testing ━━━
Running tests...
✓ All CRUD operations working
✓ Draft handling verified
✓ Actions tested

✨ RAP Business Object complete!
```

---

## Related Artifacts

- **Knowledge**: `knowledge/sap-cap-patterns.json`
- **Blueprints**: `blueprints/sap-rap/blueprint.json`
