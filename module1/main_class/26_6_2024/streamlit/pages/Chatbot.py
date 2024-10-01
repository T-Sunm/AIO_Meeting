import streamlit as st
def main():
  st.title("Object Detection for Images")
  with st.sidebar:
    st.title('Login HugChat')
    hf_email = st.text_input('Enter E-mail:')
    hf_pass = st.text_input('Enter Password:', type='password')
    if not (hf_email and hf_pass):
      st.warning('Please enter your account!', icon='⚠️')
    else:
      st.success('Proceed to entering your prompt message!', icon='👉')


if __name__ == "__main__":
  main()
