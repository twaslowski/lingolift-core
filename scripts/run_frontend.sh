export PYTHONPATH=$(git rev-parse --show-toplevel)
pushd streamlit_app > /dev/null
poetry run streamlit run app.py
popd
