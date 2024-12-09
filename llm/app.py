import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

# Function to get response from LLaMA 2 model
def getMentalHealthResponse(selected_issues, tone):
    input_text = ", ".join(selected_issues)
    llm = CTransformers(
        model='models/llama-2-7b-chat.ggmlv3.q4_0.bin',  
        model_type='llama',
        config={'max_new_tokens': 50, 'temperature': 0.7}
    )
    
    # Prompt Template
    template = """
        Provide a comforting message for someone experiencing {input_text}.
        Keep the tone {tone} and offer practical, supportive advice.
    """
    prompt = PromptTemplate(input_variables=["input_text", "tone"], template=template)
    
    try:
        print(f"Prompt: {prompt.format(input_text=input_text, tone=tone)}")
        response = llm.invoke(prompt.format(input_text=input_text, tone=tone))
        print(f"Response: {response}")
        
        return response
    except Exception as e:
        # Debugging: Print the error if it occurs
        print(f"Error occurred: {str(e)}")
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="Mental Health Support",
    page_icon="💙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.header("Mental Health Support 💙")

# Disclaimer
st.warning(
    """
    **Disclaimer:** This application is not a substitute for professional psychological or psychiatric help.
    If you're experiencing serious mental health challenges, please consult a licensed psychologist or psychiatrist.
    This tool provides temporary, supportive advice and is not intended to replace therapy or medical care.
    Take the output with caution and prioritize seeking professional help.
    """
)

# Checkbox options for selecting feelings
st.write("Select the issues you're experiencing:")
stress = st.checkbox("Stress")
anxiety = st.checkbox("Anxiety")
depression = st.checkbox("Depression")
suicidal_thoughts = st.checkbox("Suicidal Thoughts")

# Collect selected issues
selected_issues = []
if stress:
    selected_issues.append("stress")
if anxiety:
    selected_issues.append("anxiety")
if depression:
    selected_issues.append("depression")
if suicidal_thoughts:
    selected_issues.append("suicidal thoughts")

# Allow the user to choose a tone for the response
tone = st.selectbox("Choose a tone for the response", ("Calm", "Empathetic", "Uplifting"), index=0)

# Submit button
submit = st.button("Get Support")

# Display response
if submit and selected_issues:
    st.subheader("Here's some comforting advice:")
    response = getMentalHealthResponse(selected_issues, tone)
    st.write(response)
elif submit:
    st.warning("Please select at least one issue you're experiencing.")
