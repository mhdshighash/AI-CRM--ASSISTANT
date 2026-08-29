import streamlit as st
import json

from google import genai

from tools.crm_tools import (
    get_all_customers,
    get_customer_deals,
    get_deals_by_status,
    get_customer_notes,
    add_note
)
# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI CRM Assistant",
    page_icon="🤖",
    layout="wide"
)

client = genai.Client()

# =========================
# GEMINI CRM TOOL
# =========================

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
# =========================
# SIDEBAR
# =========================

st.sidebar.title("🤖 AI CRM")
st.sidebar.caption("Customer Relationship Manager")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👥 Customers",
        "💰 Deals",
        "📝 Notes",
        "🤖 AI Assistant"
    ]
)

# =========================
# LOAD DATA
# =========================

customers = get_all_customers()
won_deals = get_deals_by_status("Won")

# =========================
# DASHBOARD
# =========================

# =========================
# DASHBOARD
# =========================

if page == "🏠 Dashboard":

    st.title("🏠 CRM Dashboard")
    st.caption("Overview of your customer relationships and sales pipeline")

    # -------------------------
    # METRICS
    # -------------------------

    total_customers = len(customers)
    total_won_deals = len(won_deals)

    total_won_value = sum(
        deal[2] for deal in won_deals
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="👥 Total Customers",
            value=total_customers
        )

    with col2:
        st.metric(
            label="🏆 Won Deals",
            value=total_won_deals
        )

    with col3:
        st.metric(
            label="💰 Won Revenue",
            value=f"${total_won_value:,.0f}"
        )

    st.divider()

    # -------------------------
    # WON DEALS
    # -------------------------

    st.subheader("🏆 Won Deals")

    if won_deals:

        won_deals_display = []

        for deal in won_deals:

            won_deals_display.append({
                "Customer": deal[0],
                "Deal": deal[1],
                "Value": f"${deal[2]:,.0f}",
                "Status": deal[3]
            })

        st.dataframe(
            won_deals_display,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No won deals found.")

    st.divider()

    # -------------------------
    # CUSTOMER OVERVIEW
    # -------------------------

    st.subheader("👥 Customer Overview")

    customer_display = []

    for customer in customers:

        customer_id, name, email, company = customer

        customer_deals = get_customer_deals(name)

        customer_display.append({
            "Customer": name,
            "Company": company,
            "Email": email,
            "Deals": len(customer_deals)
        })

    st.dataframe(
        customer_display,
        width="stretch",
        hide_index=True
    )

# =========================
# CUSTOMERS
# =========================

# =========================
# CUSTOMERS
# =========================

elif page == "👥 Customers":

    st.title("👥 Customers")
    st.caption("Manage and review your customer relationships")

    # -------------------------
    # CUSTOMER COUNT
    # -------------------------

    st.info(
        f"You currently have **{len(customers)} customers** in your CRM."
    )

    # -------------------------
    # CUSTOMER LIST
    # -------------------------

    for customer in customers:

        customer_id, name, email, company = customer

        with st.expander(
            f"👤 {name}  •  {company}",
            expanded=False
        ):

            # Customer information

            st.subheader("Customer Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Customer ID**")
                st.write(customer_id)

            with col2:
                st.write("**Email**")
                st.write(email)

            with col3:
                st.write("**Company**")
                st.write(company)

            st.divider()

            # -------------------------
            # DEALS
            # -------------------------

            st.subheader("💰 Deals")

            deals = get_customer_deals(name)

            if deals:

                deal_display = []

                for deal in deals:

                    deal_display.append({
                        "Deal": deal[1],
                        "Value": f"${deal[2]:,.0f}",
                        "Status": deal[3]
                    })

                st.dataframe(
                    deal_display,
                    width="stretch",
                    hide_index=True
                )

            else:

                st.info(
                    "No deals found for this customer."
                )

            st.divider()

            # -------------------------
            # NOTES
            # -------------------------

            st.subheader("📝 Recent Notes")

            notes = get_customer_notes(name)

            if notes:

                for note in notes:

                    note_id, note_text, created_at = note

                    st.write(
                        f"**{created_at}**"
                    )

                    st.write(note_text)

                    st.divider()

            else:

                st.info(
                    "No notes found for this customer."
                )

# =========================
# DEALS
# =========================

# =========================
# DEALS
# =========================

elif page == "💰 Deals":

    st.title("💰 Deals")
    st.caption("Track and manage your sales pipeline")

    # -------------------------
    # GET ALL DEALS
    # -------------------------

    all_deals = []

    for customer in customers:

        customer_id, name, email, company = customer

        customer_deals = get_customer_deals(name)

        all_deals.extend(customer_deals)

    # -------------------------
    # METRICS
    # -------------------------

    total_deals = len(all_deals)

    total_pipeline_value = sum(
        deal[2] for deal in all_deals
    )

    total_won_value = sum(
        deal[2]
        for deal in all_deals
        if deal[3] == "Won"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "💼 Total Deals",
            total_deals
        )

    with col2:

        st.metric(
            "📊 Pipeline Value",
            f"${total_pipeline_value:,.0f}"
        )

    with col3:

        st.metric(
            "🏆 Won Revenue",
            f"${total_won_value:,.0f}"
        )

    st.divider()

    # -------------------------
    # FILTER
    # -------------------------

    status = st.selectbox(
        "🔎 Filter by status",
        [
            "All",
            "New",
            "Contacted",
            "Won",
            "Lost"
        ]
    )

    # -------------------------
    # FILTER DEALS
    # -------------------------

    if status == "All":

        deals = all_deals

    else:

        deals = [
            deal
            for deal in all_deals
            if deal[3] == status
        ]

    # -------------------------
    # DISPLAY DEALS
    # -------------------------

    st.subheader(
        f"Deals — {status}"
    )

    if deals:

        deal_display = []

        for deal in deals:

            deal_display.append({
                "Customer": deal[0],
                "Deal": deal[1],
                "Value": f"${deal[2]:,.0f}",
                "Status": deal[3]
            })

        st.dataframe(
            deal_display,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            f"No {status.lower()} deals found."
            if status != "All"
            else "No deals found."
        )

## =========================
# NOTES
# =========================

elif page == "📝 Notes":

    st.title("📝 Customer Notes")
    st.caption("Review and record customer interactions")

    # -------------------------
    # SELECT CUSTOMER
    # -------------------------

    selected_customer = st.selectbox(
        "👤 Select customer",
        customers,
        format_func=lambda customer:
            f"{customer[1]} — {customer[3]}"
    )

    customer_id, customer_name, email, company = selected_customer

    st.divider()

    # -------------------------
    # ADD NEW NOTE
    # -------------------------

    st.subheader("➕ Add New Note")

    new_note = st.text_area(
        "Note",
        placeholder="Enter a note about this customer...",
        height=120
    )

    if st.button(
        "➕ Add Note",
        width="stretch"
    ):

        if new_note.strip():

            result = add_note(
                customer_id,
                new_note.strip()
            )

            st.success(result)

            st.rerun()

        else:

            st.warning(
                "Please enter a note before adding."
            )

    st.divider()

    # -------------------------
    # NOTE HISTORY
    # -------------------------

    st.subheader(
        f"📝 Notes for {customer_name}"
    )

    notes = get_customer_notes(
        customer_name
    )

    if notes:

        for note in notes:

            note_id, note_text, created_at = note

            with st.container(border=True):

                st.caption(
                    f"🕒 {created_at}"
                )

                st.write(
                    note_text
                )

    else:

        st.info(
            "No notes found for this customer."
        )
# =========================
# AI ASSISTANT
# =========================

elif page == "🤖 AI Assistant":

    st.title("🤖 AI CRM Assistant")

    st.caption(
        "Ask questions about customers, deals, and CRM activity using natural language."
    )

    # -------------------------
    # CHAT HISTORY
    # -------------------------

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # Display previous messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # -------------------------
    # USER INPUT
    # -------------------------

    user_input = st.chat_input(
        "Ask something about your CRM..."
    )

    if user_input:

        # Show user message

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):

            st.markdown(user_input)

        # -------------------------
        # GEMINI REQUEST
        # -------------------------

        with st.chat_message("assistant"):

            try:

                interaction = client.interactions.create(
                    model="gemini-3.6-flash",
                    input=user_input,
                    tools=[
                        get_customer_deals_tool
                    ]
                )

                result = None

                # -------------------------
                # PROCESS TOOL CALL
                # -------------------------

                for step in interaction.steps:

                    if step.type == "function_call":

                        arguments = step.arguments

                        if step.name == "get_customer_deals":

                            result = get_customer_deals(
                                arguments["customer_name"]
                            )

                # -------------------------
                # FORMAT CRM RESULT
                # -------------------------

                if result is not None:

                    final_interaction = client.interactions.create(
                        model="gemini-3.6-flash",
                        input=[
                            {
                                "type": "text",
                                "text":
                                    "Format this CRM result clearly "
                                    "for the user:\n"
                                    + json.dumps(result)
                            }
                        ]
                    )

                    answer = final_interaction.output_text

                else:

                    answer = interaction.output_text

                # Display answer

                st.markdown(answer)

                # Save assistant response

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            # -------------------------
            # ERROR HANDLING
            # -------------------------

            except Exception as e:

                error_message = str(e)

                if "quota" in error_message.lower():

                    answer = (
                        "⚠️ **Gemini API quota exceeded.**\n\n"
                        "Your CRM database and Streamlit application "
                        "are working correctly, but Gemini's API "
                        "quota is currently unavailable.\n\n"
                        "Please wait for the quota to reset or use "
                        "a billing-enabled API plan."
                    )

                elif "429" in error_message:

                    answer = (
                        "⚠️ **Gemini API rate limit reached.**\n\n"
                        "Please wait and try again."
                    )

                else:

                    answer = (
                        "⚠️ **Something went wrong while contacting "
                        "the AI service.**\n\n"
                        f"Error: `{error_message}`"
                    )

                st.warning(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

    # -------------------------
    # CLEAR CHAT
    # -------------------------

    if st.session_state.messages:

        if st.button("🗑️ Clear Chat"):

            st.session_state.messages = []

            st.rerun()