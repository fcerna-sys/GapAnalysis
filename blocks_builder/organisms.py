"""
Módulo para crear componentes complejos (organismos).
Componentes que usan moléculas y átomos: slider, hero, section, cards, gallery, etc.
"""
import os
import json
from typing import Optional
from .helpers import get_bem_prefix
from .renders import (
    _generate_slider_render_php,
    _render_simple_section,
    _render_sidebar,
    _render_search,
    _render_pagination,
    _render_header,
    _render_footer,
    _render_form,
    _render_menu,
    _render_gallery,
    _render_section,
    _render_cards,
    _render_hero,
)
from .editors import (
    _generate_slider_editor_js,
    _editor_simple_section,
    _editor_sidebar,
    _editor_search,
    _editor_pagination,
    _editor_header,
    _editor_footer,
    _editor_form,
    _editor_menu,
)
from .styles import (
    _generate_slider_style_css,
    _generate_slider_editor_css,
)

# Importar funciones de creación de bloques desde el backup
# Reutilizar el módulo backup de renders.py para evitar cargar múltiples veces
from .renders import backup as backup_module

try:
    # Inyectar funciones auxiliares en el namespace del backup ANTES de importar las funciones
    # Esto permite que las funciones del backup usen las funciones auxiliares importadas
    backup_module._generate_slider_render_php = _generate_slider_render_php
    backup_module._generate_slider_editor_js = _generate_slider_editor_js
    backup_module._generate_slider_style_css = _generate_slider_style_css
    backup_module._generate_slider_editor_css = _generate_slider_editor_css
    backup_module._render_simple_section = _render_simple_section
    backup_module._render_sidebar = _render_sidebar
    backup_module._render_search = _render_search
    backup_module._render_pagination = _render_pagination
    backup_module._render_header = _render_header
    backup_module._render_footer = _render_footer
    backup_module._render_form = _render_form
    backup_module._render_menu = _render_menu
    backup_module._render_gallery = _render_gallery
    backup_module._render_section = _render_section
    backup_module._render_cards = _render_cards
    backup_module._render_hero = _render_hero
    backup_module._editor_simple_section = _editor_simple_section
    backup_module._editor_sidebar = _editor_sidebar
    backup_module._editor_search = _editor_search
    backup_module._editor_pagination = _editor_pagination
    backup_module._editor_header = _editor_header
    backup_module._editor_footer = _editor_footer
    backup_module._editor_form = _editor_form
    backup_module._editor_menu = _editor_menu
    
    # Importar funciones de creación de bloques desde el backup
    # Estas funciones ahora pueden usar las funciones auxiliares inyectadas
    create_slider_block = getattr(backup_module, 'create_slider_block', None)
    create_hero_block = getattr(backup_module, 'create_hero_block', None)
    create_section_block = getattr(backup_module, 'create_section_block', None)
    create_cards_block = getattr(backup_module, 'create_cards_block', None)
    create_gallery_block = getattr(backup_module, 'create_gallery_block', None)
    create_text_image_block = getattr(backup_module, 'create_text_image_block', None)
    create_sidebar_block = getattr(backup_module, 'create_sidebar_block', None)
    create_search_block = getattr(backup_module, 'create_search_block', None)
    create_pagination_block = getattr(backup_module, 'create_pagination_block', None)
    create_header_block = getattr(backup_module, 'create_header_block', None)
    create_footer_block = getattr(backup_module, 'create_footer_block', None)
    create_form_block = getattr(backup_module, 'create_form_block', None)
    create_menu_block = getattr(backup_module, 'create_menu_block', None)
    
    # Funciones de organismos (wrappers que llaman a las funciones de bloques)
    def create_organism_slider(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Slider - usa moléculas y átomos."""
        if create_slider_block:
            create_slider_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_hero(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Hero - usa moléculas y átomos."""
        if create_hero_block:
            create_hero_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_section(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Section - usa moléculas y átomos."""
        if create_section_block:
            create_section_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_cards_grid(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Cards Grid - usa molécula card."""
        if create_cards_block:
            create_cards_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_gallery(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Gallery."""
        if create_gallery_block:
            create_gallery_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_text_image(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Text+Image."""
        if create_text_image_block:
            create_text_image_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_sidebar(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Sidebar."""
        if create_sidebar_block:
            create_sidebar_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_search(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Search."""
        if create_search_block:
            create_search_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_pagination(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Pagination."""
        if create_pagination_block:
            create_pagination_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_header(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Header - usa molécula nav-item."""
        if create_header_block:
            create_header_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_footer(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Footer."""
        if create_footer_block:
            create_footer_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_form(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Form - usa molécula form-field."""
        if create_form_block:
            create_form_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_menu(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Menu - usa molécula nav-item."""
        if create_menu_block:
            create_menu_block(organisms_dir, css_framework, bem_prefix)
except Exception as e:
    # Si falla, crear stubs básicos
    def create_slider_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el bloque Slider."""
        pass
    
    def create_hero_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el bloque Hero."""
        pass
    
    create_section_block = None
    create_cards_block = None
    create_gallery_block = None
    create_text_image_block = None
    create_sidebar_block = None
    create_search_block = None
    create_pagination_block = None
    create_header_block = None
    create_footer_block = None
    create_form_block = None
    create_menu_block = None
    
    # Wrappers de organismos
    def create_organism_slider(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Slider - usa moléculas y átomos."""
        if create_slider_block:
            create_slider_block(organisms_dir, css_framework, bem_prefix)
    
    def create_organism_hero(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
        """Crea el organismo Hero - usa moléculas y átomos."""
        if create_hero_block:
            create_hero_block(organisms_dir, css_framework, bem_prefix)
    
    create_organism_section = None
    create_organism_cards_grid = None
    create_organism_gallery = None
    create_organism_text_image = None
    create_organism_sidebar = None
    create_organism_search = None
    create_organism_pagination = None
    create_organism_header = None
    create_organism_footer = None
    create_organism_form = None
    create_organism_menu = None

__all__ = [
    'create_slider_block',
    'create_hero_block',
    'create_section_block',
    'create_cards_block',
    'create_gallery_block',
    'create_text_image_block',
    'create_sidebar_block',
    'create_search_block',
    'create_pagination_block',
    'create_header_block',
    'create_footer_block',
    'create_form_block',
    'create_menu_block',
    'create_organism_slider',
    'create_organism_hero',
    'create_organism_section',
    'create_organism_cards_grid',
    'create_organism_gallery',
    'create_organism_text_image',
    'create_organism_sidebar',
    'create_organism_search',
    'create_organism_pagination',
    'create_organism_header',
    'create_organism_footer',
    'create_organism_form',
    'create_organism_menu',
]
