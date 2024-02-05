from streamlit.testing.v1 import AppTest

at = AppTest.from_file("grammr.py")

at.run()

at.get(at.session_state)

