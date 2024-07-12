# Vado Tecum

Vado Tecum is a personal project that will be an AI-powered ancient language tutor. At the moment, all development is happening around the Latin language.

# Getting Started

1) Clone the repository.
2) Insall dependencies found in `requirements.txt`
3) Create a `config.yaml` file in the root directory. It should look like this:

    ```yaml
    llm_provider: "openai"
    openai_model: "gpt-4o"
    openai_api_key: "..."
    anthropic_model: "claude-3-5-sonnet-20240620"
    anthropic_api_key: "..."
    texts_path: ".\\resources\\texts\\" # Path to the folder with texts
    app_save_path: ".\\resources\\app_save\\" # Path to the folder with app save files
    evaluations_path: ".\\resources\\evaluations\\" # Path to the folder with evaluations
    ```
5) From the root directory, run the `app` directory as a python module:

    ```python
    python -m app
    ```
