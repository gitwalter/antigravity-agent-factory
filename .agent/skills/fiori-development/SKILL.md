---
description: Fiori Elements app creation (List Report, Object Page, Worklist), CDS annotations for UI, value helps, draft-enabled UIs, SAP Fiori Tools usage
---

# Fiori Development

Fiori Elements app creation (List Report, Object Page, Worklist), CDS annotations for UI, value helps, draft-enabled UIs, SAP Fiori Tools usage

## 
# Fiori Development Skill

Create Fiori Elements applications using CDS annotations, configure List Reports, Object Pages, Worklists, and Overview Pages with proper value helps, field groups, and draft support.

## 
# Fiori Development Skill

Create Fiori Elements applications using CDS annotations, configure List Reports, Object Pages, Worklists, and Overview Pages with proper value helps, field groups, and draft support.

## Process
### Step 1: Configure List Report Annotations

```abap
@EndUserText.label: 'Travel Booking Projection'
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
      TotalPrice,
      CurrencyCode,
      Description,
      Status,
      
      /* List Report Annotations */
      @UI: {
        lineItem: [ { 
          position: 10, 
          importance: #HIGH,
          type: #AS_LINK,
          semanticObjectAction: 'display'
        } ],
        identification: [ { 
          position: 10, 
          label: 'Travel ID',
          type: #AS_LINK,
          semanticObjectAction: 'display'
        } ],
        selectionField: [ { position: 10 } ]
      }
      TravelID,
      
      @UI: {
        lineItem: [ { position: 20 } ],
        identification: [ { position: 20 } ],
        fieldGroup: [ { qualifier: 'General', position: 20 } ],
        selectionField: [ { position: 20 } ]
      }
      Description,
      
      @UI: {
        lineItem: [ { 
          position: 30,
          type: #AS_DATETIME,
          formatOptions: { displayMode: #DATE_ONLY }
        } ],
        identification: [ { position: 30 } ],
        fieldGroup: [ { qualifier: 'General', position: 30 } ],
        selectionField: [ { position: 30 } ]
      }
      BeginDate,
      
      @UI: {
        lineItem: [ { 
          position: 40,
          type: #AS_DATETIME,
          formatOptions: { displayMode: #DATE_ONLY }
        } ],
        identification: [ { position: 40 } ],
        fieldGroup: [ { qualifier: 'General', position: 40 } ],
        selectionField: [ { position: 40 } ]
      }
      EndDate,
      
      @UI: {
        lineItem: [ { 
          position: 50,
          type: #AS_NUMERIC,
          unit: CurrencyCode
        } ],
        identification: [ { position: 50 } ],
        fieldGroup: [ { qualifier: 'General', position: 50 } ]
      }
      TotalPrice,
      
      @UI: {
        lineItem: [ { 
          position: 60,
          type: #AS_STATUS,
          criticality: 'StatusCriticality'
        } ],
        identification: [ { position: 60 } ],
        fieldGroup: [ { qualifier: 'General', position: 60 } ],
        selectionField: [ { position: 60 } ]
      }
      Status,
      
      /* Value Helps */
      @Consumption.valueHelpDefinition: [ { 
        entity: { 
          name: 'ZC_Agency', 
          element: 'AgencyID' 
        },
        useForValidation: true
      } ]
      AgencyID,
      
      @Consumption.valueHelpDefinition: [ { 
        entity: { 
          name: 'ZC_Customer', 
          element: 'CustomerID' 
        },
        useForValidation: true
      } ]
      CustomerID
}
```

### Step 2: Configure Object Page Annotations

```abap
@UI: {
  headerInfo: {
    typeName: 'Travel Booking',
    typeNamePlural: 'Travel Bookings',
    title: {
      type: #STANDARD,
      value: 'TravelID'
    },
    description: {
      type: #STANDARD,
      value: 'Description'
    }
  },
  presentationVariant: [ {
    sortOrder: [ {
      by: 'BeginDate',
      direction: #DESC
    } ]
  } ]
}
define view entity ZC_TravelBooking
  as projection on ZI_TravelBooking
{
  // ... fields ...
  
  /* Object Page Facets */
  @UI.facet: [
    {
      id: 'GeneralInfo',
      type: #COLLECTION,
      label: 'General Information',
      position: 10
    },
    {
      id: 'TravelDetails',
      parentId: 'GeneralInfo',
      type: #FIELDGROUP_REFERENCE,
      targetQualifier: 'TravelData',
      label: 'Travel Details',
      position: 10
    },
    {
      id: 'FinancialInfo',
      parentId: 'GeneralInfo',
      type: #FIELDGROUP_REFERENCE,
      targetQualifier: 'FinancialData',
      label: 'Financial Information',
      position: 20
    },
    {
      id: 'Items',
      type: #IDENTIFICATION_REFERENCE,
      targetQualifier: 'Items',
      label: 'Travel Items',
      position: 20
    },
    {
      id: 'StatusInfo',
      type: #FIELDGROUP_REFERENCE,
      targetQualifier: 'StatusData',
      label: 'Status',
      position: 30
    }
  ]
  
  /* Field Groups */
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 10,
    label: 'Travel Details'
  } ]
  TravelID,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 20 
  } ]
  Description,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 30 
  } ]
  AgencyID,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 40 
  } ]
  CustomerID,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 50 
  } ]
  BeginDate,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 60 
  } ]
  EndDate,
  
  @UI.fieldGroup: [ { 
    qualifier: 'FinancialData', 
    position: 10,
    label: 'Financial Information'
  } ]
  BookingFee,
  
  @UI.fieldGroup: [ { 
    qualifier: 'FinancialData', 
    position: 20 
  } ]
  TotalPrice,
  
  @UI.fieldGroup: [ { 
    qualifier: 'FinancialData', 
    position: 30 
  } ]
  CurrencyCode,
  
  @UI.fieldGroup: [ { 
    qualifier: 'StatusData', 
    position: 10,
    label: 'Status'
  } ]
  Status,
  
  @UI.fieldGroup: [ { 
    qualifier: 'StatusData', 
    position: 20 
  } ]
  CreatedBy,
  
  @UI.fieldGroup: [ { 
    qualifier: 'StatusData', 
    position: 30 
  } ]
  CreatedAt
}
```

### Step 3: Configure Actions and Data Actions

```abap
@UI: {
  lineItem: [ { 
    position: 10,
    type: #FOR_ACTION,
    dataAction: 'submit',
    label: 'Submit Booking'
  } ],
  identification: [ { position: 10 } ]
}
TravelID,

@UI: {
  lineItem: [ { 
    position: 20,
    type: #FOR_ACTION,
    dataAction: 'cancel',
    label: 'Cancel Booking'
  } ]
}
Status,

/* Header Actions */
@UI.headerInfo: {
  typeName: 'Travel Booking',
  actions: [
    {
      type: #FOR_ACTION,
      dataAction: 'submit',
      label: 'Submit'
    },
    {
      type: #FOR_ACTION,
      dataAction: 'cancel',
      label: 'Cancel'
    }
  ]
}
```

### Step 4: Configure Value Helps

```abap
/* Simple Value Help */
@Consumption.valueHelpDefinition: [ { 
  entity: { 
    name: 'ZC_Agency', 
    element: 'AgencyID' 
  },
  useForValidation: true
} ]
AgencyID,

/* Value Help with Additional Properties */
@Consumption.valueHelpDefinition: [ { 
  entity: { 
    name: 'ZC_Customer', 
    element: 'CustomerID' 
  },
  additionalBinding: [
    {
      localElement: 'CustomerName',
      element: 'CustomerName',
      usage: #OUTPUT_ONLY
    },
    {
      localElement: 'CustomerEmail',
      element: 'Email',
      usage: #OUTPUT_ONLY
    }
  ],
  useForValidation: true
} ]
CustomerID,

/* Value Help with Filter */
@Consumption.valueHelpDefinition: [ { 
  entity: { 
    name: 'ZC_Material', 
    element: 'MaterialID' 
  },
  filter: {
    materialType: 'SERVICE'
  },
  useForValidation: true
} ]
MaterialID
```

### Step 5: Configure Charts and Analytics

```abap
@UI.chart: [ {
  title: 'Travel Bookings by Status',
  description: 'Distribution of travel bookings',
  chartType: #COLUMN,
  dimensions: [ 'Status' ],
  measures: [ 'TotalPrice' ],
  qualifier: 'StatusChart'
} ]
define view entity ZC_TravelBookingAnalytics
  as projection on ZI_TravelBooking
{
  Status,
  @Aggregation.default: #SUM
  TotalPrice,
  
  @UI.chart: [ {
    qualifier: 'StatusChart',
    dimension: [ 'Status' ],
    measure: [ 'TotalPrice' ]
  } ]
}
```

### Step 6: Configure Draft-Enabled UI

```abap
/* In Behavior Definition */
define behavior for ZI_TravelBooking alias TravelBooking
persistent table ztravelbook
draft table ztravelbook_d
lock master total etag LastChangedAt
with draft
{
  // ... CRUD operations ...
  
  draft action Resume;
  draft action Edit;
  draft action Activate;
  draft action Discard;
}

/* In CDS View - Draft Indicator */
@UI: {
  identification: [ { position: 1 } ],
  headerInfo: {
    typeName: 'Travel Booking',
    typeNamePlural: 'Travel Bookings'
  }
}
%isDraft,
```

### Step 7: Create Fiori Launchpad App

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
      "minUI5Version": "1.120.0",
      "libs": {
        "sap.fe": {}
      }
    },
    "routing": {
      "routes": [
        {
          "pattern": "",
          "name": "TravelBookingList",
          "target": "TravelBookingList"
        },
        {
          "pattern": ":TravelUUID:",
          "name": "TravelBookingObjectPage",
          "target": "TravelBookingObjectPage"
        }
      ],
      "targets": {
        "TravelBookingList": {
          "type": "Component",
          "id": "TravelBookingList",
          "name": "sap.fe.templates.ListReport",
          "options": {
            "settings": {
              "entitySet": "TravelBooking",
              "navigation": {
                "TravelBooking": {
                  "detail": {
                    "route": "TravelBookingObjectPage"
                  }
                }
              }
            }
          }
        },
        "TravelBookingObjectPage": {
          "type": "Component",
          "id": "TravelBookingObjectPage",
          "name": "sap.fe.templates.ObjectPage",
          "options": {
            "settings": {
              "entitySet": "TravelBooking"
            }
          }
        }
      }
    }
  }
}
```

```abap
@EndUserText.label: 'Travel Booking Projection'
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
      TotalPrice,
      CurrencyCode,
      Description,
      Status,
      
      /* List Report Annotations */
      @UI: {
        lineItem: [ { 
          position: 10, 
          importance: #HIGH,
          type: #AS_LINK,
          semanticObjectAction: 'display'
        } ],
        identification: [ { 
          position: 10, 
          label: 'Travel ID',
          type: #AS_LINK,
          semanticObjectAction: 'display'
        } ],
        selectionField: [ { position: 10 } ]
      }
      TravelID,
      
      @UI: {
        lineItem: [ { position: 20 } ],
        identification: [ { position: 20 } ],
        fieldGroup: [ { qualifier: 'General', position: 20 } ],
        selectionField: [ { position: 20 } ]
      }
      Description,
      
      @UI: {
        lineItem: [ { 
          position: 30,
          type: #AS_DATETIME,
          formatOptions: { displayMode: #DATE_ONLY }
        } ],
        identification: [ { position: 30 } ],
        fieldGroup: [ { qualifier: 'General', position: 30 } ],
        selectionField: [ { position: 30 } ]
      }
      BeginDate,
      
      @UI: {
        lineItem: [ { 
          position: 40,
          type: #AS_DATETIME,
          formatOptions: { displayMode: #DATE_ONLY }
        } ],
        identification: [ { position: 40 } ],
        fieldGroup: [ { qualifier: 'General', position: 40 } ],
        selectionField: [ { position: 40 } ]
      }
      EndDate,
      
      @UI: {
        lineItem: [ { 
          position: 50,
          type: #AS_NUMERIC,
          unit: CurrencyCode
        } ],
        identification: [ { position: 50 } ],
        fieldGroup: [ { qualifier: 'General', position: 50 } ]
      }
      TotalPrice,
      
      @UI: {
        lineItem: [ { 
          position: 60,
          type: #AS_STATUS,
          criticality: 'StatusCriticality'
        } ],
        identification: [ { position: 60 } ],
        fieldGroup: [ { qualifier: 'General', position: 60 } ],
        selectionField: [ { position: 60 } ]
      }
      Status,
      
      /* Value Helps */
      @Consumption.valueHelpDefinition: [ { 
        entity: { 
          name: 'ZC_Agency', 
          element: 'AgencyID' 
        },
        useForValidation: true
      } ]
      AgencyID,
      
      @Consumption.valueHelpDefinition: [ { 
        entity: { 
          name: 'ZC_Customer', 
          element: 'CustomerID' 
        },
        useForValidation: true
      } ]
      CustomerID
}
```

```abap
@UI: {
  headerInfo: {
    typeName: 'Travel Booking',
    typeNamePlural: 'Travel Bookings',
    title: {
      type: #STANDARD,
      value: 'TravelID'
    },
    description: {
      type: #STANDARD,
      value: 'Description'
    }
  },
  presentationVariant: [ {
    sortOrder: [ {
      by: 'BeginDate',
      direction: #DESC
    } ]
  } ]
}
define view entity ZC_TravelBooking
  as projection on ZI_TravelBooking
{
  // ... fields ...
  
  /* Object Page Facets */
  @UI.facet: [
    {
      id: 'GeneralInfo',
      type: #COLLECTION,
      label: 'General Information',
      position: 10
    },
    {
      id: 'TravelDetails',
      parentId: 'GeneralInfo',
      type: #FIELDGROUP_REFERENCE,
      targetQualifier: 'TravelData',
      label: 'Travel Details',
      position: 10
    },
    {
      id: 'FinancialInfo',
      parentId: 'GeneralInfo',
      type: #FIELDGROUP_REFERENCE,
      targetQualifier: 'FinancialData',
      label: 'Financial Information',
      position: 20
    },
    {
      id: 'Items',
      type: #IDENTIFICATION_REFERENCE,
      targetQualifier: 'Items',
      label: 'Travel Items',
      position: 20
    },
    {
      id: 'StatusInfo',
      type: #FIELDGROUP_REFERENCE,
      targetQualifier: 'StatusData',
      label: 'Status',
      position: 30
    }
  ]
  
  /* Field Groups */
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 10,
    label: 'Travel Details'
  } ]
  TravelID,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 20 
  } ]
  Description,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 30 
  } ]
  AgencyID,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 40 
  } ]
  CustomerID,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 50 
  } ]
  BeginDate,
  
  @UI.fieldGroup: [ { 
    qualifier: 'TravelData', 
    position: 60 
  } ]
  EndDate,
  
  @UI.fieldGroup: [ { 
    qualifier: 'FinancialData', 
    position: 10,
    label: 'Financial Information'
  } ]
  BookingFee,
  
  @UI.fieldGroup: [ { 
    qualifier: 'FinancialData', 
    position: 20 
  } ]
  TotalPrice,
  
  @UI.fieldGroup: [ { 
    qualifier: 'FinancialData', 
    position: 30 
  } ]
  CurrencyCode,
  
  @UI.fieldGroup: [ { 
    qualifier: 'StatusData', 
    position: 10,
    label: 'Status'
  } ]
  Status,
  
  @UI.fieldGroup: [ { 
    qualifier: 'StatusData', 
    position: 20 
  } ]
  CreatedBy,
  
  @UI.fieldGroup: [ { 
    qualifier: 'StatusData', 
    position: 30 
  } ]
  CreatedAt
}
```

```abap
@UI: {
  lineItem: [ { 
    position: 10,
    type: #FOR_ACTION,
    dataAction: 'submit',
    label: 'Submit Booking'
  } ],
  identification: [ { position: 10 } ]
}
TravelID,

@UI: {
  lineItem: [ { 
    position: 20,
    type: #FOR_ACTION,
    dataAction: 'cancel',
    label: 'Cancel Booking'
  } ]
}
Status,

/* Header Actions */
@UI.headerInfo: {
  typeName: 'Travel Booking',
  actions: [
    {
      type: #FOR_ACTION,
      dataAction: 'submit',
      label: 'Submit'
    },
    {
      type: #FOR_ACTION,
      dataAction: 'cancel',
      label: 'Cancel'
    }
  ]
}
```

```abap
/* Simple Value Help */
@Consumption.valueHelpDefinition: [ { 
  entity: { 
    name: 'ZC_Agency', 
    element: 'AgencyID' 
  },
  useForValidation: true
} ]
AgencyID,

/* Value Help with Additional Properties */
@Consumption.valueHelpDefinition: [ { 
  entity: { 
    name: 'ZC_Customer', 
    element: 'CustomerID' 
  },
  additionalBinding: [
    {
      localElement: 'CustomerName',
      element: 'CustomerName',
      usage: #OUTPUT_ONLY
    },
    {
      localElement: 'CustomerEmail',
      element: 'Email',
      usage: #OUTPUT_ONLY
    }
  ],
  useForValidation: true
} ]
CustomerID,

/* Value Help with Filter */
@Consumption.valueHelpDefinition: [ { 
  entity: { 
    name: 'ZC_Material', 
    element: 'MaterialID' 
  },
  filter: {
    materialType: 'SERVICE'
  },
  useForValidation: true
} ]
MaterialID
```

```abap
@UI.chart: [ {
  title: 'Travel Bookings by Status',
  description: 'Distribution of travel bookings',
  chartType: #COLUMN,
  dimensions: [ 'Status' ],
  measures: [ 'TotalPrice' ],
  qualifier: 'StatusChart'
} ]
define view entity ZC_TravelBookingAnalytics
  as projection on ZI_TravelBooking
{
  Status,
  @Aggregation.default: #SUM
  TotalPrice,
  
  @UI.chart: [ {
    qualifier: 'StatusChart',
    dimension: [ 'Status' ],
    measure: [ 'TotalPrice' ]
  } ]
}
```

```abap
/* In Behavior Definition */
define behavior for ZI_TravelBooking alias TravelBooking
persistent table ztravelbook
draft table ztravelbook_d
lock master total etag LastChangedAt
with draft
{
  // ... CRUD operations ...
  
  draft action Resume;
  draft action Edit;
  draft action Activate;
  draft action Discard;
}

/* In CDS View - Draft Indicator */
@UI: {
  identification: [ { position: 1 } ],
  headerInfo: {
    typeName: 'Travel Booking',
    typeNamePlural: 'Travel Bookings'
  }
}
%isDraft,
```

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
      "minUI5Version": "1.120.0",
      "libs": {
        "sap.fe": {}
      }
    },
    "routing": {
      "routes": [
        {
          "pattern": "",
          "name": "TravelBookingList",
          "target": "TravelBookingList"
        },
        {
          "pattern": ":TravelUUID:",
          "name": "TravelBookingObjectPage",
          "target": "TravelBookingObjectPage"
        }
      ],
      "targets": {
        "TravelBookingList": {
          "type": "Component",
          "id": "TravelBookingList",
          "name": "sap.fe.templates.ListReport",
          "options": {
            "settings": {
              "entitySet": "TravelBooking",
              "navigation": {
                "TravelBooking": {
                  "detail": {
                    "route": "TravelBookingObjectPage"
                  }
                }
              }
            }
          }
        },
        "TravelBookingObjectPage": {
          "type": "Component",
          "id": "TravelBookingObjectPage",
          "name": "sap.fe.templates.ObjectPage",
          "options": {
            "settings": {
              "entitySet": "TravelBooking"
            }
          }
        }
      }
    }
  }
}
```

## Fiori Elements Templates
### List Report
- Standard list with filtering and sorting
- Use for master data and transactional data
- Supports search, filters, and bulk actions

### Object Page
- Detail page for single entity
- Use for editing and viewing details
- Supports tabs, field groups, and sub-objects

### Worklist
- Task-based list
- Use for approval workflows
- Supports task actions and status updates

### Overview Page
- Analytical dashboard
- Use for KPIs and charts
- Supports cards, charts, and tables

## Best Practices
- Use semantic annotations (@EndUserText.label) for all fields
- Configure proper field groups for Object Page organization
- Use value helps for all foreign key fields
- Enable draft handling for complex editing scenarios
- Use proper field types (@UI.type) for better UX
- Configure criticality for status fields
- Use identification annotations for key fields
- Configure proper sorting and filtering
- Use charts for analytical data
- Test service binding before Fiori app development
- Use Page Map editor in Fiori Tools for visual configuration
- Follow Fiori design guidelines

## Anti-Patterns
- Missing value helps for foreign keys (poor UX)
- Not using field groups (disorganized Object Page)
- Missing semantic annotations (poor accessibility)
- Not enabling draft for complex editing (data loss risk)
- Incorrect field types (poor display)
- Missing criticality for status fields (poor visual feedback)
- Not testing service binding first (wasted time)
- Ignoring Fiori design guidelines (inconsistent UX)

## Related
- Skill: `rap-development` - RAP BO creation
- Skill: `cds-modeling` - CDS view creation
- Knowledge: `sap-fiori-patterns.json` - Fiori patterns and annotations

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: sap-fiori-patterns.json
