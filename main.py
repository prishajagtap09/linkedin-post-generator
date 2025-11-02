import streamlit as st
from few_shots import FewShotPosts
from llm_helper import llm
from langchain_core.prompts import PromptTemplate

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


# Main app layout
def main():
    st.subheader("LinkedIn Post Generator")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()
    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)



    # Generate Button
   
    if st.button("Generate"):   
    
    # All this logic now runs ONLY when the button is clicked
    
    # 1. Define a prompt template that uses your variables
        template = """
        You are an expert LinkedIn post generator.
        Write a LinkedIn post based on the following topic.
    
        Topic: {tag}
        Length: {length}
        Language: {language}
        """
    
        pt = PromptTemplate.from_template(template)
    
        # 2. Create a chain that pipes the prompt to the llm
        chain = pt | llm 
    
        # 3. Invoke the chain with the user's selected options
        with st.spinner("Generating post..."):
            response = chain.invoke({
            "tag": selected_tag,
            "length": selected_length,
            "language": selected_language
            })

            # 4. Write the AI's response
            st.write(response.content)

# Run the app
if __name__ == "__main__":
    main()

