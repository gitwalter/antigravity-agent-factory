---
description: CDS view creation (basic, composite, consumption), associations, compositions, CDS annotations (semantic, UI, analytics), CDS access control (DCL)
---

# Cds Modeling

CDS view creation (basic, composite, consumption), associations, compositions, CDS annotations (semantic, UI, analytics), CDS access control (DCL)

## 
# CDS Modeling Skill

Create Core Data Services (CDS) views for data modeling, including basic views, composite views, consumption views, associations, compositions, annotations, and access control rules.

## 
# CDS Modeling Skill

Create Core Data Services (CDS) views for data modeling, including basic views, composite views, consumption views, associations, compositions, annotations, and access control rules.

## Process
### Step 1: Create Basic CDS View

```abap
@EndUserText.label: 'Travel Booking View'
@AccessControl.authorizationCheck: #CHECK
define view entity ZI_TravelBooking
  as select from ztravelbook
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      booking_fee as BookingFee,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status,
      created_by as CreatedBy,
      created_at as CreatedAt,
      last_changed_by as LastChangedBy,
      last_changed_at as LastChangedAt
}
```

### Step 2: Create Composite View with Associations

```abap
@EndUserText.label: 'Travel Booking with Associations'
@AccessControl.authorizationCheck: #CHECK
define view entity ZI_TravelBooking
  as select from ztravelbook
  association [0..*] to ZI_TravelBookingItem as _Items 
    on $projection.TravelUUID = _Items.TravelUUID
  association [0..1] to ZI_Agency as _Agency 
    on $projection.AgencyID = _Agency.AgencyID
  association [0..1] to ZI_Customer as _Customer 
    on $projection.CustomerID = _Customer.CustomerID
  association [0..1] to ZI_Currency as _Currency 
    on $projection.CurrencyCode = _Currency.CurrencyCode
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      booking_fee as BookingFee,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status,
      created_by as CreatedBy,
      created_at as CreatedAt,
      last_changed_by as LastChangedBy,
      last_changed_at as LastChangedAt,
      
      /* Associations */
      _Items,
      _Agency {
        AgencyID,
        AgencyName,
        AgencyAddress
      },
      _Customer {
        CustomerID,
        CustomerName,
        CustomerEmail
      },
      _Currency {
        CurrencyCode,
        CurrencyName
      },
      
      /* Calculated Fields */
      @EndUserText.label: 'Duration in Days'
      cast(end_date - begin_date as abap.int4) as DurationInDays,
      
      @EndUserText.label: 'Is Active'
      case 
        when status = 'A' then cast('X' as abap.boolean)
        else cast('' as abap.boolean)
      end as IsActive
}
```

### Step 3: Create Composition (Parent-Child Relationship)

```abap
@EndUserText.label: 'Travel Booking Root'
@AccessControl.authorizationCheck: #CHECK
define root view entity ZI_TravelBooking
  as select from ztravelbook
  composition [0..*] of ZI_TravelBookingItem as _Items
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      booking_fee as BookingFee,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status,
      created_by as CreatedBy,
      created_at as CreatedAt,
      last_changed_by as LastChangedBy,
      last_changed_at as LastChangedAt,
      
      /* Composition */
      _Items
}

@EndUserText.label: 'Travel Booking Item'
@AccessControl.authorizationCheck: #CHECK
define view entity ZI_TravelBookingItem
  as select from ztravelbookitem
  association [0..1] to ZI_TravelBooking as _TravelBooking 
    on $projection.TravelUUID = _TravelBooking.TravelUUID
  association [0..1] to ZI_Material as _Material 
    on $projection.MaterialID = _Material.MaterialID
{
  key travel_uuid as TravelUUID,
  key item_uuid as ItemUUID,
      travel_id as TravelID,
      item_id as ItemID,
      material_id as MaterialID,
      description as Description,
      quantity as Quantity,
      unit as Unit,
      price as Price,
      currency_code as CurrencyCode,
      
      /* Associations */
      _TravelBooking,
      _Material {
        MaterialID,
        MaterialName,
        MaterialDescription
      },
      
      /* Calculated Fields */
      @EndUserText.label: 'Line Total'
      cast(quantity * price as abap.curr(17,2)) as LineTotal
}
```

### Step 4: Create Consumption View with Annotations

```abap
@EndUserText.label: 'Travel Booking Consumption View'
@AccessControl.authorizationCheck: #CHECK
@Metadata.allowExtensions: true
@Search.searchable: true
define view entity ZC_TravelBooking
  as projection on ZI_TravelBooking
{
  key TravelUUID,
      TravelID,
      AgencyID,
      CustomerID,
      BeginDate,
      EndDate,
      BookingFee,
      TotalPrice,
      CurrencyCode,
      Description,
      Status,
      CreatedBy,
      CreatedAt,
      LastChangedBy,
      LastChangedAt,
      DurationInDays,
      IsActive,
      
      /* Associations */
      _Items,
      _Agency,
      _Customer,
      _Currency,
      
      /* Semantic Annotations */
      @Semantics.amount.currencyCode: 'CurrencyCode'
      TotalPrice,
      
      @Semantics.amount.currencyCode: 'CurrencyCode'
      BookingFee,
      
      @Semantics.currencyCode: true
      CurrencyCode,
      
      @Semantics.user.createdBy: true
      CreatedBy,
      
      @Semantics.systemDateTime.createdAt: true
      CreatedAt,
      
      @Semantics.user.lastChangedBy: true
      LastChangedBy,
      
      @Semantics.systemDateTime.lastChangedAt: true
      LastChangedAt,
      
      /* UI Annotations */
      @UI: {
        lineItem: [ { position: 10, importance: #HIGH } ],
        identification: [ { position: 10 } ],
        selectionField: [ { position: 10 } ]
      }
      TravelID,
      
      @UI: {
        lineItem: [ { position: 20 } ],
        identification: [ { position: 20 } ],
        fieldGroup: [ { qualifier: 'General', position: 20 } ]
      }
      Description,
      
      /* Value Helps */
      @Consumption.valueHelpDefinition: [ { 
        entity: { name: 'ZC_Agency', element: 'AgencyID' } 
      } ]
      AgencyID,
      
      @Consumption.valueHelpDefinition: [ { 
        entity: { name: 'ZC_Customer', element: 'CustomerID' } 
      } ]
      CustomerID
}
```

### Step 5: Create CDS Access Control (DCL)

```abap
@EndUserText.label: 'Travel Booking Access Control'
@MappingRole: true
define role ZC_TravelBooking {
  grant select on ZI_TravelBooking
    where ( AgencyID ) = aspect pfcg_auth( ZTRAVELBOOK, AGENCYID, ACTVT = '03' )
       or ( CreatedBy ) = aspect user_filter( CreatedBy );
}
```

### Step 6: Create Abstract Entity

```abap
@EndUserText.label: 'Abstract Travel Booking'
define abstract entity ZA_TravelBooking {
  TravelUUID : sysuuid_x16;
  TravelID : abap.numc(10);
  AgencyID : abap.char(6);
  CustomerID : abap.char(8);
  BeginDate : abap.dats;
  EndDate : abap.dats;
  TotalPrice : abap.curr(17,2);
  CurrencyCode : abap.cuky(5);
  Description : abap.char(255);
  Status : abap.char(1);
}

@EndUserText.label: 'Travel Booking Implementation'
define view entity ZI_TravelBooking
  as projection on ztravelbook
  implements ZA_TravelBooking
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status
}
```

### Step 7: Create Custom Entity

```abap
@EndUserText.label: 'Travel Booking Custom Entity'
define custom entity ZCE_TravelBooking {
  key TravelUUID : sysuuid_x16;
  TravelID : abap.numc(10);
  AgencyID : abap.char(6);
  CustomerID : abap.char(8);
  BeginDate : abap.dats;
  EndDate : abap.dats;
  TotalPrice : abap.curr(17,2);
  CurrencyCode : abap.cuky(5);
  Description : abap.char(255);
  Status : abap.char(1);
}
```

```abap
@EndUserText.label: 'Travel Booking View'
@AccessControl.authorizationCheck: #CHECK
define view entity ZI_TravelBooking
  as select from ztravelbook
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      booking_fee as BookingFee,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status,
      created_by as CreatedBy,
      created_at as CreatedAt,
      last_changed_by as LastChangedBy,
      last_changed_at as LastChangedAt
}
```

```abap
@EndUserText.label: 'Travel Booking with Associations'
@AccessControl.authorizationCheck: #CHECK
define view entity ZI_TravelBooking
  as select from ztravelbook
  association [0..*] to ZI_TravelBookingItem as _Items 
    on $projection.TravelUUID = _Items.TravelUUID
  association [0..1] to ZI_Agency as _Agency 
    on $projection.AgencyID = _Agency.AgencyID
  association [0..1] to ZI_Customer as _Customer 
    on $projection.CustomerID = _Customer.CustomerID
  association [0..1] to ZI_Currency as _Currency 
    on $projection.CurrencyCode = _Currency.CurrencyCode
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      booking_fee as BookingFee,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status,
      created_by as CreatedBy,
      created_at as CreatedAt,
      last_changed_by as LastChangedBy,
      last_changed_at as LastChangedAt,
      
      /* Associations */
      _Items,
      _Agency {
        AgencyID,
        AgencyName,
        AgencyAddress
      },
      _Customer {
        CustomerID,
        CustomerName,
        CustomerEmail
      },
      _Currency {
        CurrencyCode,
        CurrencyName
      },
      
      /* Calculated Fields */
      @EndUserText.label: 'Duration in Days'
      cast(end_date - begin_date as abap.int4) as DurationInDays,
      
      @EndUserText.label: 'Is Active'
      case 
        when status = 'A' then cast('X' as abap.boolean)
        else cast('' as abap.boolean)
      end as IsActive
}
```

```abap
@EndUserText.label: 'Travel Booking Root'
@AccessControl.authorizationCheck: #CHECK
define root view entity ZI_TravelBooking
  as select from ztravelbook
  composition [0..*] of ZI_TravelBookingItem as _Items
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      booking_fee as BookingFee,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status,
      created_by as CreatedBy,
      created_at as CreatedAt,
      last_changed_by as LastChangedBy,
      last_changed_at as LastChangedAt,
      
      /* Composition */
      _Items
}

@EndUserText.label: 'Travel Booking Item'
@AccessControl.authorizationCheck: #CHECK
define view entity ZI_TravelBookingItem
  as select from ztravelbookitem
  association [0..1] to ZI_TravelBooking as _TravelBooking 
    on $projection.TravelUUID = _TravelBooking.TravelUUID
  association [0..1] to ZI_Material as _Material 
    on $projection.MaterialID = _Material.MaterialID
{
  key travel_uuid as TravelUUID,
  key item_uuid as ItemUUID,
      travel_id as TravelID,
      item_id as ItemID,
      material_id as MaterialID,
      description as Description,
      quantity as Quantity,
      unit as Unit,
      price as Price,
      currency_code as CurrencyCode,
      
      /* Associations */
      _TravelBooking,
      _Material {
        MaterialID,
        MaterialName,
        MaterialDescription
      },
      
      /* Calculated Fields */
      @EndUserText.label: 'Line Total'
      cast(quantity * price as abap.curr(17,2)) as LineTotal
}
```

```abap
@EndUserText.label: 'Travel Booking Consumption View'
@AccessControl.authorizationCheck: #CHECK
@Metadata.allowExtensions: true
@Search.searchable: true
define view entity ZC_TravelBooking
  as projection on ZI_TravelBooking
{
  key TravelUUID,
      TravelID,
      AgencyID,
      CustomerID,
      BeginDate,
      EndDate,
      BookingFee,
      TotalPrice,
      CurrencyCode,
      Description,
      Status,
      CreatedBy,
      CreatedAt,
      LastChangedBy,
      LastChangedAt,
      DurationInDays,
      IsActive,
      
      /* Associations */
      _Items,
      _Agency,
      _Customer,
      _Currency,
      
      /* Semantic Annotations */
      @Semantics.amount.currencyCode: 'CurrencyCode'
      TotalPrice,
      
      @Semantics.amount.currencyCode: 'CurrencyCode'
      BookingFee,
      
      @Semantics.currencyCode: true
      CurrencyCode,
      
      @Semantics.user.createdBy: true
      CreatedBy,
      
      @Semantics.systemDateTime.createdAt: true
      CreatedAt,
      
      @Semantics.user.lastChangedBy: true
      LastChangedBy,
      
      @Semantics.systemDateTime.lastChangedAt: true
      LastChangedAt,
      
      /* UI Annotations */
      @UI: {
        lineItem: [ { position: 10, importance: #HIGH } ],
        identification: [ { position: 10 } ],
        selectionField: [ { position: 10 } ]
      }
      TravelID,
      
      @UI: {
        lineItem: [ { position: 20 } ],
        identification: [ { position: 20 } ],
        fieldGroup: [ { qualifier: 'General', position: 20 } ]
      }
      Description,
      
      /* Value Helps */
      @Consumption.valueHelpDefinition: [ { 
        entity: { name: 'ZC_Agency', element: 'AgencyID' } 
      } ]
      AgencyID,
      
      @Consumption.valueHelpDefinition: [ { 
        entity: { name: 'ZC_Customer', element: 'CustomerID' } 
      } ]
      CustomerID
}
```

```abap
@EndUserText.label: 'Travel Booking Access Control'
@MappingRole: true
define role ZC_TravelBooking {
  grant select on ZI_TravelBooking
    where ( AgencyID ) = aspect pfcg_auth( ZTRAVELBOOK, AGENCYID, ACTVT = '03' )
       or ( CreatedBy ) = aspect user_filter( CreatedBy );
}
```

```abap
@EndUserText.label: 'Abstract Travel Booking'
define abstract entity ZA_TravelBooking {
  TravelUUID : sysuuid_x16;
  TravelID : abap.numc(10);
  AgencyID : abap.char(6);
  CustomerID : abap.char(8);
  BeginDate : abap.dats;
  EndDate : abap.dats;
  TotalPrice : abap.curr(17,2);
  CurrencyCode : abap.cuky(5);
  Description : abap.char(255);
  Status : abap.char(1);
}

@EndUserText.label: 'Travel Booking Implementation'
define view entity ZI_TravelBooking
  as projection on ztravelbook
  implements ZA_TravelBooking
{
  key travel_uuid as TravelUUID,
      travel_id as TravelID,
      agency_id as AgencyID,
      customer_id as CustomerID,
      begin_date as BeginDate,
      end_date as EndDate,
      total_price as TotalPrice,
      currency_code as CurrencyCode,
      description as Description,
      status as Status
}
```

```abap
@EndUserText.label: 'Travel Booking Custom Entity'
define custom entity ZCE_TravelBooking {
  key TravelUUID : sysuuid_x16;
  TravelID : abap.numc(10);
  AgencyID : abap.char(6);
  CustomerID : abap.char(8);
  BeginDate : abap.dats;
  EndDate : abap.dats;
  TotalPrice : abap.curr(17,2);
  CurrencyCode : abap.cuky(5);
  Description : abap.char(255);
  Status : abap.char(1);
}
```

## CDS View Types
### Basic View (Interface View)
- Direct mapping to database table
- Use for data model foundation
- Naming: ZI_* (Interface)

### Composite View
- Combines multiple tables/views
- Uses associations and joins
- Use for complex data models

### Consumption View
- Projection of interface view
- Includes UI and semantic annotations
- Use for Fiori Elements apps
- Naming: ZC_* (Consumption)

### Abstract Entity
- Template for multiple implementations
- Use for common structures
- Naming: ZA_* (Abstract)

### Custom Entity
- No database table mapping
- Use for calculated/derived data
- Naming: ZCE_* (Custom Entity)

## Associations vs Compositions
### Associations
- Loose relationship
- Can exist independently
- Use for reference data
- Syntax: `association [0..1] to Entity`

### Compositions
- Strong parent-child relationship
- Child cannot exist without parent
- Use for dependent entities
- Syntax: `composition [0..*] of Entity`

## CDS Annotations
### Semantic Annotations
- `@Semantics.amount.currencyCode` - Amount with currency
- `@Semantics.quantity.unitOfMeasure` - Quantity with unit
- `@Semantics.user.createdBy` - User who created
- `@Semantics.systemDateTime.createdAt` - Creation timestamp
- `@Semantics.currencyCode` - Currency code field

### UI Annotations
- `@UI.lineItem` - List report column
- `@UI.identification` - Object page identification
- `@UI.fieldGroup` - Object page field group
- `@UI.selectionField` - Filter field
- `@UI.chart` - Chart configuration

### Analytics Annotations
- `@Aggregation.default` - Default aggregation (SUM, AVG, etc.)
- `@Analytics.dataCategory` - Data category (DIMENSION, FACT, etc.)
- `@Analytics.dataExtraction.enabled` - Enable data extraction

## Best Practices
- Use semantic annotations for proper field semantics
- Create interface views (I_) before consumption views (C_)
- Use associations for reference data, compositions for dependent data
- Add proper access control (DCL) for security
- Use calculated fields for derived data
- Follow naming conventions (ZI_*, ZC_*, ZA_*, ZCE_*)
- Add proper labels (@EndUserText.label) for all entities
- Use abstract entities for common structures
- Implement proper authorization checks
- Use value helps for foreign key fields
- Add proper semantic annotations for better UX
- Optimize view performance by selecting only needed fields in consumption views
- Use cast() and case expressions for type conversions and conditional logic
- Document complex calculated fields and associations with comments
- Test CDS views with different user roles to verify access control works correctly
- Use @Search.searchable annotation for full-text search capabilities

## Anti-Patterns
- Missing semantic annotations (poor data semantics)
- Not using associations/compositions (poor data model)
- Missing access control (security vulnerability)
- Not following naming conventions (confusion)
- Missing labels (poor maintainability)
- Direct table access instead of CDS views (violates ABAP Cloud)
- Not using abstract entities for common structures (code duplication)
- Missing calculated fields (inefficient queries)

## Related
- Skill: `rap-development` - RAP BO creation with CDS
- Skill: `fiori-development` - Fiori Elements with CDS annotations
- Knowledge: `sap-rap-patterns.json` - CDS patterns and guidelines

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: sap-rap-patterns.json
