# backend/src/infrastructure/pdf_service.py

import os
import io
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pypdf import PdfMerger
from ..domain.interfaces import PdfServiceInterface
from ..core.config import settings
from ..core.constants import ErrorKeys

class BasePdfService:
    """Base class to handle Jinja2 template rendering."""
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(str(settings.template_dir)))

    def render_template(self, template_name: str, context: dict) -> str:
        template = self.env.get_template(template_name)
        return template.render(**context)

class PlaywrightPdfService(BasePdfService, PdfServiceInterface):
    async def generate_single_page_pdf(self, page_path: Path, context: dict, config: dict) -> bytes:
        """Gera um PDF para uma página específica com suas configurações."""
        from playwright.async_api import async_playwright
        import tempfile
        
        # Renderiza o template da página
        context["base_url"] = page_path.absolute().as_uri() + "/"
        print(f"Base URL for template: {context['base_url']}")  # Debugging line
        
        template_file = page_path / "report_template.html"
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_file}")
        
        # Usa o loader com o diretório específico da página
        page_env = Environment(loader=FileSystemLoader(str(page_path)))
        template = page_env.get_template("report_template.html")
        html_content = template.render(**context)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(args=[
                '--disable-web-security',
                '--allow-file-access-from-files'
            ])
            page = await browser.new_page()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as tmp_file:
                tmp_file.write(html_content)
                tmp_file_path = tmp_file.name
            
            try:
                await page.goto(f"file://{tmp_file_path}", wait_until="networkidle")
                
                # Usa as configurações específicas da página
                print(f"Config: {config}")  # Debugging line
                pdf_bytes = await page.pdf(**config)
            finally:
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
            
            await browser.close()
            return pdf_bytes
    
    async def generate_pdf_merged(self, context: dict) -> bytes:
        """Gera PDFs de cada página separadamente e depois faz merge."""
        pdf_merger = PdfMerger()
        
        # Itera por cada página definida em settings.pages_dir
        for page_config in settings.pages_dir:
            for page_path, config in page_config.items():
                print(f"Gerando PDF para: {page_path}")
                
                # Gera o PDF para esta página
                pdf_bytes = await self.generate_single_page_pdf(page_path, context, config)
                
                # Adiciona ao merger
                pdf_file = io.BytesIO(pdf_bytes)
                pdf_merger.append(pdf_file)
        
        # Escreve o PDF final em memória
        output = io.BytesIO()
        pdf_merger.write(output)
        pdf_merger.close()
        
        output.seek(0)
        return output.getvalue()
   