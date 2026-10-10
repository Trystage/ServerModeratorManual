"""
Markdown 批量转 PDF (纯Python, 无需LaTeX)
用法: python md2pdf.py
将 texts/ 下所有 .md 文件转换为 output/ 下同名 .pdf
依赖: pip install markdown xhtml2pdf
"""
import os
import markdown
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

TEXTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "texts")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# 注册 CID 中文字体 (无需字体文件)
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

CSS = """
body { font-family: STSong-Light; font-size: 10pt; line-height: 1.8; margin: 2cm; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #333; padding: 5px 8px; text-align: left; font-family: STSong-Light; }
th { background-color: #f0f0f0; }
h1 { font-family: STSong-Light; font-size: 16pt; border-bottom: 2px solid #333; padding-bottom: 6px; }
h2 { font-family: STSong-Light; font-size: 13pt; border-bottom: 1px solid #999; padding-bottom: 4px; margin-top: 1.2em; }
h3 { font-family: STSong-Light; font-size: 11pt; margin-top: 1em; }
blockquote { border-left: 3px solid #ccc; margin-left: 0; padding-left: 1em; color: #555; font-family: STSong-Light; }
p { font-family: STSong-Light; }
li { font-family: STSong-Light; }
strong { font-family: STSong-Light; }
em { font-family: STSong-Light; }
"""

def md_to_pdf(md_path: str, pdf_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_body}</body></html>"""

    with open(pdf_path, "wb") as f:
        pisa.CreatePDF(html, dest=f)

    print(f"已生成: {os.path.basename(pdf_path)}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_files = sorted(f for f in os.listdir(TEXTS_DIR) if f.endswith(".md"))
    if not md_files:
        print("texts/ 目录下没有 .md 文件")
        exit(1)
    print(f"共 {len(md_files)} 个文件待转换\n")
    for name in md_files:
        md_path = os.path.join(TEXTS_DIR, name)
        pdf_path = os.path.join(OUTPUT_DIR, os.path.splitext(name)[0] + ".pdf")
        md_to_pdf(md_path, pdf_path)
    print(f"\n全部完成, PDF 已输出到: {OUTPUT_DIR}")
