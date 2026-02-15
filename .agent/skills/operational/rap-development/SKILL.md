---
description: RAP business object creation (managed, unmanaged, abstract), behavior
  definitions, determinations, validations, actions, draft handling, authorization
  control
name: rap-development
type: skill
---
# Rap Development

RAP business object creation (managed, unmanaged, abstract), behavior definitions, determinations, validations, actions, draft handling, authorization control

Implement RESTful ABAP Programming Model (RAP) business objects with proper behavior definitions, draft handling, authorization, and best practices.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Create Database Table

```abap
@EndUserText.label : 'Travel Booking'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #ALLOWED
define table ztravelbook {
  key client         : abap.clnt not null;
  key travel_uuid    : sysuuid_x16 not null;
  travel_id          : abap.numc(10);
  agency_id          : abap.char(6);
  customer_id        : abap.char(8);
  begin_date         : abap.dats;
  end_date           : abap.dats;
  booking_fee        : abap.curr(17,2);
  total_price        : abap.curr(17,2);
  currency_code      : abap.cuky(5);
  description        : abap.char(255);
  status             : abap.char(1);
  created_by         : abap.uname;
  created_at         : timestampl;
  last_changed_by    : abap.uname;
  last_changed_at    : timestampl;

  @AbapCatalog.foreignKey.keyType : #KEY
  @AbapCatalog.foreignKey.screenCheck : true
  foreign key [0..1,1] zagency
    references zagency
      on delete restrict
      agency_id;
}
```

### Step 2: Create CDS Interface View (I_)

```abap
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Travel Booking Interface'
define root view entity ZI_TravelBooking
  as select from ztravelbook
  composition [0..*] of ZI_TravelBookingItem as _Items
  association [0..1] to ZI_Agency as _Agency on $projection.AgencyID = _Agency.AgencyID
  association [0..1] to ZI_Customer as _Customer on $projection.CustomerID = _Customer.CustomerID
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
      _Agency,
      _Customer,

      /* Calculated fields */
      @EndUserText.label: 'Duration in Days'
      cast(end_date - begin_date as abap.int4) as DurationInDays
}
```

### Step 3: Create CDS Projection View (C_)

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

      /* Associations */
      _Items,
      _Agency,
      _Customer,

      /* UI Annotations */
      @UI: {
        lineItem: [ { position: 10, importance: #HIGH },
                    { type: #FOR_ACTION, dataAction: 'submit', label: 'Submit' } ],
        identification: [ { position: 10, label: 'Travel ID' } ],
        fieldGroup: [ { qualifier: 'General', position: 10 } ],
        selectionField: [ { position: 10 } ]
      }
      TravelID,

      @UI: {
        lineItem: [ { position: 20 } ],
        identification: [ { position: 20 } ],
        fieldGroup: [ { qualifier: 'General', position: 20 } ]
      }
      Description,

      @UI: {
        lineItem: [ { position: 30 } ],
        identification: [ { position: 30 } ],
        fieldGroup: [ { qualifier: 'General', position: 30 } ]
      }
      Status,

      @Consumption.valueHelpDefinition: [ { entity: { name: 'ZC_Agency', element: 'AgencyID' } } ]
      AgencyID,

      @Consumption.valueHelpDefinition: [ { entity: { name: 'ZC_Customer', element: 'CustomerID' } } ]
      CustomerID
}
```

### Step 4: Create Behavior Definition (BDEF)

```abap
managed implementation in class zbp_i_travelbooking unique;
strict ( 2 );
with draft;

define behavior for ZI_TravelBooking alias TravelBooking
persistent table ztravelbook
draft table ztravelbook_d
lock master total etag LastChangedAt
authorization master ( instance )
{
  // Field control
  field ( readonly ) TravelUUID, CreatedBy, CreatedAt;
  field ( mandatory ) AgencyID, CustomerID, BeginDate, EndDate;
  field ( readonly : update ) TravelID;

  // CRUD operations
  create;
  update;
  delete;

  // Draft actions
  draft action Resume;
  draft action Edit;
  draft action Activate;
  draft action Discard;

  // Standard actions
  action ( features : instance ) submit result [1] $self;
  action ( features : instance ) cancel result [1] $self;

  // Determinations
  determination setTravelID on modify { create; }
  determination calculateTotalPrice on modify { create; update; }
  determination validateDates on modify { create; update; }

  // Validations
  validation validateBookingDates on save { create; update; }
  validation validateCustomer on save { create; update; }

  // Side effects
  association _Items { create; update; delete; }
  association _Agency { read; }
  association _Customer { read; }
}

define behavior for ZI_TravelBookingItem alias TravelBookingItem
persistent table ztravelbookitem
draft table ztravelbookitem_d
lock dependent by _TravelBooking
authorization dependent by _TravelBooking
{
  field ( readonly ) TravelUUID, ItemUUID;
  field ( mandatory ) TravelID, Description, Price;

  create;
  update;
  delete;

  association _TravelBooking { create; }
}
```

### Step 5: Implement Behavior Pool

```abap
CLASS lhc_travelbooking DEFINITION INHERITING FROM cl_abap_behavior_handler.
  PRIVATE SECTION.
    METHODS setTravelID FOR DETERMINE ON MODIFY
      IMPORTING keys FOR TravelBooking~setTravelID.
    METHODS calculateTotalPrice FOR DETERMINE ON MODIFY
      IMPORTING keys FOR TravelBooking~calculateTotalPrice.
    METHODS validateDates FOR DETERMINE ON MODIFY
      IMPORTING keys FOR TravelBooking~validateDates.
    METHODS validateBookingDates FOR VALIDATE ON SAVE
      IMPORTING keys FOR TravelBooking~validateBookingDates.
    METHODS validateCustomer FOR VALIDATE ON SAVE
      IMPORTING keys FOR TravelBooking~validateCustomer.
    METHODS submit FOR MODIFY
      IMPORTING keys FOR ACTION TravelBooking~submit
      RESULT result.
    METHODS cancel FOR MODIFY
      IMPORTING keys FOR ACTION TravelBooking~cancel
      RESULT result.
    METHODS get_instance_authorizations FOR INSTANCE AUTHORIZATION
      IMPORTING keys REQUEST requested_authorizations FOR TravelBooking
      RESULT result.
ENDCLASS.

CLASS lhc_travelbooking IMPLEMENTATION.

  METHOD setTravelID.
    " Read travel bookings
    READ ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      FIELDS ( TravelID )
      WITH CORRESPONDING #( keys )
      RESULT DATA(travel_bookings).

    " Get next number
    DATA(number_range) = cl_numberrange_runtime=>number_get(
      exporting
        nr_range_nr = '01'
        object      = 'ZTRAVELBOOK'
        quantity    = lines( travel_bookings )
    ).

    " Update travel bookings
    LOOP AT travel_bookings ASSIGNING FIELD-SYMBOL(<booking>).
      <booking>-TravelID = number_range-number.
      number_range-number = number_range-number + 1.
    ENDLOOP.

    " Modify entities
    MODIFY ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      UPDATE FIELDS ( TravelID )
      WITH CORRESPONDING #( travel_bookings ).
  ENDMETHOD.

  METHOD calculateTotalPrice.
    " Read travel bookings with items
    READ ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(travel_bookings).

    READ ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking BY \_Items
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(items).

    " Calculate total price
    LOOP AT travel_bookings ASSIGNING FIELD-SYMBOL(<booking>).
      DATA(total) = <booking>-BookingFee.
      LOOP AT items INTO DATA(item) WHERE TravelUUID = <booking>-TravelUUID.
        total = total + item-Price.
      ENDLOOP.
      <booking>-TotalPrice = total.
    ENDLOOP.

    " Update entities
    MODIFY ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      UPDATE FIELDS ( TotalPrice )
      WITH CORRESPONDING #( travel_bookings ).
  ENDMETHOD.

  METHOD validateDates.
    " Read travel bookings
    READ ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      FIELDS ( BeginDate EndDate Status )
      WITH CORRESPONDING #( keys )
      RESULT DATA(travel_bookings).

    " Validate dates
    LOOP AT travel_bookings ASSIGNING FIELD-SYMBOL(<booking>).
      IF <booking>-EndDate < <booking>-BeginDate.
        APPEND VALUE #( TravelUUID = <booking>-TravelUUID ) TO failed-travelbooking.
        APPEND VALUE #( TravelUUID = <booking>-TravelUUID
                        %msg = new_message( id = 'ZTRAVELBOOK'
                                           number = '001'
                                           severity = if_abap_behv_message=>severity-error
                                           v1 = |End date must be after begin date| )
                        %element-BeginDate = if_abap_behv=>mk-on
                        %element-EndDate = if_abap_behv=>mk-on ) TO reported-travelbooking.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD validateBookingDates.
    " Similar validation logic
  ENDMETHOD.

  METHOD validateCustomer.
    " Validate customer exists and is active
    READ ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      FIELDS ( CustomerID )
      WITH CORRESPONDING #( keys )
      RESULT DATA(travel_bookings).

    " Check customer
    SELECT SINGLE FROM zcustomer
      FIELDS customer_id
      WHERE customer_id = @<booking>-CustomerID
        AND status = 'A'
      INTO @DATA(customer_exists).

    IF customer_exists IS INITIAL.
      APPEND VALUE #( TravelUUID = <booking>-TravelUUID ) TO failed-travelbooking.
      APPEND VALUE #( TravelUUID = <booking>-TravelUUID
                      %msg = new_message( id = 'ZTRAVELBOOK'
                                         number = '002'
                                         severity = if_abap_behv_message=>severity-error
                                         v1 = |Customer not found or inactive| )
                      %element-CustomerID = if_abap_behv=>mk-on ) TO reported-travelbooking.
    ENDIF.
  ENDMETHOD.

  METHOD submit.
    " Read travel bookings
    READ ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(travel_bookings).

    " Update status
    LOOP AT travel_bookings ASSIGNING FIELD-SYMBOL(<booking>).
      <booking>-Status = 'S'. " Submitted
    ENDLOOP.

    " Modify entities
    MODIFY ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      UPDATE FIELDS ( Status )
      WITH CORRESPONDING #( travel_bookings ).

    " Return result
    result = VALUE #( FOR booking IN travel_bookings
                      ( TravelUUID = booking-TravelUUID
                        %param = booking ) ).
  ENDMETHOD.

  METHOD cancel.
    " Similar to submit, set status to 'C' (Cancelled)
  ENDMETHOD.

  METHOD get_instance_authorizations.
    " Implement instance-level authorization checks
    READ ENTITIES OF ZI_TravelBooking IN LOCAL MODE
      ENTITY TravelBooking
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(travel_bookings).

    LOOP AT travel_bookings INTO DATA(booking).
      " Check authorization
      AUTHORITY-CHECK OBJECT 'ZTRAVELBOOK'
        ID 'ACTVT' FIELD '02'
        ID 'AGENCYID' FIELD booking-AgencyID.

      IF sy-subrc = 0.
        result = VALUE #( ( TravelUUID = booking-TravelUUID
                           %update = if_abap_behv=>auth-allowed
                           %delete = if_abap_behv=>auth-allowed
                           %action-submit = if_abap_behv=>auth-allowed ) ).
      ELSE.
        result = VALUE #( ( TravelUUID = booking-TravelUUID
                           %update = if_abap_behv=>auth-unauthorized
                           %delete = if_abap_behv=>auth-unauthorized
                           %action-submit = if_abap_behv=>auth-unauthorized ) ).
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.
```

### Step 6: Create Draft Table

```abap
@EndUserText.label : 'Travel Booking Draft'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
define table ztravelbook_d {
  key client         : abap.clnt not null;
  key travel_uuid    : sysuuid_x16 not null;
  %is_draft          : abap.boolean;
  travel_id          : abap.numc(10);
  agency_id          : abap.char(6);
  customer_id        : abap.char(8);
  begin_date         : abap.dats;
  end_date           : abap.dats;
  booking_fee        : abap.curr(17,2);
  total_price        : abap.curr(17,2);
  currency_code      : abap.cuky(5);
  description        : abap.char(255);
  status             : abap.char(1);
  created_by         : abap.uname;
  created_at         : timestampl;
  last_changed_by    : abap.uname;
  last_changed_at    : timestampl;
  %prep_action       : abap.char(10);
  %action            : abap.char(10);
  %control-travel_id : abap.int1;
  %control-agency_id : abap.int1;
  %control-customer_id : abap.int1;
  %control-begin_date : abap.int1;
  %control-end_date : abap.int1;
  %control-booking_fee : abap.int1;
  %control-total_price : abap.int1;
  %control-currency_code : abap.int1;
  %control-description : abap.int1;
  %control-status : abap.int1;
}
```

### Step 7: Create Service Definition and Binding

```abap
@EndUserText.label: 'Travel Booking Service'
define service ZUI_TRAVELBOOKING_O4 {
  expose ZC_TravelBooking as TravelBooking;
  expose ZC_TravelBookingItem as TravelBookingItem;
}
```

## RAP Scenarios

### Managed Scenario
- Framework handles CRUD operations automatically
- Use when creating new business objects
- Best for standard CRUD operations

### Unmanaged Scenario
- Developer implements all CRUD operations
- Use when working with legacy tables
- More control but more code

### Abstract Entity Scenario
- Read-only scenario
- Use for reporting and analytics
- No persistent data

## Best Practices

- Always use managed BOs unless legacy tables require unmanaged
- Enable draft handling for complex multi-step processes
- Use total ETag (LastChangedAt) for optimistic locking
- Implement instance-level authorization for sensitive data
- Use determinations for calculated fields and side effects
- Use validations for business rule enforcement
- Use actions for complex operations (approval workflows)
- Follow naming conventions: ZI_ for interface, ZC_ for consumption
- Use semantic annotations (@EndUserText.label) for all entities
- Implement proper error handling with messages
- Use associations for related data
- Configure proper field control (readonly, mandatory)
- Use lock master/dependent for proper concurrency control in parent-child relationships
- Implement side effects to update related entities when parent changes
- Test behavior implementations with different user roles and authorization scenarios
- Use draft actions (Resume, Edit, Activate, Discard) for better user experience
- Configure proper field control timing (readonly on create vs update)

## Anti-Patterns

- Using unmanaged when managed would work (adds unnecessary complexity)
- Missing draft handling for complex processes (causes concurrency issues)
- Not using ETag for optimistic locking (causes data loss)
- Missing authorization checks (security vulnerability)
- Hardcoding values instead of using determinations
- Not implementing proper error messages
- Missing field control annotations
- Not using associations for related data

## Related

- Skill: `fiori-development` - Fiori Elements UI configuration
- Skill: `cds-modeling` - CDS view creation
- Skill: `sap-security` - Authorization and security patterns
- Knowledge: `sap-rap-patterns.json` - RAP patterns and guidelines

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
