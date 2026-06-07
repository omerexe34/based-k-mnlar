import html_template
from flask import render_template_string
from extensions import app

with app.app_context():
    try:
        res = render_template_string(
            html_template.HTML_CODE,
            onesignal_app_id="test",
            supabase_url="test",
            supabase_key="test",
        )
        print("SUCCESS! Render length:", len(res))
    except Exception as e:
        import traceback
        traceback.print_exc()
