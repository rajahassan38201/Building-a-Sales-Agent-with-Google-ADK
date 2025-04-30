import streamlit as st
import csv
import os
import asyncio
import re  
import nest_asyncio
nest_asyncio.apply()

from agent.main_agent import sales_agents_pipeline

# Initialize leads.csv if not present
csv_file = 'leads.csv'
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['lead_id', 'name', 'age', 'country', 'interest', 'status'])

# Load leads
async def load_leads():
    leads = []
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                leads.append(row)
    return leads

# Save or update a lead
async def save_or_update_lead(new_data):
    leads = await load_leads()
    updated = False
    for lead in leads:
        if lead['lead_id'] == new_data['lead_id']:
            lead.update(new_data)
            updated = True
            break
    if not updated:
        leads.append(new_data)
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['lead_id', 'name', 'age', 'country', 'interest', 'status'])
        writer.writeheader()
        writer.writerows(leads)

# --- Streamlit App Title ---
st.title("📞 Sales Agent - Lead Interaction")

# --- Session Initialization ---
if 'lead_id' not in st.session_state:
    st.session_state.lead_id = None
    st.session_state.lead_name = None
    st.session_state.awaiting_consent = False
    st.session_state.awaiting_answer = False
    st.session_state.current_field = None
    st.session_state.responses = {}
    st.session_state.conversation_finished = False

# --- Lead Form ---
with st.form("lead_form", clear_on_submit=True) as form:
    lead_id = st.text_input("Lead ID", key="lead_id_input")
    lead_name = st.text_input("Lead Name", key="lead_name_input")
    submit = st.form_submit_button("Start Interaction")

    if submit:
        errors = {}
        if not lead_id.strip():
            errors['lead_id'] = "Lead ID cannot be empty."
        if not lead_name.strip():
            errors['lead_name'] = "Lead Name cannot be empty."

        if errors:
            for field, error in errors.items():
                st.error(f"Error in '{field}': {error}")
        else:
            st.session_state.lead_id = lead_id.strip()
            st.session_state.lead_name = lead_name.strip()
            st.session_state.step = 0
            st.session_state.responses = {}
            st.session_state.awaiting_consent = True
            st.session_state.awaiting_answer = False
            st.session_state.conversation_finished = False

            asyncio.run(save_or_update_lead({
                'lead_id': st.session_state.lead_id,
                'name': st.session_state.lead_name,
                'age': '',
                'country': '',
                'interest': '',
                'status': 'pending'
            }))

# --- Conversation ---
if st.session_state.lead_id and not st.session_state.conversation_finished:
    current_step = st.session_state.step
    agent = sales_agents_pipeline[current_step]
    prompt_text = agent.instruction.replace("{lead_name}", st.session_state.lead_name)

    with st.form(f"response_form_{current_step}"):
        st.info(prompt_text)
        user_reply = st.text_input("Your Response:")
        submit_response = st.form_submit_button("Submit Response (Double Click)")

        if submit_response:
            user_reply = user_reply.strip()
            validation_error = None

            if agent.name == "ask_age_agent":
                if not re.match(r"^\d+$", user_reply):
                    validation_error = "Please enter a valid age (numbers only)."
                elif not 1 <= int(user_reply) <= 150:
                    validation_error = "Please enter a realistic age."
            elif agent.name == "ask_country_agent":
                if not user_reply.strip():
                    validation_error = "Country cannot be empty."
                elif not re.match(r"^[a-zA-Z\s]+$", user_reply):
                    validation_error = "Country should only contain alphabets and spaces."
            elif agent.name == "ask_interest_agent":
                if not user_reply.strip():
                    validation_error = "Interest cannot be empty."

            if validation_error:
                st.error(validation_error)
            else:
                if current_step == 0:  # Consent Step
                    if user_reply.lower() in ["yes", "y", "yeap"]:
                        st.session_state.awaiting_consent = False
                        st.session_state.awaiting_answer = True
                        st.session_state.step += 1
                    elif user_reply.lower() in ["no", "n", "not"]:
                        st.warning("Alright, no problem. Have a great day!")
                        asyncio.run(save_or_update_lead({
                            'lead_id': st.session_state.lead_id,
                            'name': st.session_state.lead_name,
                            'age': '',
                            'country': '',
                            'interest': '',
                            'status': 'no_response'
                        }))
                        st.session_state.conversation_finished = True
                    else:
                        st.error("Please respond with 'yes' or 'no' for consent.")
                else:
                    if agent.name == "ask_age_agent":
                        st.session_state.responses['age'] = user_reply
                    elif agent.name == "ask_country_agent":
                        st.session_state.responses['country'] = user_reply
                    elif agent.name == "ask_interest_agent":
                        st.session_state.responses['interest'] = user_reply

                    if current_step < len(sales_agents_pipeline) - 2:
                        st.session_state.step += 1
                    else:
                        placeholder = st.empty()

                        async def final_save():
                            with placeholder.container():
                                with st.spinner('💾 Saving your information, please wait...'):
                                    await asyncio.sleep(2)

                            await save_or_update_lead({
                                'lead_id': st.session_state.lead_id,
                                'name': st.session_state.lead_name,
                                'age': st.session_state.responses.get('age', ''),
                                'country': st.session_state.responses.get('country', ''),
                                'interest': st.session_state.responses.get('interest', ''),
                                'status': 'secured'
                            })

                            placeholder.success("✅ Thank you! Your information has been saved successfully.")
                            st.balloons()

                            st.session_state.conversation_finished = True
                            st.session_state.lead_id = None
                            st.session_state.lead_name = None
                            st.session_state.awaiting_consent = False
                            st.session_state.awaiting_answer = False
                            st.session_state.current_field = None
                            st.session_state.responses = {}

                        asyncio.run(final_save())

# --- Follow-Up Button ---
if st.session_state.conversation_finished:
    if st.button("Start New Interaction"):
        st.rerun()
elif st.session_state.lead_id and st.button("Simulate Follow-Up"):
    st.info("🔔 Reminder sent to lead.")
elif st.session_state.conversation_finished and not st.session_state.lead_id and st.button("Simulate Follow-Up"):
    st.info("Please start a new interaction first.")
