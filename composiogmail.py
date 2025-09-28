from composio import Composio
from openai import OpenAI

composio = Composio(api_key="xxxxx")

# env: OPENAI_API_KEY
openai_client = OpenAI()

# Id of the user in your system
externalUserId = "<emaiid>"

connection_request = composio.connected_accounts.initiate(
  user_id=externalUserId,
  auth_config_id="<configid>",
)

# Redirect user to the OAuth flow
redirect_url = connection_request.redirect_url

print(f'Please authorize the app by visiting this URL: {redirect_url}') # Print the redirect url to the user

# Wait for the connection to be established
connected_account = connection_request.wait_for_connection()
print(f'Connection established successfully! Connected account id: {connected_account.id}')


# Get Gmail tools that are pre-configured
tools = composio.tools.get(user_id=externalUserId, tools=["GMAIL_SEND_EMAIL"])

# Get response from the LLM
response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
          "role": "user",
          "content": (
            f"Send an email to <emailid> with the subject 'Hello from composio 👋🏻' and "
            "the body 'Congratulations on sending your first email using AI Agents and Composio!'"
          ),
        },
    ],
)

# Execute the function calls.
result = composio.provider.handle_tool_calls(response=response, user_id=externalUserId)
print(result)
print("Email sent successfully!")
