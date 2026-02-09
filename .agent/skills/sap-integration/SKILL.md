---
description: CPI iFlow design patterns (content-based routing, splitter, aggregator), Groovy script patterns, API Management policies, Event Mesh topic design, OData consumption
---

# Sap Integration

CPI iFlow design patterns (content-based routing, splitter, aggregator), Groovy script patterns, API Management policies, Event Mesh topic design, OData consumption

## 
# SAP Integration Skill

Design and implement SAP integration solutions using Cloud Platform Integration (CPI), API Management, Event Mesh, and OData consumption patterns.

## 
# SAP Integration Skill

Design and implement SAP integration solutions using Cloud Platform Integration (CPI), API Management, Event Mesh, and OData consumption patterns.

## Process
### Step 1: Create CPI iFlow - Content-Based Routing

```groovy
// Content-Based Router Script
import com.sap.gateway.ip.core.customdev.util.Message
import java.util.HashMap

def Message processData(Message message) {
    def body = message.getBody(java.lang.String)
    def messageLog = messageLogFactory.getMessageLog(message)
    
    // Parse message
    def xml = new XmlSlurper().parseText(body)
    def orderType = xml.OrderType.text()
    
    // Route based on content
    if (orderType == 'STANDARD') {
        message.setProperty('Route', 'StandardOrderChannel')
        messageLog.addAttachmentAsString('Routing', 'Routed to Standard Order Channel', 'text/plain')
    } else if (orderType == 'EXPRESS') {
        message.setProperty('Route', 'ExpressOrderChannel')
        messageLog.addAttachmentAsString('Routing', 'Routed to Express Order Channel', 'text/plain')
    } else {
        message.setProperty('Route', 'DefaultChannel')
        messageLog.addAttachmentAsString('Routing', 'Routed to Default Channel', 'text/plain')
    }
    
    return message
}
```

### Step 2: Create Groovy Script for Message Transformation

```groovy
// Message Transformation Script
import com.sap.gateway.ip.core.customdev.util.Message
import groovy.xml.XmlUtil
import groovy.json.JsonBuilder
import groovy.json.JsonSlurper

def Message processData(Message message) {
    def body = message.getBody(java.lang.String)
    def messageLog = messageLogFactory.getMessageLog(message)
    
    try {
        // Parse XML input
        def xml = new XmlSlurper().parseText(body)
        
        // Transform to JSON
        def json = [
            orderId: xml.OrderID.text(),
            customerId: xml.CustomerID.text(),
            orderDate: xml.OrderDate.text(),
            items: xml.Items.Item.collect { item ->
                [
                    itemId: item.ItemID.text(),
                    quantity: item.Quantity.text() as Integer,
                    price: item.Price.text() as BigDecimal,
                    description: item.Description.text()
                ]
            },
            totalAmount: xml.TotalAmount.text() as BigDecimal,
            currency: xml.Currency.text()
        ]
        
        // Convert to JSON string
        def jsonBuilder = new JsonBuilder(json)
        def jsonString = jsonBuilder.toPrettyString()
        
        // Set output
        message.setBody(jsonString)
        message.setHeader('Content-Type', 'application/json')
        
        messageLog.addAttachmentAsString('Transformation', 'XML to JSON transformation successful', 'text/plain')
        
    } catch (Exception e) {
        messageLog.addAttachmentAsString('Error', "Transformation error: ${e.message}", 'text/plain')
        throw new Exception("Transformation failed: ${e.message}", e)
    }
    
    return message
}
```

### Step 3: Create Splitter Pattern

```groovy
// Splitter Script - Split Order into Individual Items
import com.sap.gateway.ip.core.customdev.util.Message
import groovy.xml.XmlUtil

def Message processData(Message message) {
    def body = message.getBody(java.lang.String)
    def xml = new XmlSlurper().parseText(body)
    
    // Get order header
    def orderHeader = [
        orderId: xml.OrderID.text(),
        customerId: xml.CustomerID.text(),
        orderDate: xml.OrderDate.text()
    ]
    
    // Split items
    def items = xml.Items.Item.collect { item ->
        def itemXml = """
            <OrderItem>
                <OrderID>${orderHeader.orderId}</OrderID>
                <CustomerID>${orderHeader.customerId}</CustomerID>
                <OrderDate>${orderHeader.orderDate}</OrderDate>
                <ItemID>${item.ItemID.text()}</ItemID>
                <Quantity>${item.Quantity.text()}</Quantity>
                <Price>${item.Price.text()}</Price>
                <Description>${item.Description.text()}</Description>
            </OrderItem>
        """
        return itemXml
    }
    
    // Store items for aggregation
    message.setProperty('SplitItems', items.join('|'))
    message.setProperty('ItemCount', items.size().toString())
    
    return message
}
```

### Step 4: Create Aggregator Pattern

```groovy
// Aggregator Script - Combine Split Items
import com.sap.gateway.ip.core.customdev.util.Message
import groovy.xml.XmlUtil

def Message processData(Message message) {
    def splitItems = message.getProperty('SplitItems')
    def itemCount = message.getProperty('ItemCount') as Integer
    
    if (splitItems && itemCount > 0) {
        def items = splitItems.split('\\|')
        
        // Build aggregated XML
        def aggregatedXml = new groovy.xml.StreamingMarkupBuilder().bind {
            Order {
                OrderID(items[0].OrderID.text())
                CustomerID(items[0].CustomerID.text())
                OrderDate(items[0].OrderDate.text())
                Items {
                    items.each { itemXml ->
                        def item = new XmlSlurper().parseText(itemXml)
                        Item {
                            ItemID(item.ItemID.text())
                            Quantity(item.Quantity.text())
                            Price(item.Price.text())
                            Description(item.Description.text())
                        }
                    }
                }
            }
        }
        
        message.setBody(XmlUtil.serialize(aggregatedXml))
    }
    
    return message
}
```

### Step 5: Create Error Handling and Retry

```groovy
// Error Handler Script
import com.sap.gateway.ip.core.customdev.util.Message

def Message processData(Message message) {
    def exception = message.getProperty('CamelExceptionCaught')
    def messageLog = messageLogFactory.getMessageLog(message)
    
    if (exception) {
        def errorDetails = [
            timestamp: new Date().toString(),
            errorMessage: exception.message,
            errorClass: exception.class.name,
            exchangeId: message.getExchange().getExchangeId(),
            retryCount: message.getProperty('RetryCount') ?: '0'
        ]
        
        messageLog.addAttachmentAsString('Error', 
            "Error occurred: ${errorDetails.errorMessage}\n" +
            "Class: ${errorDetails.errorClass}\n" +
            "Retry Count: ${errorDetails.retryCount}",
            'text/plain')
        
        // Check retry count
        def retryCount = (errorDetails.retryCount as Integer) ?: 0
        if (retryCount < 3) {
            // Retry
            message.setProperty('RetryCount', (retryCount + 1).toString())
            message.setProperty('Retry', 'true')
        } else {
            // Send to dead letter queue
            message.setProperty('Retry', 'false')
            message.setProperty('DeadLetter', 'true')
        }
    }
    
    return message
}
```

### Step 6: API Management Policy Configuration

```xml
<!-- API Proxy Policy: Spike Arrest -->
<SpikeArrest async="false" continueOnError="false" enabled="true" name="SpikeArrest-1">
    <DisplayName>Spike Arrest</DisplayName>
    <Properties>
        <Property name="spikeArrest">100ps</Property>
        <Property name="useEffectiveCount">false</Property>
    </Properties>
</SpikeArrest>

<!-- API Proxy Policy: Quota -->
<Quota async="false" continueOnError="false" enabled="true" name="Quota-1" type="calendar">
    <DisplayName>Quota</DisplayName>
    <Properties>
        <Property name="interval">1</Property>
        <Property name="timeUnit">day</Property>
        <Property name="allow">10000</Property>
    </Properties>
</Quota>

<!-- API Proxy Policy: OAuth 2.0 -->
<OAuthV2 async="false" continueOnError="false" enabled="true" name="OAuthV2-1">
    <DisplayName>OAuth 2.0</DisplayName>
    <Properties>
        <Property name="operation">VerifyAccessToken</Property>
        <Property name="publicKey">public_key</Property>
    </Properties>
</OAuthV2>

<!-- API Proxy Policy: Caching -->
<ResponseCache async="false" continueOnError="false" enabled="true" name="ResponseCache-1">
    <DisplayName>Response Cache</DisplayName>
    <Properties>
        <Property name="cacheKey">
            <KeyFragment ref="request.uri" />
            <KeyFragment ref="request.queryparam.id" />
        </Property>
        <Property name="timeToLiveInSeconds">300</Property>
    </Properties>
</ResponseCache>
```

### Step 7: Event Mesh Topic Configuration

```json
{
  "topic": "salesorder/created",
  "description": "Sales order created event",
  "schema": {
    "type": "object",
    "properties": {
      "orderId": {
        "type": "string",
        "description": "Sales order ID"
      },
      "customerId": {
        "type": "string",
        "description": "Customer ID"
      },
      "orderDate": {
        "type": "string",
        "format": "date-time",
        "description": "Order creation date"
      },
      "totalAmount": {
        "type": "number",
        "description": "Total order amount"
      },
      "currency": {
        "type": "string",
        "description": "Currency code"
      }
    },
    "required": ["orderId", "customerId", "orderDate"]
  }
}
```

### Step 8: Event Mesh Subscription

```json
{
  "subscription": {
    "name": "salesorder-created-subscription",
    "topic": "salesorder/created",
    "queue": "salesorder-queue",
    "options": {
      "qos": 1,
      "retain": false
    },
    "filters": [
      {
        "field": "customerId",
        "operator": "eq",
        "value": "CUSTOMER001"
      }
    ]
  }
}
```

### Step 9: OData Service Consumption

```javascript
// OData Client Consumption
const axios = require('axios');

class ODataClient {
    constructor(baseUrl, auth) {
        this.baseUrl = baseUrl;
        this.auth = auth;
        this.client = axios.create({
            baseURL: baseUrl,
            headers: {
                'Authorization': `Bearer ${auth.token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
    }
    
    async getEntitySet(entitySet, options = {}) {
        try {
            const params = {
                $top: options.top || 100,
                $skip: options.skip || 0,
                $filter: options.filter,
                $orderby: options.orderby,
                $select: options.select
            };
            
            const response = await this.client.get(`/${entitySet}`, { params });
            return response.data.value;
        } catch (error) {
            console.error(`Error fetching ${entitySet}:`, error);
            throw error;
        }
    }
    
    async getEntity(entitySet, key, options = {}) {
        try {
            const params = {
                $select: options.select
            };
            
            const response = await this.client.get(`/${entitySet}(${key})`, { params });
            return response.data;
        } catch (error) {
            console.error(`Error fetching ${entitySet}(${key}):`, error);
            throw error;
        }
    }
    
    async createEntity(entitySet, data) {
        try {
            const response = await this.client.post(`/${entitySet}`, data);
            return response.data;
        } catch (error) {
            console.error(`Error creating ${entitySet}:`, error);
            throw error;
        }
    }
    
    async updateEntity(entitySet, key, data) {
        try {
            const response = await this.client.patch(`/${entitySet}(${key})`, data);
            return response.data;
        } catch (error) {
            console.error(`Error updating ${entitySet}(${key}):`, error);
            throw error;
        }
    }
    
    async deleteEntity(entitySet, key) {
        try {
            await this.client.delete(`/${entitySet}(${key})`);
            return true;
        } catch (error) {
            console.error(`Error deleting ${entitySet}(${key}):`, error);
            throw error;
        }
    }
}

// Usage
const client = new ODataClient('https://api.example.com/odata/v4', { token: 'access_token' });
const orders = await client.getEntitySet('SalesOrders', { $filter: "Status eq 'Open'" });
```

```groovy
// Content-Based Router Script
import com.sap.gateway.ip.core.customdev.util.Message
import java.util.HashMap

def Message processData(Message message) {
    def body = message.getBody(java.lang.String)
    def messageLog = messageLogFactory.getMessageLog(message)
    
    // Parse message
    def xml = new XmlSlurper().parseText(body)
    def orderType = xml.OrderType.text()
    
    // Route based on content
    if (orderType == 'STANDARD') {
        message.setProperty('Route', 'StandardOrderChannel')
        messageLog.addAttachmentAsString('Routing', 'Routed to Standard Order Channel', 'text/plain')
    } else if (orderType == 'EXPRESS') {
        message.setProperty('Route', 'ExpressOrderChannel')
        messageLog.addAttachmentAsString('Routing', 'Routed to Express Order Channel', 'text/plain')
    } else {
        message.setProperty('Route', 'DefaultChannel')
        messageLog.addAttachmentAsString('Routing', 'Routed to Default Channel', 'text/plain')
    }
    
    return message
}
```

```groovy
// Message Transformation Script
import com.sap.gateway.ip.core.customdev.util.Message
import groovy.xml.XmlUtil
import groovy.json.JsonBuilder
import groovy.json.JsonSlurper

def Message processData(Message message) {
    def body = message.getBody(java.lang.String)
    def messageLog = messageLogFactory.getMessageLog(message)
    
    try {
        // Parse XML input
        def xml = new XmlSlurper().parseText(body)
        
        // Transform to JSON
        def json = [
            orderId: xml.OrderID.text(),
            customerId: xml.CustomerID.text(),
            orderDate: xml.OrderDate.text(),
            items: xml.Items.Item.collect { item ->
                [
                    itemId: item.ItemID.text(),
                    quantity: item.Quantity.text() as Integer,
                    price: item.Price.text() as BigDecimal,
                    description: item.Description.text()
                ]
            },
            totalAmount: xml.TotalAmount.text() as BigDecimal,
            currency: xml.Currency.text()
        ]
        
        // Convert to JSON string
        def jsonBuilder = new JsonBuilder(json)
        def jsonString = jsonBuilder.toPrettyString()
        
        // Set output
        message.setBody(jsonString)
        message.setHeader('Content-Type', 'application/json')
        
        messageLog.addAttachmentAsString('Transformation', 'XML to JSON transformation successful', 'text/plain')
        
    } catch (Exception e) {
        messageLog.addAttachmentAsString('Error', "Transformation error: ${e.message}", 'text/plain')
        throw new Exception("Transformation failed: ${e.message}", e)
    }
    
    return message
}
```

```groovy
// Splitter Script - Split Order into Individual Items
import com.sap.gateway.ip.core.customdev.util.Message
import groovy.xml.XmlUtil

def Message processData(Message message) {
    def body = message.getBody(java.lang.String)
    def xml = new XmlSlurper().parseText(body)
    
    // Get order header
    def orderHeader = [
        orderId: xml.OrderID.text(),
        customerId: xml.CustomerID.text(),
        orderDate: xml.OrderDate.text()
    ]
    
    // Split items
    def items = xml.Items.Item.collect { item ->
        def itemXml = """
            <OrderItem>
                <OrderID>${orderHeader.orderId}</OrderID>
                <CustomerID>${orderHeader.customerId}</CustomerID>
                <OrderDate>${orderHeader.orderDate}</OrderDate>
                <ItemID>${item.ItemID.text()}</ItemID>
                <Quantity>${item.Quantity.text()}</Quantity>
                <Price>${item.Price.text()}</Price>
                <Description>${item.Description.text()}</Description>
            </OrderItem>
        """
        return itemXml
    }
    
    // Store items for aggregation
    message.setProperty('SplitItems', items.join('|'))
    message.setProperty('ItemCount', items.size().toString())
    
    return message
}
```

```groovy
// Aggregator Script - Combine Split Items
import com.sap.gateway.ip.core.customdev.util.Message
import groovy.xml.XmlUtil

def Message processData(Message message) {
    def splitItems = message.getProperty('SplitItems')
    def itemCount = message.getProperty('ItemCount') as Integer
    
    if (splitItems && itemCount > 0) {
        def items = splitItems.split('\\|')
        
        // Build aggregated XML
        def aggregatedXml = new groovy.xml.StreamingMarkupBuilder().bind {
            Order {
                OrderID(items[0].OrderID.text())
                CustomerID(items[0].CustomerID.text())
                OrderDate(items[0].OrderDate.text())
                Items {
                    items.each { itemXml ->
                        def item = new XmlSlurper().parseText(itemXml)
                        Item {
                            ItemID(item.ItemID.text())
                            Quantity(item.Quantity.text())
                            Price(item.Price.text())
                            Description(item.Description.text())
                        }
                    }
                }
            }
        }
        
        message.setBody(XmlUtil.serialize(aggregatedXml))
    }
    
    return message
}
```

```groovy
// Error Handler Script
import com.sap.gateway.ip.core.customdev.util.Message

def Message processData(Message message) {
    def exception = message.getProperty('CamelExceptionCaught')
    def messageLog = messageLogFactory.getMessageLog(message)
    
    if (exception) {
        def errorDetails = [
            timestamp: new Date().toString(),
            errorMessage: exception.message,
            errorClass: exception.class.name,
            exchangeId: message.getExchange().getExchangeId(),
            retryCount: message.getProperty('RetryCount') ?: '0'
        ]
        
        messageLog.addAttachmentAsString('Error', 
            "Error occurred: ${errorDetails.errorMessage}\n" +
            "Class: ${errorDetails.errorClass}\n" +
            "Retry Count: ${errorDetails.retryCount}",
            'text/plain')
        
        // Check retry count
        def retryCount = (errorDetails.retryCount as Integer) ?: 0
        if (retryCount < 3) {
            // Retry
            message.setProperty('RetryCount', (retryCount + 1).toString())
            message.setProperty('Retry', 'true')
        } else {
            // Send to dead letter queue
            message.setProperty('Retry', 'false')
            message.setProperty('DeadLetter', 'true')
        }
    }
    
    return message
}
```

```xml
<!-- API Proxy Policy: Spike Arrest -->
<SpikeArrest async="false" continueOnError="false" enabled="true" name="SpikeArrest-1">
    <DisplayName>Spike Arrest</DisplayName>
    <Properties>
        <Property name="spikeArrest">100ps</Property>
        <Property name="useEffectiveCount">false</Property>
    </Properties>
</SpikeArrest>

<!-- API Proxy Policy: Quota -->
<Quota async="false" continueOnError="false" enabled="true" name="Quota-1" type="calendar">
    <DisplayName>Quota</DisplayName>
    <Properties>
        <Property name="interval">1</Property>
        <Property name="timeUnit">day</Property>
        <Property name="allow">10000</Property>
    </Properties>
</Quota>

<!-- API Proxy Policy: OAuth 2.0 -->
<OAuthV2 async="false" continueOnError="false" enabled="true" name="OAuthV2-1">
    <DisplayName>OAuth 2.0</DisplayName>
    <Properties>
        <Property name="operation">VerifyAccessToken</Property>
        <Property name="publicKey">public_key</Property>
    </Properties>
</OAuthV2>

<!-- API Proxy Policy: Caching -->
<ResponseCache async="false" continueOnError="false" enabled="true" name="ResponseCache-1">
    <DisplayName>Response Cache</DisplayName>
    <Properties>
        <Property name="cacheKey">
            <KeyFragment ref="request.uri" />
            <KeyFragment ref="request.queryparam.id" />
        </Property>
        <Property name="timeToLiveInSeconds">300</Property>
    </Properties>
</ResponseCache>
```

```json
{
  "topic": "salesorder/created",
  "description": "Sales order created event",
  "schema": {
    "type": "object",
    "properties": {
      "orderId": {
        "type": "string",
        "description": "Sales order ID"
      },
      "customerId": {
        "type": "string",
        "description": "Customer ID"
      },
      "orderDate": {
        "type": "string",
        "format": "date-time",
        "description": "Order creation date"
      },
      "totalAmount": {
        "type": "number",
        "description": "Total order amount"
      },
      "currency": {
        "type": "string",
        "description": "Currency code"
      }
    },
    "required": ["orderId", "customerId", "orderDate"]
  }
}
```

```json
{
  "subscription": {
    "name": "salesorder-created-subscription",
    "topic": "salesorder/created",
    "queue": "salesorder-queue",
    "options": {
      "qos": 1,
      "retain": false
    },
    "filters": [
      {
        "field": "customerId",
        "operator": "eq",
        "value": "CUSTOMER001"
      }
    ]
  }
}
```

```javascript
// OData Client Consumption
const axios = require('axios');

class ODataClient {
    constructor(baseUrl, auth) {
        this.baseUrl = baseUrl;
        this.auth = auth;
        this.client = axios.create({
            baseURL: baseUrl,
            headers: {
                'Authorization': `Bearer ${auth.token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
    }
    
    async getEntitySet(entitySet, options = {}) {
        try {
            const params = {
                $top: options.top || 100,
                $skip: options.skip || 0,
                $filter: options.filter,
                $orderby: options.orderby,
                $select: options.select
            };
            
            const response = await this.client.get(`/${entitySet}`, { params });
            return response.data.value;
        } catch (error) {
            console.error(`Error fetching ${entitySet}:`, error);
            throw error;
        }
    }
    
    async getEntity(entitySet, key, options = {}) {
        try {
            const params = {
                $select: options.select
            };
            
            const response = await this.client.get(`/${entitySet}(${key})`, { params });
            return response.data;
        } catch (error) {
            console.error(`Error fetching ${entitySet}(${key}):`, error);
            throw error;
        }
    }
    
    async createEntity(entitySet, data) {
        try {
            const response = await this.client.post(`/${entitySet}`, data);
            return response.data;
        } catch (error) {
            console.error(`Error creating ${entitySet}:`, error);
            throw error;
        }
    }
    
    async updateEntity(entitySet, key, data) {
        try {
            const response = await this.client.patch(`/${entitySet}(${key})`, data);
            return response.data;
        } catch (error) {
            console.error(`Error updating ${entitySet}(${key}):`, error);
            throw error;
        }
    }
    
    async deleteEntity(entitySet, key) {
        try {
            await this.client.delete(`/${entitySet}(${key})`);
            return true;
        } catch (error) {
            console.error(`Error deleting ${entitySet}(${key}):`, error);
            throw error;
        }
    }
}

// Usage
const client = new ODataClient('https://api.example.com/odata/v4', { token: 'access_token' });
const orders = await client.getEntitySet('SalesOrders', { $filter: "Status eq 'Open'" });
```

## Integration Patterns
### Content-Based Routing
- Route messages based on content
- Use for conditional processing
- Implement with Groovy scripts

### Splitter-Aggregator
- Split large messages into smaller parts
- Process parts independently
- Aggregate results

### Request-Reply
- Synchronous request-response pattern
- Use for real-time integration
- Implement with request/reply channels

### Publish-Subscribe
- Event-driven pattern
- Use Event Mesh for decoupling
- Multiple consumers per event

### Error Handling
- Retry mechanisms
- Dead letter queues
- Error notifications
- Exception subprocesses

## Best Practices
- Use content-based routing for conditional processing
- Implement proper error handling with retries
- Use Groovy scripts for complex transformations
- Configure proper security (OAuth, certificates)
- Use Event Mesh for decoupled architectures
- Implement idempotency for message processing
- Use API Management for external APIs
- Configure proper logging and monitoring
- Use message mapping for simple transformations
- Implement proper credential management
- Use splitter/aggregator for batch processing
- Configure proper timeout and retry policies

## Anti-Patterns
- Hardcoding credentials (use secure stores)
- Missing error handling (always implement exception subprocesses)
- Not using idempotency (can cause duplicate processing)
- Over-complex Groovy scripts (break into smaller functions)
- Missing security configuration (always use OAuth/authentication)
- Not implementing retry mechanisms (can cause message loss)
- Using synchronous calls when async would be better
- Missing monitoring and logging (makes troubleshooting difficult)
- Not using API Management for external APIs
- Ignoring timeout configurations

## Related
- Skill: `sap-security` - Security and authentication patterns
- Knowledge: `sap-event-mesh.json` - Event Mesh patterns
- Knowledge: `sap-api-management.json` - API Management patterns

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: sap-event-mesh.json, sap-api-management.json
