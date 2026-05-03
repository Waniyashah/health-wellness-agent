import markdown
from fpdf import FPDF, HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    pass

# Read the markdown file
with open(r"C:\Users\Wahab\.gemini\antigravity\brain\1fb4fe6a-0211-4c7f-a19a-fc68c20695d0\health_wellness_agent_report.md", "r", encoding="utf-8") as f:
    text = f.read()

# Convert markdown to html
html = markdown.markdown(text)

# Initialize PDF
pdf = MyFPDF()
pdf.add_page()
# set font so it doesn't complain
pdf.set_font("Helvetica", size=12)

# FPDF requires some basic HTML, and cannot parse all elements perfectly, but it handles basic things
pdf.write_html(html)

pdf.output(r"e:\health-wellness\health-wellness-agent-main\Health_Wellness_Agent_Report.pdf")
