from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py")

at.run()

at.get(at.session_state)

