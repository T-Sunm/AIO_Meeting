import streamlit as st
from PIL import Image
import io
def main():

  # display text
  st.title("MY PROJECT")
  st.header("This is a header")
  st.subheader("This is a subheader")
  st.text("I love AI VIET NAM")
  st.caption("Anh minh có đẹp trai không")

  st.divider()

  # text elements
  # 1. Display string formatted as Markdown
  st.markdown("# Heading 1")

  # viết link '(link)'
  st.markdown("[AI VIETNAM](https://aivietnam.edu.vn/)")
  st.markdown("""
  1. Machine Learning
  2. Deep Learning
  """)

  # viết công thức toán học (r"$ ctth $")
  st.markdown(r"$ \sqrt{2x+2}$")
  st.latex("\\sqrt{2x+2}")

  # 2. Write arguments to the app.
  st.write('I love AI VIET NAM')
  st.write('## Heading 2')
  st.write('$ \\sqrt{2x+2} $')
  st.write('1 + 1 = ', 2)

  # 3. Code format
  st.code("""
  import torch
  data = torch.Tensor([1, 2, 3])
  print(data)
  """, language="python")

  def get_user_name():
    return 'Minhdeptrai'

  # khi có quá nhiều khối code , đây vào hết echo
  with st.echo():
    st.write('This code will be printed')

    def get_email():
      return 'minh@gmail.com'
    user_name = get_user_name()
    email = get_email()
    st.write(user_name, email)

  st.divider()

  # ----------------------Media Element-----------------------------------
  st.logo('../data/logo.png')
  st.image('../data/dogs.jpeg', caption='Funny dogs.')
  st.audio('../data/audio.mp4')
  st.video('../data/video.mp4')

  st.divider()

  # ------------------------Input Widgets----------------------------------

  # 1.Checkbox
  # Tạo một biến trạng thái để lưu trữ trạng thái của checkbox
  if 'checkbox_state' not in st.session_state:
    st.session_state.checkbox_state = False

  def get_name():
    # mỗi lần checkbox thay đổi là get_name sẽ đc gọi là cập nhật lại checkbox_state
    st.session_state.checkbox_state = not st.session_state.checkbox_state
  agree = st.checkbox("I agree", on_change=get_name)

  if st.session_state.checkbox_state:
    st.write("Thai")
  if agree:
    st.write("Great!")

  # 2.Radio
  st.radio("Your favorite color:",
           ['Yellow', 'Bleu'],
           captions=['Vàng', 'Xanh'])

  # 3. Selectbox
  option = st.selectbox(
      "Your contact:", ("Email", "Home phone", "Mobile phone"))
  st.write("Selected:", option)

  # 4. Multiselect
  options = st.multiselect(
      "Your favorite colors:",
      ["Green", "Yellow", "Red", "Blue"],

      # check box mặc định khi render lần đầu
      ["Yellow", "Red"])
  st.write("You selected:", options)

  # 5. Select slider
  color = st.select_slider(
      "Your favorite color:",
      options=["red", "orange", "violet"])
  st.write("My favorite color is", color)

  # 6. Button elements
  # nếu nhấn st.button thì hiện chữ Hello
  if st.button("Say hello"):
    st.write("Hello")
  else:
    st.write("Goodbye")
  st.link_button(
      "Go to Google",
      "https://www.google.com.vn/"
  )

  st.divider()

  # -----------------------Text Input Elements--------------------------
  # 1. Text input
  # text_input(title , initial text)
  title = st.text_input("Movie title:", "Life of Brian")
  st.write("The current movie title is", title)

  # chat elements

  # Tạo một container để chứa các tin nhắn chat, với chiều cao 200px
  messages = st.container(height=200)

  # Sử dụng st.chat_input để tạo một input box cho người dùng nhập tin nhắn
  # Biến prompt sẽ lưu trữ nội dung tin nhắn người dùng nhập vào
  if prompt := st.chat_input("Say something"):
    # Nếu người dùng nhập tin nhắn, nó sẽ được hiển thị dưới dạng một tin nhắn của người dùng
    messages.chat_message("user").write(prompt)

  messages.chat_message("assistant").write(f"Echo: {prompt}")

  st.divider()

  # ---------File Uploader Widget---------
  # 1. Upload multiple files
  uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
  for uploaded_file in uploaded_files:
    # đọc file ở dạng byte
    bytes_data = uploaded_file.read()

    # sài io.BytesIO để xử lý và preview Image
    image = Image.open(io.BytesIO(bytes_data))
    st.image(image=image, caption=f"filename: {uploaded_file.name}")

  st.divider()

  # -------------Form---------------
  with st.form("my_form"):
    col1, col2 = st.columns(2)
    f_name = col1.text_input('First Name')
    l_name = col2.text_input('Last Name')
    submitted = st.form_submit_button("Submit")
    if submitted:
      st.write("First Name: ", f_name, " - Last Name:", l_name)


if __name__ == "__main__":
  main()
