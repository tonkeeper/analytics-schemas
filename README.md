# Analytics Schemas

This repository contains JSON Schema definitions for analytics events, organized into base properties and event-specific schemas.

## Architecture

### `_main.schema.json` - Base Event Properties
Contains the base `AnalyticsEvent` schema with fields that are **required for ALL events**. These properties should be abstracted out in your application code and automatically included with every analytics event.

**Base Properties:**
- `timestamp` - ISO 8601 timestamp when the event was recorded
- `eventName` - The name of the analytics event
- `systemProps` - System-level properties (locale, debug mode, app version, SDK version)
- `props` - Event properties including OS name
- `sessionId` - Session identifier
- `firebase_user_id` - Firebase user identifier (optional)
- `user_properties` - User-specific properties (application, wallet type, network, etc.)

### Event Schemas - Event-Specific Properties
Individual schema files (like `dapp-browser.schema.json`) contain the specific properties for each event type.

**Example Events:**
- `DappBrowserOpen` - When a dapp browser is opened
- `DappPin` - When a dapp is pinned
- `DappClick` - When a dapp is clicked
- etc.

### How to add a new event

1. Add a new schema file in the `schemas` directory.
2. Add the new schema to the `index.json` file.

## Usage in Code

### ✅ Recommended Approach
Abstract the base properties in your analytics service:

```typescript
class AnalyticsService {
  private getBaseProperties(): BaseAnalyticsEvent {
    return {
      timestamp: new Date().toISOString(),
      systemProps: {
        locale: this.getBrowserLocale(),
        isDebug: this.isDebug,
        appVersion: this.appVersion,
        sdkVersion: 'custom_0.0.1'
      },
      props: {
        osName: this.getOSName()
      },
      sessionId: this.sessionId,
      firebase_user_id: this.firebaseUserId,
      user_properties: {
        application: 'wallet-app',
        walletType: this.walletType,
        network: this.network,
        accounts: this.accountCount,
        version: this.version,
        platform: this.platform
      }
    };
  }

  trackDappPin(url: string, location: string) {
    const event = {
      ...this.getBaseProperties(),
      eventName: 'dapp_pin',
      name: 'dapp_pin',
      url: url,
      location: location
    };
    
    this.sendEvent(event);
  }
}
```

### ❌ Avoid
Don't manually add base properties to every event - use the abstraction layer instead.

## Schema Validation

Use the schemas to validate your events before sending them to your analytics service. The schemas ensure data quality and consistency across your application.

## File Structure

```
schemas/
├── _main.schema.json          # Base properties for all events
├── dapp-browser.schema.json   # Dapp browser specific events
└── ton-connect.schema.json    # TON Connect specific events
``` 