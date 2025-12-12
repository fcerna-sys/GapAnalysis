"""
Sistema profesional de versiones para patterns y bloques.
Incluye control de versión semántica, metadatos y detección de cambios.
"""
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class SemanticVersion:
    """Gestiona versiones semánticas (MAJOR.MINOR.PATCH)."""
    
    @staticmethod
    def parse(version: str) -> Tuple[int, int, int]:
        """Parsea una versión semántica."""
        parts = version.split('.')
        major = int(parts[0]) if len(parts) > 0 and parts[0] else 0
        minor = int(parts[1]) if len(parts) > 1 and parts[1] else 0
        patch = int(parts[2]) if len(parts) > 2 and parts[2] else 0
        return (major, minor, patch)
    
    @staticmethod
    def bump(version: str, bump_type: str = 'patch') -> str:
        """Incrementa una versión semántica."""
        major, minor, patch = SemanticVersion.parse(version)
        
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        elif bump_type == 'patch':
            patch += 1
        else:
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    @staticmethod
    def compare(v1: str, v2: str) -> int:
        """Compara dos versiones. Retorna -1 si v1 < v2, 0 si igual, 1 si v1 > v2."""
        m1, mi1, p1 = SemanticVersion.parse(v1)
        m2, mi2, p2 = SemanticVersion.parse(v2)
        
        if m1 != m2:
            return -1 if m1 < m2 else 1
        if mi1 != mi2:
            return -1 if mi1 < mi2 else 1
        if p1 != p2:
            return -1 if p1 < p2 else 1
        return 0


class BlockVersionManager:
    """Gestiona versiones de bloques individuales."""
    
    def __init__(self, theme_dir: str, bem_prefix: str = 'img2html'):
        self.theme_dir = theme_dir
        self.bem_prefix = bem_prefix
        self.blocks_meta_file = os.path.join(theme_dir, 'blocks-meta.json')
    
    def get_block_metadata(self, block_type: str, block_name: str) -> Dict:
        """Obtiene metadatos de un bloque."""
        meta = self._load_metadata()
        key = f"{block_type}/{block_name}"
        return meta.get('blocks', {}).get(key, {
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'hash': '',
            'changes': []
        })
    
    def update_block_version(self, block_type: str, block_name: str, 
                            block_dir: str, change_type: str = 'patch') -> str:
        """Actualiza la versión de un bloque y genera hash."""
        meta = self._load_metadata()
        key = f"{block_type}/{block_name}"
        
        block_meta = meta.setdefault('blocks', {}).setdefault(key, {})
        current_version = block_meta.get('version', '1.0.0')
        
        # Calcular hash del bloque
        block_hash = self._calculate_block_hash(block_dir)
        previous_hash = block_meta.get('hash', '')
        
        # Si el hash cambió, incrementar versión
        if block_hash != previous_hash:
            new_version = SemanticVersion.bump(current_version, change_type)
            block_meta.update({
                'version': new_version,
                'hash': block_hash,
                'updated': datetime.now().isoformat(),
                'previous_version': current_version,
                'changes': block_meta.get('changes', []) + [{
                    'version': new_version,
                    'date': datetime.now().isoformat(),
                    'type': change_type,
                    'hash': block_hash
                }]
            })
            
            if 'created' not in block_meta:
                block_meta['created'] = datetime.now().isoformat()
            
            self._save_metadata(meta)
            
            # Actualizar block.json
            self._update_block_json_version(block_dir, new_version)
            
            return new_version
        
        return current_version
    
    def _calculate_block_hash(self, block_dir: str) -> str:
        """Calcula hash MD5 de todos los archivos del bloque."""
        hasher = hashlib.md5()
        
        files_to_hash = ['block.json', 'render.php', 'style.css', 'index.js', 'editor.css']
        
        for filename in files_to_hash:
            file_path = os.path.join(block_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    hasher.update(f.read())
        
        return hasher.hexdigest()
    
    def _update_block_json_version(self, block_dir: str, version: str):
        """Actualiza la versión en block.json."""
        block_json_path = os.path.join(block_dir, 'block.json')
        if os.path.isfile(block_json_path):
            with open(block_json_path, 'r', encoding='utf-8') as f:
                block_json = json.load(f)
            
            block_json['version'] = version
            block_json.setdefault('metadata', {})['lastUpdated'] = datetime.now().isoformat()
            
            with open(block_json_path, 'w', encoding='utf-8') as f:
                json.dump(block_json, f, indent=2, ensure_ascii=False)
    
    def _load_metadata(self) -> Dict:
        """Carga metadatos de bloques."""
        if os.path.isfile(self.blocks_meta_file):
            with open(self.blocks_meta_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'version': '1.0.0',
            'bemPrefix': self.bem_prefix,
            'blocks': {},
            'generated': datetime.now().isoformat()
        }
    
    def _save_metadata(self, meta: Dict):
        """Guarda metadatos de bloques."""
        meta['updated'] = datetime.now().isoformat()
        with open(self.blocks_meta_file, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)


class PatternVersionManager:
    """Gestiona versiones de patterns."""
    
    def __init__(self, theme_dir: str, bem_prefix: str = 'img2html'):
        self.theme_dir = theme_dir
        self.bem_prefix = bem_prefix
        self.patterns_dir = os.path.join(theme_dir, 'patterns')
        self.patterns_meta_file = os.path.join(self.patterns_dir, 'patterns_meta.json')
    
    def get_pattern_version(self, pattern_slug: str) -> str:
        """Obtiene la versión actual de un pattern."""
        meta = self._load_patterns_meta()
        pattern = self._find_pattern(meta, pattern_slug)
        return pattern.get('version', '1.0.0') if pattern else '1.0.0'
    
    def update_pattern_version(self, pattern_slug: str, pattern_file: str, 
                              change_type: str = 'patch', reason: str = '') -> str:
        """Actualiza la versión de un pattern."""
        meta = self._load_patterns_meta()
        patterns = meta.get('patterns', [])
        
        pattern = self._find_pattern(meta, pattern_slug)
        if not pattern:
            # Crear nuevo pattern
            pattern = {
                'slug': pattern_slug,
                'filename': pattern_file,
                'version': '1.0.0',
                'created': datetime.now().isoformat(),
                'updated': datetime.now().isoformat(),
                'hash': '',
                'changes': []
            }
            patterns.append(pattern)
        
        # Calcular hash del pattern
        pattern_path = os.path.join(self.patterns_dir, pattern_file)
        pattern_hash = self._calculate_pattern_hash(pattern_path)
        previous_hash = pattern.get('hash', '')
        
        # Si el hash cambió, incrementar versión
        if pattern_hash != previous_hash:
            current_version = pattern.get('version', '1.0.0')
            new_version = SemanticVersion.bump(current_version, change_type)
            
            pattern.update({
                'version': new_version,
                'hash': pattern_hash,
                'updated': datetime.now().isoformat(),
                'previous_version': current_version,
                'changes': pattern.get('changes', []) + [{
                    'version': new_version,
                    'date': datetime.now().isoformat(),
                    'type': change_type,
                    'hash': pattern_hash,
                    'reason': reason
                }]
            })
            
            if 'created' not in pattern:
                pattern['created'] = datetime.now().isoformat()
            
            self._save_patterns_meta(meta)
            
            return new_version
        
        return pattern.get('version', '1.0.0')
    
    def should_regenerate_pattern(self, pattern_slug: str, design_hash: str) -> bool:
        """Determina si un pattern debe regenerarse basado en cambios en el diseño."""
        meta = self._load_patterns_meta()
        pattern = self._find_pattern(meta, pattern_slug)
        
        if not pattern:
            return True
        
        # Si el hash del diseño cambió, debe regenerarse
        design_hash_stored = pattern.get('designHash', '')
        return design_hash != design_hash_stored
    
    def mark_pattern_regenerated(self, pattern_slug: str, design_hash: str, 
                                change_type: str = 'patch'):
        """Marca un pattern como regenerado y actualiza su versión."""
        meta = self._load_patterns_meta()
        pattern = self._find_pattern(meta, pattern_slug)
        
        if pattern:
            pattern['designHash'] = design_hash
            pattern['lastRegenerated'] = datetime.now().isoformat()
            # Incrementar versión si el diseño cambió
            if pattern.get('designHash') != design_hash:
                current_version = pattern.get('version', '1.0.0')
                new_version = SemanticVersion.bump(current_version, change_type)
                pattern['version'] = new_version
                pattern['previous_version'] = current_version
                pattern['updated'] = datetime.now().isoformat()
        
        self._save_patterns_meta(meta)
    
    def _calculate_pattern_hash(self, pattern_path: str) -> str:
        """Calcula hash MD5 del contenido del pattern."""
        if not os.path.isfile(pattern_path):
            return ''
        
        hasher = hashlib.md5()
        with open(pattern_path, 'rb') as f:
            hasher.update(f.read())
        
        return hasher.hexdigest()
    
    def _find_pattern(self, meta: Dict, pattern_slug: str) -> Optional[Dict]:
        """Encuentra un pattern en los metadatos."""
        patterns = meta.get('patterns', [])
        for pattern in patterns:
            if pattern.get('slug') == pattern_slug or pattern.get('slug') == f"{self.bem_prefix}/{pattern_slug}":
                return pattern
        return None
    
    def _load_patterns_meta(self) -> Dict:
        """Carga patterns_meta.json."""
        if os.path.isfile(self.patterns_meta_file):
            with open(self.patterns_meta_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'version': '1.0.0',
            'bemPrefix': self.bem_prefix,
            'patterns': [],
            'generated': datetime.now().isoformat()
        }
    
    def _save_patterns_meta(self, meta: Dict):
        """Guarda patterns_meta.json."""
        meta['updated'] = datetime.now().isoformat()
        with open(self.patterns_meta_file, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)


def calculate_design_hash(plan: Dict, dna: Optional[Dict] = None) -> str:
    """Calcula hash del diseño basado en plan y DNA."""
    hasher = hashlib.md5()
    
    # Incluir información relevante del plan
    plan_str = json.dumps({
        'sections': plan.get('sections', []),
        'layout_rows': plan.get('layout_rows', []),
        'patterns': plan.get('patterns', [])
    }, sort_keys=True)
    hasher.update(plan_str.encode('utf-8'))
    
    # Incluir información del DNA
    if dna:
        dna_str = json.dumps({
            'colors': dna.get('colors', []),
            'typography': dna.get('typography', {}),
            'spacing': dna.get('spacing', {})
        }, sort_keys=True)
        hasher.update(dna_str.encode('utf-8'))
    
    return hasher.hexdigest()


def update_all_block_versions(theme_dir: str, bem_prefix: str = 'img2html', 
                              change_type: str = 'patch'):
    """Actualiza versiones de todos los bloques en el tema."""
    bvm = BlockVersionManager(theme_dir, bem_prefix)
    blocks_dir = os.path.join(theme_dir, 'blocks')
    
    updated_blocks = []
    
    # Átomos
    atoms_dir = os.path.join(blocks_dir, 'atoms')
    if os.path.isdir(atoms_dir):
        for atom_name in os.listdir(atoms_dir):
            atom_path = os.path.join(atoms_dir, atom_name)
            if os.path.isdir(atom_path):
                version = bvm.update_block_version('atom', atom_name, atom_path, change_type)
                updated_blocks.append(('atom', atom_name, version))
    
    # Moléculas
    molecules_dir = os.path.join(blocks_dir, 'molecules')
    if os.path.isdir(molecules_dir):
        for molecule_name in os.listdir(molecules_dir):
            molecule_path = os.path.join(molecules_dir, molecule_name)
            if os.path.isdir(molecule_path):
                version = bvm.update_block_version('molecule', molecule_name, molecule_path, change_type)
                updated_blocks.append(('molecule', molecule_name, version))
    
    # Organismos
    organisms_dir = os.path.join(blocks_dir, 'organisms')
    if os.path.isdir(organisms_dir):
        for organism_name in os.listdir(organisms_dir):
            organism_path = os.path.join(organisms_dir, organism_name)
            if os.path.isdir(organism_path):
                version = bvm.update_block_version('organism', organism_name, organism_path, change_type)
                updated_blocks.append(('organism', organism_name, version))
    
    return updated_blocks


def enhance_patterns_meta_with_versions(theme_dir: str, bem_prefix: str = 'img2html', 
                                       plan: Optional[Dict] = None, dna: Optional[Dict] = None):
    """Mejora patterns_meta.json con versiones y metadatos completos."""
    pvm = PatternVersionManager(theme_dir, bem_prefix)
    patterns_dir = os.path.join(theme_dir, 'patterns')
    
    if not os.path.isdir(patterns_dir):
        return
    
    # Calcular hash del diseño
    design_hash = calculate_design_hash(plan or {}, dna)
    
    # Cargar patterns_meta.json existente
    meta = pvm._load_patterns_meta()
    patterns = meta.get('patterns', [])
    
    # Actualizar versiones de todos los patterns
    pattern_files = [f for f in os.listdir(patterns_dir) if f.endswith('.php')]
    
    for pattern_file in pattern_files:
        pattern_slug = os.path.splitext(pattern_file)[0]
        
        # Buscar pattern en metadata
        pattern = pvm._find_pattern(meta, pattern_slug)
        
        if pattern:
            # Verificar si debe regenerarse
            should_regenerate = pvm.should_regenerate_pattern(pattern_slug, design_hash)
            
            if should_regenerate:
                # Actualizar versión y hash del diseño
                pvm.mark_pattern_regenerated(pattern_slug, design_hash, 'patch')
            else:
                # Solo actualizar hash del diseño sin cambiar versión
                pattern['designHash'] = design_hash
        else:
            # Nuevo pattern
            version = pvm.update_pattern_version(pattern_slug, pattern_file, 'patch', 
                                                'Pattern generado inicialmente')
            pattern = pvm._find_pattern(meta, pattern_slug)
            if pattern:
                pattern['designHash'] = design_hash
    
    # Añadir metadatos globales
    meta['designHash'] = design_hash
    meta['lastDesignUpdate'] = datetime.now().isoformat()
    meta['version'] = meta.get('version', '1.0.0')
    
    # Guardar
    pvm._save_patterns_meta(meta)
    
    print(f"✓ Versiones de patterns actualizadas. Hash del diseño: {design_hash[:8]}...")

