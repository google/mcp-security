# Frequently Asked Questions (FAQ)

This page covers common issues, errors, and questions encountered when setting up or using the Google MCP Security project.

---

### SOAR_URL Error: “Failed to fetch valid scopes from SOAR”

If you're using the **SOAR MCP server** and see the following error:

```
Error: Failed to fetch valid scopes from SOAR, please make sure you have configured the right SOAR credentials. Shutting down...
MCP error -32000: Connection closed
```

This usually means that the `SOAR_URL` environment variable is **not correctly set** or is pointing to the wrong base URL.

#### Why this happens

The SOAR MCP server tries to connect to the **SOAR platform**, but some users mistakenly configure it with a **Backstory URL**, which does not support the necessary endpoints. The Swagger documentation in Backstory also won’t show these SOAR endpoints, which can cause confusion.

---

### How to find your correct SOAR base URL

You can retrieve the correct `SOAR_URL` using one of the following methods:

#### Option 1: Using the Webhooks UI

1. In the SOAR platform, go to `Settings → Webhooks`.
2. Create a new webhook (the parameters don’t matter).
3. Copy the base URL from the generated Webhook URL.

> Example:  
> `https://s4i0z.siemplify-soar.com`

#### Option 2: Using Browser Developer Tools

1. Open Developer Tools in your browser (usually by pressing **F12**).
2. Switch to the **Network** tab.
3. In the SOAR UI, navigate to the **Cases** section.
4. Look for a request like `GetCaseCardsByRequest`.
5. Click on the request, go to the **Headers** tab, and copy the base URL from the `:authority` or full request URL field.

---