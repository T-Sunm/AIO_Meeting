import streamlit as st

def levenshtein_distance(s, t):
  rows = len(s) + 1
  cols = len(t) + 1

  # Khởi tạo ma trận zero với kích thước (rows x cols)
  matrix = [[0] * cols for _ in range(rows)]

  # Điền giá trị cho cột 0 và hàng 0
  for i in range(rows):
    matrix[i][0] = i
  for j in range(cols):
    matrix[0][j] = j

  # Tính toán khoảng cách chỉnh sửa
  for i in range(1, rows):
    for j in range(1, cols):
      if s[i - 1] == t[j - 1]:
        matrix[i][j] = matrix[i - 1][j - 1]
      else:
        del_cost = matrix[i - 1][j]    # Chi phí xóa
        ins_cost = matrix[i][j - 1]    # Chi phí chèn
        sub_cost = matrix[i - 1][j - 1]  # Chi phí thay thế
        matrix[i][j] = min(del_cost, ins_cost, sub_cost) + 1

  # Giá trị ở góc dưới bên phải của ma trận là khoảng cách Levenshtein
  return matrix[rows - 1][cols - 1]

def load_vocab(file_path='../data/vocab.txt'):
  with open(file_path, 'r') as f:
    lines = f.readlines()
    words = sorted(set([line.strip() for line in lines]))
    return words


vocabs = load_vocab()
st.title('Word correction')
word = st.text_input("Vocab:", "Write something")
if st.button("Compute"):
  leven_distances = dict()
  for vocab in vocabs:
    distance = levenshtein_distance(word, vocab)
    leven_distances[vocab] = distance

  # Sử dụng .items() để lấy các cặp (key, value)
  # chuyển về tupple để sort thì nhớ ép về dict lại
  leven_distances = sorted(leven_distances.items(), key=lambda item: item[1])
  leven_distances = dict(leven_distances)
  col1, col2 = st.columns(2)
  col1.write(vocabs)
  col2.write(leven_distances)
