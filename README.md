# Football IQ & Performance Academy

## Run locally
1. `pip install -r requirements.txt`
2. Optional: copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your Supabase URL and anon key. Without it the app runs in clearly labelled DEMO mode.
3. `streamlit run app.py`

## Supabase
1. Create a project. In the SQL editor run `supabase_schema.sql` (row-level security makes each player's rows private).
2. Settings > API: copy the project URL and the **anon** key (never the service-role key).

## Deploy
Push to GitHub, create an app on Streamlit Community Cloud pointing at `app.py`, and paste the secrets file contents into Advanced settings > Secrets.

## Adding content
Append entries to `LESSONS`, `EXERCISES`, `POSITIONS`, `FORMATIONS` in `content.py`.
