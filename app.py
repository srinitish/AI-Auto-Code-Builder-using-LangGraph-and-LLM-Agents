import streamlit as st
from agent.graph import agent, save_files

st.title("Auto Code Builder")

user_prompt = st.text_area("Describe your project", height=150)

if st.button("Generate"):
    if not user_prompt.strip():
        st.warning("Please enter a project description.")
    else:
        with st.spinner("Running pipeline..."):
            try:
                result = agent.invoke({"user_prompt": user_prompt.strip()})

                plan = result.get("plan", "")
                task_plan = result.get("task_plan", "")
                code_files = result.get("code_files", {})

                save_files(code_files)

                st.success(f"Done! Generated {len(code_files)} file(s).")

                with st.expander("Plan"):
                    st.write(plan)

                with st.expander("Architecture Tasks"):
                    st.write(task_plan)

                st.subheader("Generated Files")
                for filename, content in code_files.items():
                    with st.expander(filename):
                        ext = filename.rsplit(".", 1)[-1] if "." in filename else "text"
                        st.code(content, language=ext)

            except Exception as e:
                st.error(f"Error: {e}")