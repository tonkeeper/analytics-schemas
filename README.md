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

### Pre-commit Hooks

This repository includes pre-commit hooks that automatically validate all JSON schema files against the JSON Schema draft 2020-12 specification. The hooks will:

1. **Check JSON syntax** - Ensures all JSON files are properly formatted
2. **Validate JSON Schemas** - Validates that `.schema.json` files conform to the draft 2020-12 specification

#### Setup

Pre-commit hooks are already configured in `.pre-commit-config.yaml`. To install them:

```bash
pip install pre-commit
pre-commit install
```

#### Manual Validation

You can also manually validate schema files:

```bash
# Validate all schema files
python scripts/validate_schemas.py schemas/*.schema.json

# Validate a specific schema file
python scripts/validate_schemas.py schemas/_main.schema.json
```

The validation script will show detailed error messages if any schemas are invalid, including the specific path where errors occur.

### GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/validate-schemas.yml`) that automatically:

1. **Validates JSON schemas** on every push and pull request
2. **Checks JSON syntax** for all JSON files
3. **Auto-updates index.json** when schema files are added/removed
4. **Generates validation reports** as artifacts
5. **Auto-commits changes** back to the repository when needed

#### Features

- **Multi-trigger**: Runs on push to `main`/`develop`, pull requests, and manual dispatch
- **Smart detection**: Only runs update logic when schema files actually change
- **Safe automation**: Only pushes back to `main` branch, includes `[skip ci]` to prevent loops
- **Comprehensive validation**: Uses the same validation logic as pre-commit hooks
- **Artifact reports**: Saves validation reports for debugging

#### Manual Index Update

You can also manually update the `index.json` file:

```bash
python scripts/update_index.py
```

This script automatically scans the `schemas/` directory and updates `index.json` with all `.schema.json` files (except `_main.schema.json`).

## File Structure

```
schemas/
├── _main.schema.json          # Base properties for all events
├── dapp-browser.schema.json   # Dapp browser specific events
└── ton-connect.schema.json    # TON Connect specific events
``` 