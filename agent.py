import json


from google import genai
from tools.crm_tools import get_customer_deals, get_deals_by_status, update_deal_status, add_note, get_customer_id_by_name

# ==========================================
# 1. CREATE GEMINI CLIENT
# ==========================================

client = genai.Client()


# ==========================================
# 2. DEFINE CRM TOOL
# ==========================================

get_customer_deals_tool = {
    "type": "function",
    "name": "get_customer_deals",
    "description": "Get all deals belonging to a specific customer by customer name.",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_name": {
                "type": "string",
                "description": "The name of the customer."
            }
        },
        "required": ["customer_name"]
    }
}

get_deals_by_status_tool = {
    "type": "function",
    "name": "get_deals_by_status",
    "description": "Get all CRM deals that have a specific status.",
    "parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "The deal status. Must be New, Contacted, Won, or Lost."
            }
        },
        "required": ["status"]
    }
}

update_deal_status_tool = {
    "type": "function",
    "name": "update_deal_status",
    "description": "Update the status of a CRM deal. Use this when the user explicitly asks to change a deal's status.",
    "parameters": {
        "type": "object",
        "properties": {
            "deal_id": {
                "type": "integer",
                "description": "The ID of the deal to update."
            },
            "new_status": {
                "type": "string",
                "description": "The new status. Must be New, Contacted, Won, or Lost."
            }
        },
        "required": ["deal_id", "new_status"]
    }
}

add_note_tool = {
    "type": "function",
    "name": "add_note",
    "description": "Add a note to a customer in the CRM.",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "integer",
                "description": "The ID of the customer."
            },
            "note": {
                "type": "string",
                "description": "The note to save for the customer."
            }
        },
        "required": ["customer_id", "note"]
    }
}
get_customer_id_tool = {
    "type": "function",
    "name": "get_customer_id_by_name",
    "description": "Find the customer ID using the customer's name.",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_name": {
                "type": "string",
                "description": "The name of the customer."
            }
        },
        "required": ["customer_name"]
    }
}
# ==========================================
# 3. ASK GEMINI
# ==========================================

user_input = input("You: ")

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=user_input,
    tools=[get_customer_deals_tool, get_deals_by_status_tool, update_deal_status_tool,add_note_tool, get_customer_id_tool]
)

# ==========================================
# 4. PROCESS TOOL CALL
# ==========================================

for step in interaction.steps:

    if step.type == "function_call":

        arguments = step.arguments

        if step.name == "get_customer_deals":

            result = get_customer_deals(
                arguments["customer_name"]
            )

        elif step.name == "get_deals_by_status":

            result = get_deals_by_status(
                arguments["status"]
            )
        elif step.name == "update_deal_status":
            result = update_deal_status(
                arguments["deal_id"],
                arguments["new_status"]
            )
        elif step.name == "add_note":
            result = add_note(
                arguments["customer_id"],
                arguments["note"]
            )
        elif step.name == "get_customer_id_by_name":

            customer_id = get_customer_id_by_name(
                arguments["customer_name"]
            )

            result = {
                "customer_name": arguments["customer_name"],
                "customer_id": customer_id
            }
        else:

            result = "Unknown tool."

        print("\nTool result:")
        print(result)

        # ==========================================
        # 5. SEND RESULT BACK TO GEMINI
        # ==========================================

        final_interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {
                    "type": "text",
                    "text": "The CRM tool returned this result: "
                           + json.dumps(result)
                }
            ]
        )

        print("\nGemini's final answer:")
        print(final_interaction.output_text)